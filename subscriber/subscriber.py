#!/usr/bin/env python3
import subprocess
import threading
import json
import time
import schedule
import os

# Toggle simulation mode: True for mock (no hardware needed), False for real serial
SIMULATION = True

if not SIMULATION:
    import serial
    # Real serial configuration (use environment variables or defaults)
    SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyACM0")
    BAUD_RATE = int(os.getenv("BAUD_RATE", "9600"))
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
else:
    # FakeSerial class for simulation
    class FakeSerial:
        def __init__(self, port, baud, timeout):
            print(f"[SIM] Opening fake serial on {port} @ {baud}bps")
        def write(self, data):
            cmd = data.decode()
            print(f"[SIM] → Relay set to: {cmd!r}")
    SERIAL_PORT = "SIMULATOR"
    BAUD_RATE = 9600
    ser = FakeSerial(SERIAL_PORT, BAUD_RATE, timeout=1)

# MQTT configuration
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "light/schedule")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")


def schedule_jobs(on_time, off_time):
    """
    Clear existing jobs and schedule new ON/OFF commands.

    :param on_time:  HH:MM format for turning ON the light
    :param off_time: HH:MM format for turning OFF the light
    """
    schedule.clear()
    schedule.every().day.at(on_time).do(lambda: ser.write(b'1'))
    schedule.every().day.at(off_time).do(lambda: ser.write(b'0'))
    print(f"Scheduled ON at {on_time}, OFF at {off_time}")


def mqtt_listener():
    """
    Subscribe to MQTT_TOPIC and schedule jobs upon receiving a valid JSON payload.
    Payload example: {"on": "08:00", "off": "18:00"}
    """
    proc = subprocess.Popen(
        ["mosquitto_sub", "-h", MQTT_HOST, "-t", MQTT_TOPIC],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    for line in proc.stdout:
        try:
            data = json.loads(line.strip())
            on_time = data.get("on")
            off_time = data.get("off")
            if on_time and off_time:
                schedule_jobs(on_time, off_time)
        except json.JSONDecodeError:
            continue


if __name__ == "__main__":
    # Start MQTT listener thread
    threading.Thread(target=mqtt_listener, daemon=True).start()
    print("Subscriber running in {} mode, waiting for schedule...".format(
        "SIMULATION" if SIMULATION else "REAL_SERIAL"
    ))

    # Main loop to execute scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(1)
