#!/usr/bin/env python3
import asyncio
import json
import subprocess
import os
import websockets

# MQTT settings (can override via ENV vars)
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "light/schedule")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")

async def handler(websocket, path=None):
    """
    Handle incoming WebSocket messages. Each message is expected to be JSON with "on"/"off" times.
    Publishes the schedule to MQTT and sends an acknowledgement back.
    """
    async for message in websocket:
        try:
            schedule = json.loads(message)
            # Publish to MQTT
            subprocess.run([
                "mosquitto_pub",
                "-h", MQTT_HOST,
                "-t", MQTT_TOPIC,
                "-m", json.dumps(schedule)
            ], check=True)
            # Send back acknowledgement
            await websocket.send(json.dumps({"status": "Published to MQTT"}))
        except Exception as e:
            await websocket.send(json.dumps({"status": f"Error: {e}"}))

async def main():
    server = await websockets.serve(handler, "0.0.0.0", 6789)
    print(f"WebSocket server listening on ws://0.0.0.0:6789")
    await server.wait_closed()

if __name__ == "__main__":
    # Use asyncio.run for compatibility
    asyncio.run(main())
