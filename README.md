# C9 Tactical Command Ecosystem: From Server to Soldier
A unified tactical ecosystem that bridges the gap between digital esports data and physical reflexes. This project combines a live Red Team Scouting Dashboard with a physical "Spike Defusal" Training Device that doubles as a tactical controller for analysts.

---
## How It Works
The ecosystem consists of two synchronized nodes:

* The C9 Server (Raspberry Pi Zero W):<br>
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
|        A       |         STATS        |     View Switcher   |
|        4       |         BOT          |     Lane Filter     |
|        5       |         SUP          |     Lane Filter     |
|        6       |         TEAM         |     Alert/Highlight |
|        B       |         BANS         |     View Switcher   |
|        7       |         OPP1         |     Alert/Highlight |
|        8       |         OPP2         |     (Reserved)      |
|        9       |         OPP3         |     (Reserved)      |
|        C       |         MATCH        |     View Switcher   |
|        *       |         *            |     Game Input      |
|        0       |         0            |     Game Input      |
|        #       |         #            |     Game Input      |
|        D       |         HOME         |     System Reset    |

2. Detailed Function Explanation<br>

A. Lane Filters (The "Focus" Buttons)<br>
These buttons allow an analyst to instantly cut through the noise on the dashboard.<br>
**Keys**: `TOP`, `JGL`, `MID`, `BOT`, `SUP`.<br>
**Code Action**: Sends `{"type": "filter", "target": "RoleName"}`.<br>
Result on Dashboard:<br>
The Javascript frontend receives this command.<br>
It applies a CSS class (.dimmed) to all player rows that do not match the selected target.<br>
Example: Pressing '2' (JGL) makes the Top, Mid, Bot, and Support rows fade to 20% opacity, leaving the Jungle matchup highlighted in bright green.<br>

B. View Switchers (The "Screen" Buttons)<br>
These buttons change the entire layout of the web dashboard, acting like tabs in a browser but controlled physically.<br>

`STATS (Key 'A')`:<br>
**Payload**: `{"type": "view", "target": "statistics"}`.<br>
**Result**: Hides the "Roster Intel" panel and reveals the "Advanced Analytics" panel (graphs/charts).<br>

`BANS (Key 'B')`:<br>
**Payload**: `{"type": "view", "target": "ban_picks"}`.<br>
**Result**: Switches the screen to the Pick/Ban recommendation engine (Category 3).<br>

`MATCH (Key 'C')`:<br>
**Payload**: `{"type": "view", "target": "overview"}`.<br>
**Result**: Forces the screen back to the main Live Feed.<br>

`HOME (Key 'D')`:<br>
**Payload**: `{"type": "view", "target": "overview"}`, plus resets all filters.<br>
**Result**: "Panic Button." Resets the dashboard to its default state (showing all lanes, main view).<br>

C. Tactical Alerts (The "Action" Buttons)<br>
These are context-specific triggers used to flag specific events during a match.<br>

`TEAM` (Key '6'):<br>
**Payload**: {"type": "alert", "target": "C9"}.<br>
**Result**: Highlights your own team's roster section (e.g., flashes blue), useful for signaling a `"Great Play"` or `"Team Synergy"` moment.<br>

`OPP1` (Key '7'):<br>
**Payload**: {"type": "alert", "target": "Enemy_Carry"}.<br>
**Result**: Automatically identifies the highest-risk enemy player (from the GRID data) and flashes their name RED on the big screen.<br>

D. Game Inputs (The "Defusal" Buttons)<br>
When the device is in Fan Activation Mode (Spike Defusal Game), these keys revert to standard numeric inputs.<br>
**Keys**: `0-9`, `*`, `#`<br>
**Function**: Used to type the 4-digit defusal code.<br>
**Logic**: The code checks if `game_state == "ARMED"`. If yes, it treats these keys as numbers. If `game_state == "MENU"`, it treats them as Tactical Commands.<br>

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
<img width="1856" height="1076" alt="image" src="https://github.com/user-attachments/assets/8e14cb1c-5865-4fea-92f6-57a7058724c3" />

* The physical edge device:<br>
<img width="2560" height="1928" alt="image" src="https://github.com/user-attachments/assets/7b7d68c3-7b88-4593-b4af-0d96276f447b" />


---
## License
Distributed under the MIT License.  – see the [LICENSE](LICENSE) file for details.
