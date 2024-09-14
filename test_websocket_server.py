import unittest
from websocket import create_connection

class TestWebSocketServer(unittest.TestCase):
    def test_websocket_server_is_running(self):
        server_url = "ws://localhost:8080"
        try:
            ws = create_connection(server_url)
            self.assertTrue(ws.connected)
            ws.close()
        except Exception as e:
            self.fail(f"WebSocket server is not running or not accessible: {e}")

if __name__ == "__main__":
    unittest.main()
