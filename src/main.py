import sys

__version__ = "0.0.2"

if "--version" in sys.argv[1:]:
    print(f"DarkSoulsNotify {__version__}")
    sys.exit(0)

import threading
from notifier import SoulNotifier
from triggers import EventManager
from tray import SystemTray

def main_logic(manager):
    # We no longer need start_file_watch!
    # The Ctrl+S listener starts automatically when EventManager is created.
    
    # Start Monitor Loop (Blocking)
    manager.start_window_monitor()

if __name__ == "__main__":
    print("Souls Notifier Initializing...")

    notifier = SoulNotifier()
    manager = EventManager(notifier)
    
    tray = SystemTray(stop_callback=manager.stop)

    logic_thread = threading.Thread(target=main_logic, args=(manager,))
    logic_thread.start()

    tray.run() 
    
    logic_thread.join()
    print("[System] Exited cleanly.")
