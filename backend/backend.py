from streamcontroller_plugin_tools import BackendBase

from websocket_server import WebsocketServer
from loguru import logger as log


class WebsocketBackend(BackendBase):
    def __init__(self):
        super().__init__()

        self.running = False

        self.host = self.get_setting("host", "localhost")
        self.port = self.get_setting("port", 8765)
        self.start_websocket_server()
        log.debug(f"WebSocket Server has started, listening at: ws://{self.host}:{self.port}/")

    def start_websocket_server(self):
        self.ws_server = WebsocketServer(host=self.host, port=self.port)
        self.ws_server.set_fn_new_client(self.handle_new_client)
        self.ws_server.set_fn_client_left(self.handle_leave_client)
        self.ws_server.set_fn_message_received(self.handle_message_received)
        self.ws_server.run_forever(True)

    def handle_new_client(self, client, _server):
        log.debug(f"New Client ({client['id']}) has connected.")

    def handle_leave_client(self, client, _server):
        log.debug(f"Client ({client['id']}) has disconnected.")

    def handle_message_received(self, client, _server, message):
        log.debug(f"Client ({client['id']}) sent: {message}")

    def send_message(self, message : str):
        self.ws_server.send_message_to_all(message)

    def change_address(self, host : str, port : int):
        log.debug("Changing address of WebSocket server...")
        self.ws_server.shutdown_gracefully()
        self.host = host
        self.port = port
        self.start_websocket_server()
        log.debug(f"WebSocket Server started, listening at: ws://{self.host}:{self.port}/")

    def on_disconnect(self, conn):
        log.debug("WebSocket Server shutdown started...")
        self.ws_server.shutdown_gracefully()
        super().on_disconnect(conn)

    def get_setting(self, key: str, default = None):
        return self.frontend.get_settings().get(key, default)

backend = WebsocketBackend()