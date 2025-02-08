import asyncio, websockets

from streamcontroller_plugin_tools import BackendBase
from loguru import logger as log
from websockets import WebSocketServerProtocol


class WebsocketBackend(BackendBase):
    def __init__(self):
        super().__init__()

        self.clients = set()
        self.running = False
        self.socket = None

        host = self.get_setting("host", "localhost")
        port = self.get_setting("port", 8765)

        self.start_websocket_server(host, port)


    async def handler(self, websocket : WebSocketServerProtocol, path : str):
        self.clients.add(websocket)
        log.debug(f"Accepted connection from {websocket}")
        try:
            async for message in websocket:
                log.debug(f"WebSocket Received: {message}")
        except websockets.exceptions.ConnectionClosed as e:
            log.debug(f"Client Disconnected: {e}")
        finally:
            self.clients.remove(websocket)

    async def start_server_async(self, host : str = "localhost", port : int = 8765):
        self.running = True
        self.socket = await websockets.serve(self.handler, host, port)
        log.info(f"Starting WebSocket server at ws://{host}:{port}/")
        await self.socket.wait_closed()

    def start_websocket_server(self, host : str = "localhost", port : int = 8765):
        asyncio.run(self.start_server_async(host, port))

    def stop_server(self):
        self.running = False
        self.socket.close()

    def send_message(self, message):
        for client in self.clients:
            try:
                client.send(message)
            except websockets.exceptions.ConnectionClosed:
                self.clients.remove(client)

    def on_disconnect(self, conn):
        log.debug("Shutting Down Server...")
        self.stop_server()
        log.debug("Server shutdown.")
        super().on_disconnect(conn)

    def get_setting(self, key: str, default = None):
        return self.frontend.get_settings().get(key, default)

backend = WebsocketBackend()