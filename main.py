# Import StreamController modules

from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

import os

# Import Actions
from .actions.SendWebsocket import SendWebsocket

class PluginWebsocket(PluginBase):
    def __init__(self):
        super().__init__()

        # Launch backend
        backend_path = os.path.join(self.PATH, "backend", "backend.py")
        self.launch_backend(backend_path=backend_path, open_in_terminal=False, venv_path=os.path.join(self.PATH, "backend", ".venv"))
        self.wait_for_backend(5)

        # Register Actions
        self.send_websocket_holder = ActionHolder(
            plugin_base = self,
            action_base = SendWebsocket,
            action_id = "dev_eumario_WebSocket::SendWebsocket",
            action_name = "Send Websocket Message"
        )
        self.add_action_holder(self.send_websocket_holder)

        # Register Plugin
        self.register(
            plugin_name = "Websocket Server",
            github_repo = "https://github.com/eumario/plugin-websocket",
            plugin_version = "0.1.0",
            app_version = "1.5.0-beta6"
        )