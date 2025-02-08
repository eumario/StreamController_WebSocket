from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase
import json

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
        self.arguments = None

        self.server_ip = ""
        self.server_port = 8765
        self.server_identifier = "dev.eumario.WebSocket"
        self.server_command = ""
        self.server_args = ""


    def on_ready(self):
        self.load_config_values(False)
        return super().on_ready()

    def on_key_down(self):
        packet = {'event': "keyDown", 'identifier': self.server_identifier, 'action': self.server_command}
        if self.server_args != "":
            packet['arguments'] =  self.server_args
        self.plugin_base.backend.send_message(json.dumps(packet))

    def on_key_up(self):
        packet = {'event': "keyUp", 'identifier': self.server_identifier, 'action': self.server_command}
        if self.server_args != "":
            packet['arguments'] = self.server_args
        self.plugin_base.backend.send_message(json.dumps(packet))

    def get_config_rows(self) -> list:
        self.host = Adw.EntryRow( title = "Server Host:", show_apply_button=True)
        self.port = Adw.EntryRow( title = "Server Port:", show_apply_button=True)
        self.identifier = Adw.EntryRow( title = "Identifier:", show_apply_button=True)
        self.message = Adw.EntryRow( title = "Action:", show_apply_button=True)
        self.arguments = Adw.EntryRow( title = "Arguments:", show_apply_button=True)


        self.load_config_values()

        self.host.connect("apply", self.on_host_apply)
        self.port.connect("apply", self.on_port_apply)
        self.identifier.connect("apply", self.on_identifier_apply)
        self.message.connect("apply", self.on_message_apply)
        self.arguments.connect("apply", self.on_arguments_apply)

        return [self.host, self.port, self.identifier, self.message, self.arguments]

    def load_config_values(self, ui : bool = True):
        settings = self.get_settings()
        self.server_ip = settings.get("host","localhost")
        self.server_port = settings.get("port", 8765)
        self.server_identifier = settings.get("identifier", "dev.eumario.WebSocket")
        self.server_command = settings.get("message", "")
        self.server_args = settings.get("arguments", "")
        if ui:
            self.host.set_text(self.server_ip)
            self.port.set_text(str(self.server_port))
            self.identifier.set_text(self.server_identifier)
            self.message.set_text(self.server_command)
            self.arguments.set_text(self.server_args)

    def on_host_apply(self, _obj):
        settings = self.get_settings()
        self.server_ip = settings["host"] = self.host.get_text()
        self.set_settings(settings)
        self.backend.change_address(self.server_ip, self.server_port)

    def on_port_apply(self, _obj):
        settings = self.get_settings()
        self.server_port = settings["port"] = int(self.port.get_text())
        self.set_settings(settings)
        self.backend.change_address(self.server_ip, self.server_port)

    def on_message_apply(self, _obj):
        settings = self.get_settings()
        self.server_command = settings["message"] = self.message.get_text()
        self.set_settings(settings)

    def on_identifier_apply(self, _obj):
        settings = self.get_settings()
        self.server_identifier = settings["identifier"] = self.identifier.get_text()
        self.set_settings(settings)

    def on_arguments_apply(self, _obj):
        settings = self.get_settings()
        self.server_args = settings["arguments"] = self.arguments.get_text()
        self.set_settings(settings)