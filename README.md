# C9 Tactical Command Ecosystem: From Server to Soldier
A unified tactical ecosystem that bridges the gap between digital esports data and physical reflexes. This project combines a live Red Team Scouting Dashboard with a physical "Spike Defusal" Training Device that doubles as a tactical controller for analysts.

---
## How It Works
The ecosystem consists of two synchronized nodes:

* The C2 Server (Raspberry Pi Zero W):<br>
Connects to the GRID Series Events WebSocket to ingest live VALORANT/LoL match data.<br>
Runs a Flask Web Server that hosts the Tactical Dashboard.<br>
Processes "Red Team" algorithms to flag high-threat opponents based on live K/D variance.<br>

* The Field Device (Raspberry Pi Pico WH):<br>
Fan Mode: Runs a "Spike Defusal" speed mini-game.<br>
Analyst Mode: Acts as a "Tactical Stream Deck." Pressing keys on the physical keypad sends commands to the C2 Server to filter the dashboard views instantly (e.g., highlighting only the "Jungle" matchup).

---
## Hardware Requirements
* Server: Raspberry Pi Zero W (or any Python-capable PC/Pi).
* Client: Raspberry Pi Pico WH.
* Display: SSD1306 OLED Display (128x64, I2C).
* Input: 4x4 Matrix Membrane Keypad.
* Connectivity: Local Wi-Fi Network.

---
## Installation

* Part 1: The C2 Server (_Raspberry Pi Zero W_)<br>
Clone this repository:<br>
```bash
git clone https://github.com/YOUR_USERNAME/C9-Tactical-Command.git
cd C9-Tactical-Command/server
```
Install Dependencies:<br>
```bash
pip3 install flask websocket-client requests
```
Configure API Key:<br>
- Open `app.py`.
- Set `SIMULATION_MODE = True` for offline demos, or paste your `GRID_API_KEY` for live data.
Run the Server:<br>
```bash
python3 app.py
```
**The dashboard is now live at `http://<PI_ZERO_IP>:5000`**

* Part 2: The Field Device (Raspberry Pi Pico WH)<br>
1. Flash MicroPython: Ensure your Pico WH has the latest uf2 firmware.
2. Upload Libraries:
Save ssd1306.py (standard library) to the Pico.
3. Configure Network:
Open `main.py`.
Update `SSID` and `PASSWORD` with your Wi-Fi credentials.
Update `SERVER_URL` to point to your Pi Zero: `http://192.168.1.XX:5000/api/telemetry`.
4. Wiring:
OLED: SDA -> GP4, SCL -> GP5. (You can check the pin out if it doesn't work.)
Keypad Rows: GP6, GP7, GP8, GP9.
Keypad Cols: GP5, GP4, GP3, GP2.

---
## Usage Manual

|  Key  |      Function     |                       Description                       |
|-------|-------------------|---------------------------------------------------------|
|  JGL  |   Filter: Jungle  |    Dims all rows except the Jungle matchup.             |
|  MID  |   Filter: Mid     |    Focuses on the Mid lane.                             |
| STATS |   View: Analytics |   "Switches screen to the ""Advanced Stats"" graph."    |
|  HOME |   View: Overview  |    Resets dashboard to the full Roster view.            | 
|  OPP1 |   Alert: Threat   |   "Flags the enemy Top Laner as a ""Critical Threat.""" |

* Mode 2: Fan Activation ("Spike Defusal")<br>
- Press 'A' on the keypad to ARM the device.
- The OLED will show a countdown timer.
- Watch the Dashboard: The Server status will turn RED (ARMED).
- Enter the secret code (Default: 7359) before time runs out.
- Win: Dashboard status turns CYAN (DEFUSED).

---
# Snapshots
* The application server `app.py`:<br>
<img width="987" height="576" alt="image" src="https://github.com/user-attachments/assets/3d1acc96-befb-4323-8db0-8cbb2c4bbe3b" /><br>

* Web Interface:<br>
<img width="1856" height="1076" alt="image" src="https://github.com/user-attachments/assets/8e14cb1c-5865-4fea-92f6-57a7058724c3" />

* The physical edge device:<br>
<img width="2560" height="1928" alt="image" src="https://github.com/user-attachments/assets/7b7d68c3-7b88-4593-b4af-0d96276f447b" />


---
## License
Distributed under the MIT License.  – see the [LICENSE](LICENSE) file for details.
