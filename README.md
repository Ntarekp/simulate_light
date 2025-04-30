# IoT Light Scheduler Dashboard

![Dashboard Display](screenshot-img/display.png)

A simple browser‑based dashboard to schedule an Arduino‑controlled light via WebSockets → MQTT → Serial.

## Features

- **Frontend**: HTML/CSS/JS interface to pick ON/OFF times.
- **WebSocket Server**: Python `websockets` server that publishes schedules to MQTT (`mosquitto_pub`).
- **MQTT Subscriber**: Python script using `mosquitto_sub` + `schedule` to forward ON/OFF commands to Arduino over serial (or simulate in mock mode).
- **Cyberpunk Theme**: Neon‑glow UI with flickering text and animated button accents.

## Prerequisites

- **Hardware (optional)**: Arduino UNO with relay module (or run in simulation mode).
- **Software**:
  - `mosquitto` (broker, `mosquitto_pub`, `mosquitto_sub`)
  - Python 3.7+

## Project Structure

```
├── backend            # WebSocket server code
├── frontend           # HTML/CSS/JS dashboard files
├── screenshot-img     # Contains display.png screenshot
├── subscriber         # MQTT subscriber & scheduler script
└── README.md          # Project overview and instructions
```

## Getting Started

1. **Clone the repo**  
   ```bash  
   git clone https://github.com/Ntarekp/iot-dashboard.git  
   cd iot-dashboard  
   ```

2. **Create & activate venv**  
   ```bash  
   python3 -m venv .env  
   source .env/bin/activate      # Windows: .env\Scripts\activate.bat
   ```

3. **Install dependencies**  
   ```bash  
   sudo apt update && sudo apt install -y mosquitto mosquitto-clients  # Linux
   pip install --upgrade pip  
   pip install websockets pyserial schedule  
   ```

4. **Run the WebSocket server**  
   ```bash  
   python backend/websocket_server.py  
   ```

5. **Run the subscriber**  
   ```bash  
   python subscriber/subscriber.py  
   ```

6. **Open the dashboard**  
   ```bash  
   open frontend/index.html  # or navigate to file in browser
   ```

## Simulation Mode

To test without hardware, in `subscriber/subscriber.py` set `SIMULATION = True`.  
