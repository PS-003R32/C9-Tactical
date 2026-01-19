# C9 Tactical Command Ecosystem: From Server to Soldier
A unified tactical ecosystem that bridges the gap between digital esports data and physical reflexes. This project combines a live Red Team Scouting Dashboard with a physical "Spike Defusal" Training Device that doubles as a tactical controller for analysts.

---
## How It Works
The ecosystem consists of two synchronized nodes:

* The C2 Server (Raspberry Pi Zero W):
Connects to the GRID Series Events WebSocket to ingest live VALORANT/LoL match data.
Runs a Flask Web Server that hosts the Tactical Dashboard.
Processes "Red Team" algorithms to flag high-threat opponents based on live K/D variance.

* The Field Device (Raspberry Pi Pico WH):
Fan Mode: Runs a "Spike Defusal" speed mini-game.
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

* Part 1: The C2 Server (_Raspberry Pi Zero W_)
clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/C9-Tactical-Command.git
cd C9-Tactical-Command/server
```
