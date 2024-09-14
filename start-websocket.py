import os
import sys
import asyncio

# Activate the virtual environment
venv_path = os.path.join(os.path.dirname(__file__), 'venv', 'bin', 'activate_this.py')
with open(venv_path) as f:
    exec(f.read(), {'__file__': venv_path})
import websockets

async def handler(websocket, path):
    data = await websocket.recv()
    print(f"Received message: {data}")
    await websocket.send(f"Echo: {data}")

start_server = websockets.serve(handler, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
