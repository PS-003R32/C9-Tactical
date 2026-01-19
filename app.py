import threading
import json
import time
from flask import Flask, render_template, jsonify, request
import websocket


GRID_API_KEY = "yourAPIkey"
SERIES_ID = "28" # Try 28 (CS2) or 3 (LoL) if 6 is down
GRID_WS_URL = f"wss://api.grid.gg/live-data-feed/series/{SERIES_ID}?key={GRID_API_KEY}"

SIMULATION_MODE = True

app = Flask(__name__)
game_data = {
    "map": "OFFLINE",
    "score_c9": 0,
    "score_opp": 0,
    "events": [],
    "roster": {},
    "last_update": "N/A"
}

view_state = {
    "active_view": "overview",
    "active_filter": "ALL",
    "last_command": "None"
}

def run_simulation():
    print(">>> STARTING SIMULATION MODE")
    try:
        with open('match_replay.json', 'r') as f:
            script = json.load(f)
    except:
        print("Error: match_replay.json not found. Create it first!")
        return

    while True:
        game_data['map'] = "SIMULATION FEED"
        game_data['events'] = []
        game_data['roster'] = {}

        for step in script:
            time.sleep(step['delay'])
            game_data['last_update'] = time.strftime("%H:%M:%S")

            if step['type'] == 'event':
                # Handle Kills
                if step['action'] == 'killed':
                    msg = f"KILL: {step['actor']} -> {step['target']}"
                    game_data['events'].insert(0, {"time": game_data['last_update'], "msg": msg})

                    # Update Roster
                    actor = step['actor']
                    if actor not in game_data['roster']:
                        game_data['roster'][actor] = {"kills": 0, "role": step.get('role', 'Unknown'), "risk": "LOW"}

                    game_data['roster'][actor]['kills'] += 1
                    if game_data['roster'][actor]['kills'] > 1: game_data['roster'][actor]['risk'] = "HIGH"

                # Handle Plants
                elif 'msg' in step:
                    game_data['events'].insert(0, {"time": game_data['last_update'], "msg": step['msg']})

            elif step['type'] == 'state':
                game_data['map'] = step['map']
                game_data['score_c9'] = step['score_c9']

def on_message(ws, message):
    data = json.loads(message)
def start_grid_listener():
    if not SIMULATION_MODE:
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(GRID_WS_URL, on_message=on_message)
        ws.run_forever()
    else:
        run_simulation()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/telemetry', methods=['POST'])
def receive_command():
    cmd = request.json
    if cmd['type'] == 'filter':
        view_state['active_filter'] = cmd['target']
        view_state['active_view'] = 'overview'
    elif cmd['type'] == 'view':
        view_state['active_view'] = cmd['target']
        view_state['active_filter'] = 'ALL'

    view_state['last_command'] = f"{cmd.get('key_name', 'CMD')} -> {cmd['type']}"
    return jsonify({"status": "ACK"})

@app.route('/api/sync')
def sync_frontend():
    return jsonify({"game": game_data, "view": view_state})

if __name__ == '__main__':
    t = threading.Thread(target=start_grid_listener)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=5000)
