import network
import urequests
import time
from machine import Pin, I2C, SoftI2C
import ssd1306

SSID = "yourSSID"
PASS = "passwd"
# change IP of Pi Zero W.
SERVER_URL = "http://10.46.148.188:5000/api/telemetry"

i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Keypad Setup, 
# my 4x4 matrix keypad has R4-R3-R2-R1-C1-C2-C3-C4 pinout, check yours.
rows = [Pin(x, Pin.OUT) for x in [6, 7, 8, 9]]
cols = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in [5, 4, 3, 2]]

# Logical Map for teh keypad.
keys_map = [
    ['TOP',  'JGL',  'MID',  'STATS'],   # Row 1
    ['BOT',  'SUP',  'TEAM', 'BANS'],    # Row 2
    ['OPP1', 'OPP2', 'OPP3', 'MATCH'],   # Row 3
    ['*',    '0',    '#',    'HOME']     # Row 4
]

KEY_COMMANDS = {
    'TOP':  {"type": "filter", "target": "Top"},
    'JGL':  {"type": "filter", "target": "Jungle"},
    'MID':  {"type": "filter", "target": "Mid"},
    'BOT':  {"type": "filter", "target": "Bot"},
    'SUP':  {"type": "filter", "target": "Support"},
    'STATS': {"type": "view", "target": "statistics"},
    'BANS':  {"type": "view", "target": "ban_picks"},
    'MATCH': {"type": "view", "target": "overview"},
    'HOME':  {"type": "view", "target": "overview"},
    'TEAM':  {"type": "alert", "target": "C9"},
    'OPP1':  {"type": "alert", "target": "Enemy_Carry"}
}

def connect_wifi():
    w = network.WLAN(network.STA_IF)
    w.active(True)
    if not w.isconnected():
        oled.fill(0); oled.text("CONNECTING...", 0,0); oled.show()
        w.connect(SSID, PASS)
        while not w.isconnected(): time.sleep(1)
    print("IP:", w.ifconfig()[0])

def send_cmd(key_name):
    if key_name in KEY_COMMANDS:
        payload = KEY_COMMANDS[key_name]
        payload['key_name'] = key_name
        try:
            urequests.post(SERVER_URL, json=payload).close()
            oled.fill(0)
            oled.text(f"CMD: {key_name}", 0, 0)
            oled.text(f"ACT: {payload['type']}", 0, 20)
            oled.text(f"TGT: {payload['target']}", 0, 40)
            oled.show()
        except:
            oled.fill(0); oled.text("NET ERROR", 0,0); oled.show()

def scan_keys():
    for r in range(4):
        rows[r].value(1)
        for c in range(4):
            if cols[c].value():
                key = keys_map[r][c]
                while cols[c].value(): pass # Debounce
                rows[r].value(0)
                return key
        rows[r].value(0)
    return None

connect_wifi()
oled.fill(0)
oled.text("C9 TACTICAL", 10, 20)
oled.text("READY", 40, 40)
oled.show()

while True:
    k = scan_keys()
    if k: send_cmd(k)
    time.sleep(0.05)
