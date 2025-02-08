from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

import os
from loguru import logger as log

# Import gtk
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class SendWebsocket(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backend = self.plugin_base.backend

        self.host = None
        self.port = None
        self.identifier = None
        self.message = None

        self.server_ip = ""
        self.server_port = 8765
        self.server_identifier = "dev.eumario.WebSocket"
        self.server_message = ""


    def on_ready(self):
        self.load_config_values(False)
        if self.plugin_base.backend.running:
            self.plugin_base.backend.stop_server()

        self.plugin_base.backend.start_server(self.server_ip, self.server_port)

    def on_key_down(self):
        self.plugin_base.backend.send_message(f"{self.server_identifier} {self.server_message}")

    def get_config_rows(self) -> list:
        self.host = Adw.EntryRow()
        self.host.set_title("Server Host:")
        self.port = Adw.EntryRow()
        self.port.set_title("Server Port:")
        self.identifier = Adw.EntryRow()
        self.identifier.set_title("Identifier:")
        self.message = Adw.EntryRow()
        self.message.set_title("Socket Message:")

        self.host.set_show_apply_button(True)
        self.port.set_show_apply_button(True)
        self.identifier.set_show_apply_button(True)
        self.message.set_show_apply_button(True)

        self.load_config_values()

        self.host.connect("apply", self.on_host_apply)
        self.port.connect("apply", self.on_port_apply)
        self.identifier.connect("apply", self.on_identifier_apply)
        self.message.connect("apply", self.on_message_apply)

        return [self.host, self.port, self.message]

    def load_config_values(self, ui : bool = True):
        settings = self.get_settings()
        self.server_ip = settings.get("host","localhost")
        self.server_port = settings.get("port", 8765)
        self.server_identifier = settings.get("identifier", "dev.eumario.WebSocket")
        self.server_message = settings.get("message", "")
        if ui:
            self.host.set_text(self.server_ip)
            self.port.set_text(str(self.server_port))
            self.identifier.set_text(self.server_identifier)
            self.message.set_text(self.server_message)

    def on_host_apply(self):
        settings = self.get_settings()
        self.server_ip = settings["host"] = self.host.get_text()
        self.set_settings(settings)

    def on_port_apply(self):
        settings = self.get_settings()
        self.server_port = settings["port"] = int(self.port.get_text())
        self.set_settings(settings)

    def on_message_apply(self):
        settings = self.get_settings()
        self.server_message = settings["message"] = self.message.get_text()
        self.set_settings(settings)

    def on_identifier_apply(self):
        settings = self.get_settings()
        self.server_identifier = settings["identifier"] = self.identifier.get_text()
        self.set_settings(settings)