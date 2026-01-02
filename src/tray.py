import pystray
from PIL import Image
import threading
import sys
import os

class SystemTray:
    def __init__(self, stop_callback):
        self.stop_callback = stop_callback
        self.icon = None

    def get_resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            # In Development: Use the directory of THIS file (tray.py) as the anchor.
            # This ensures we look inside 'src/' regardless of where you run the command from.
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)

    def on_quit(self, icon, item):
        """ Callback for the Quit menu item """
        icon.stop()
        print("[System] Tray icon stopped.")
        # Trigger the shutdown in main logic
        self.stop_callback()

    def run(self):
        """ Creates and runs the tray icon (Blocking) """
        # Since this file is in 'src/', and assets are in 'src/assets',
        # we just ask for 'assets/icon.png'.
        image_path = self.get_resource_path("assets/icon.png")
        
        try:
            image = Image.open(image_path)
        except FileNotFoundError:
            print(f"[Error] Icon not found at {image_path}. Using default.")
            # Create a simple fallback image if file is missing
            image = Image.new('RGB', (64, 64), color = (73, 109, 137))

        menu = pystray.Menu(
            pystray.MenuItem("Quit", self.on_quit)
        )

        self.icon = pystray.Icon("DarkSoulsNotify", image, "Souls Notifier", menu)
        self.icon.run()