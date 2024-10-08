import asyncio
import time
import websockets

async def handler(websocket, path):
    data = await websocket.recv()
    print(f"Received message: {data}")
    await websocket.send(f"Echo: {data}")

start_server = websockets.serve(handler, "localhost", 8080)
print("WebSocket server started on ws://localhost:8080")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

#  Run `lsof -i :8080` to check if the WebSocket server is running on port 8080.`
