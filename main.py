import network
import urequests
import time
from machine import Pin, I2C, SoftI2C
import ssd1306

SSID = "yourSSID"
PASS = "passwd"
# change to the IP of Pi Zero W or your pc if you are running the server on your pc.
SERVER_URL = "http://10.46.148.188:5000/api/telemetry"

# --- HARDWARE SETUP ---
i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

rows = [Pin(x, Pin.OUT) for x in [6, 7, 8, 9]]
cols = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in [5, 4, 3, 2]]

# GAME State
# Modes: "ANALYST" (Default) or "GAME_RUNNING"
CURRENT_MODE = "ANALYST" 
DEFUSE_CODE = "7359"
USER_INPUT = ""
TIME_LEFT = 45

# Maping physical keys to their labels
KEY_MAP = [
    ['1', '2', '3', 'A'],  # 1=TOP, 2=JGL, 3=MID, A=START GAME
    ['4', '5', '6', 'B'],  # 4=BOT, 5=SUP, 6=TEAM, B=BANS
    ['7', '8', '9', 'C'],  # 7=OPP1, C=MATCH
    ['*', '0', '#', 'D']   # *=CLR, #=ENTER, D=HOME
]

ANALYST_COMMANDS = {
    '1': {"type": "filter", "target": "Top", "desc": "FILTER: TOP"},
    '2': {"type": "filter", "target": "Jungle", "desc": "FILTER: JUNGLE"},
    '3': {"type": "filter", "target": "Mid", "desc": "FILTER: MID"},
    '4': {"type": "filter", "target": "Bot", "desc": "FILTER: BOT"},
    '5': {"type": "filter", "target": "Support", "desc": "FILTER: SUPP"},
    '6': {"type": "alert",  "target": "C9", "desc": "HIGHLIGHT: C9"},
    '7': {"type": "alert",  "target": "Enemy_Carry", "desc": "ALERT: THREAT"},
    'B': {"type": "view",   "target": "ban_picks", "desc": "VIEW: BANS"},
    'C': {"type": "view",   "target": "statistics", "desc": "VIEW: STATS"},
    'D': {"type": "view",   "target": "overview", "desc": "VIEW: HOME"},
}

def connect_wifi():
    w = network.WLAN(network.STA_IF)
    w.active(True)
    oled.fill(0); oled.text("WIFI CONNECT...", 0,0); oled.show()
    if not w.isconnected():
        w.connect(SSID, PASS)
        while not w.isconnected(): time.sleep(1)
    print("IP:", w.ifconfig()[0])

def send_telemetry(payload):
    try:
        urequests.post(SERVER_URL, json=payload).close()
    except:
        pass

def scan_keypad():
    for r in range(4):
        rows[r].value(1)
        for c in range(4):
            if cols[c].value():
                key = KEY_MAP[r][c]
                while cols[c].value(): pass
                rows[r].value(0)
                return key
        rows[r].value(0)
    return None

# GAME LOGIC
def start_game():
    global CURRENT_MODE, USER_INPUT, TIME_LEFT
    CURRENT_MODE = "GAME_RUNNING"
    USER_INPUT = ""
    TIME_LEFT = 45
    send_telemetry({"type": "alert", "target": "SPIKE_ARMED", "key_name": "ARMED"})

def check_game_input(key):
    global USER_INPUT, CURRENT_MODE
    
    if key == '#':
        if USER_INPUT == DEFUSE_CODE:
            CURRENT_MODE = "GAME_WON"
            send_telemetry({"type": "alert", "target": "SPIKE_DEFUSED", "key_name": "DEFUSED"})
        else:
            USER_INPUT = ""
            
    elif key == '*': # Clear Key
        USER_INPUT = ""
        
    elif key in ['A', 'B', 'C', 'D']:
        pass
        
    else:
        if len(USER_INPUT) < 4:
            USER_INPUT += key

def update_display():
    oled.fill(0)
    
    if CURRENT_MODE == "ANALYST":
        oled.text("C9 TACTICAL", 15, 0)
        oled.text("MODE: ANALYST", 10, 20)
        oled.text("PRESS 'A'", 25, 45)
        oled.text("TO ARM SPIKE", 15, 55)
        
    elif CURRENT_MODE == "GAME_RUNNING":
        oled.text("!!! ARMED !!!", 15, 0)
        oled.text(f"TIME: {int(TIME_LEFT)}s", 25, 20)
        masked_input = USER_INPUT + "_" * (4 - len(USER_INPUT))
        oled.text(f"CODE: {masked_input}", 25, 40)
        
    elif CURRENT_MODE == "GAME_WON":
        oled.text("*** DEFUSED ***", 5, 20)
        oled.text("C9 WINS ROUND", 10, 40)
        
    elif CURRENT_MODE == "GAME_LOST":
        oled.text("### BOOM ###", 15, 20)
        oled.text("TERRORISTS WIN", 5, 40)

    oled.show()


connect_wifi()
last_tick = time.ticks_ms()

while True:
    key = scan_keypad()
    
    if key:
        if CURRENT_MODE == "ANALYST":
            if key == 'A':
                start_game()
            elif key in ANALYST_COMMANDS:
                cmd = ANALYST_COMMANDS[key]
                cmd['key_name'] = key
                send_telemetry(cmd)
                oled.fill(0)
                oled.text(cmd['desc'], 0, 20)
                oled.show()
                time.sleep(0.5)
                
        elif CURRENT_MODE == "GAME_RUNNING":
            check_game_input(key)
            
        elif CURRENT_MODE in ["GAME_WON", "GAME_LOST"]:
            if key == 'D':
                CURRENT_MODE = "ANALYST"
                send_telemetry({"type": "view", "target": "overview", "key_name": "RESET"})

    if CURRENT_MODE == "GAME_RUNNING":
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_tick) > 1000:
            TIME_LEFT -= 1
            last_tick = current_time
            if TIME_LEFT <= 0:
                CURRENT_MODE = "GAME_LOST"
                send_telemetry({"type": "alert", "target": "SPIKE_EXPLODED", "key_name": "BOOM"})

    update_display()
