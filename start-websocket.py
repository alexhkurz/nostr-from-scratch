import asyncio
import websockets

async def handler(websocket, path):
    data = await websocket.recv()
    print(f"Received message: {data}")
    await websocket.send(f"Echo: {data}")

start_server = websockets.serve(handler, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
