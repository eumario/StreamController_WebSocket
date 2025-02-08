from streamcontroller_plugin_tools import BackendBase

from websocket_server import WebsocketServer
from loguru import logger as log


class WebsocketBackend(BackendBase):
    def __init__(self):
        super().__init__()

        self.running = False

        self.host = self.get_setting("host", "localhost")
        self.port = self.get_setting("port", 8765)
        self.server = WebsocketServer(host=self.host, port=self.port)
        self.server.set_fn_new_client(self.handle_new_client)
        self.server.set_fn_client_left(self.handle_leave_client)
        self.server.set_fn_message_received(self.handle_message_received)
        self.server.run_forever(True)
        log.debug(f"WebSocket Server has started, listening at: ws://{self.host}:{self.port}/")

    def handle_new_client(self, client, _server):
        log.debug(f"New Client ({client['id']}) has connected.")

    def handle_leave_client(self, client, _server):
        log.debug(f"Client ({client['id']}) has disconnected.")

    def handle_message_received(self, client, _server, message):
        log.debug(f"Client ({client['id']}) sent: {message}")

    def send_message(self, message : str):
        self.server.send_message_to_all(message)

    def on_disconnect(self, conn):
        #log.debug("WebSocket Server shutdown started...")
        super().on_disconnect(conn)
        self.server.shutdown_gracefully()

    def get_setting(self, key: str, default = None):
        return self.frontend.get_settings().get(key, default)

backend = WebsocketBackend()