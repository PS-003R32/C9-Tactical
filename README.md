# C9 Tactical Command Ecosystem: From Server to Soldier
A high-pressure **"Spike Defusal" Event Game** where fans race against the clock to disarm a C9 spike, powered by a live-syncing hardware ecosystem that mimics the pressure of the VCT stage.
This project combines a fast-paced **Event Mini-Game** with a professional **Red Team Scouting Dashboard**, proving that the fun is built on pro-grade tech.

---
## How It Works
The ecosystem consists of two synchronized nodes:

* The C9 Server (Raspberry Pi Zero W):<br>
Acts as the central game authority, validating defusal codes and managing the game state.<br>
Connects to the **GRID Series Events WebSocket** to ingest live match data when in "Analyst Mode".<br>
Runs a Flask Web Server that hosts the **Arena Dashboard**.<br>

* The Field Device (Raspberry Pi Pico WH):<br>
-> **Mode 1 (Fan Game):** Runs the "Spike Defusal" simulator. Fans must Arm the device and enter a code before the OLED timer hits zero.<br>
-> **Mode 2 (Analyst Tool):** Acts as a "Tactical Stream Deck".
  Pressing keys on the physical keypad sends commands to the C2 Server to filter the dashboard views instantly (e.g., highlighting only the "Jungle" matchup).


---
## Hardware Requirements
* Server: Raspberry Pi Zero W (or any Python-capable PC/Pi).
* Client: Raspberry Pi Pico WH.
* Display: SSD1306 OLED Display (128x64, I2C).
* Input: 4x4 Matrix Membrane Keypad.
* Connectivity: Local Wi-Fi Network.

---
## Installation

* Part 1: The C9 Server (_Raspberry Pi Zero W_)<br>
Clone this repository:<br>
```bash
git clone https://github.com/PS-003R32/C9-Tactical.git
cd C9-Tactical/
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

1. The Physical-to-Logical Mapping.

|  Physical Key  |   Logical Function   |       Category      |
|----------------|----------------------|---------------------|
|        1       |         TOP          |      Lane Filter    |
|        2       |         JGL          |      Lane Filter    |
|        3       |         MID          |      Lane Filter    |
|        A       |         ARM          |      Game Trigger   |
|        4       |         BOT          |     Lane Filter     |
|        5       |         SUP          |     Lane Filter     |
|        6       |         TEAM         |     Alert/Highlight |
|        B       |         BANS         |     View Switcher   |
|        7       |         OPP1         |     Alert/Highlight |
|        8       |         OPP2         |     (Reserved)      |
|        9       |         OPP3         |     (Reserved)      |
|        C       |         STATS        |     View Switcher   |
|        *       |         *            |     Game Input      |
|        0       |         0            |     Game Input      |
|        #       |         #            |     Game Input      |
|        D       |         HOME         |     System Reset    |

2. Detailed Function Explanation<br>

A. Game Mode (The Fan Experience) Designed for the Event Booth.
**Start**: Press '`A`' to `ARM` the device.
**The Challenge**: A `45-second` countdown begins on the OLED.
**Action**: Enter the secret code (Default: `7359`) and press `#` before time runs out.
**Win**: The Arena Dashboard turns CYAN (ROUND SECURED). 
**Lose**: The Arena Dashboard triggers a "`DETONATION`" event.

B. Analyst Mode (Default) When the game is not running, the keypad acts as a tactical controller for the dashboard.
**Lane Filters (`1`-`5`)**: Instantly cuts through the noise.
**Action**: Press `2` (`JGL`).
**Result**: Dims all rows on the dashboard except the Jungle matchup, allowing the coach to focus. 
**View Switchers (`B`, `C`, `D`)**: Changes the screen layout.
- `STATS` (Key `C`): Switches to the live "Momentum Graph" (Chart.js). 
- `BANS` (Key `B`): Switches to the Pick/Ban Recommendation engine. 
- `HOME` (Key `D`): Resets the dashboard to the main Roster View. 
**Tactical Alerts (`6`, `7`)**:
- TEAM (Key '6'): Highlights Cloud9 players in Cyan to signal a great play. 
- OPP1 (Key '7'): Flags the enemy carry in Red as a "Critical Threat".<br>

_The keypad isn't just a number pad. It is a context-aware controller. During a tactical review, Button '2' focuses the dashboard on the Jungle matchup. But during a fan activation event, that same Button '2' becomes part of the defusal code for the Spike Simulator. This dual-purpose design allows one hardware device to serve both analysts and fans._

---
### Example
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
<img width="1917" height="1154" alt="image" src="https://github.com/user-attachments/assets/6b271f29-d2e5-4305-8a8d-bd840c7c896a" /><br>

* The physical edge device:<br>
<img width="2560" height="1928" alt="image" src="https://github.com/user-attachments/assets/7b7d68c3-7b88-4593-b4af-0d96276f447b" />


---
## License
Distributed under the MIT License.  – see the [LICENSE](LICENSE) file for details.
