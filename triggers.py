import time
import random
import win32gui
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import options

class EventManager:
    def __init__(self, notifier):
        self.notifier = notifier
        self.last_trigger_time = 0
        self.cooldown_delay = 2.0  # Global cooldown in seconds
        self.observer = None

    def try_trigger(self, event_type):
        # The central brain: Checks cooldowns & probability, then notifies.

        # 1. Cooldown Check
        current_time = time.time()
        if current_time - self.last_trigger_time < self.cooldown_delay:
            return 

        config = options.NOTIFICATIONS.get(event_type)
        if not config:
            return

        # 2. Probability Check
        if random.random() < config["chance"]:
            print(f"[Event] Triggering: {config['text']}")
            self.last_trigger_time = current_time 
            self.notifier.show_message(config["text"], config["color"])

    def start_file_watch(self, path="."):
        """ Starts the background thread for file watching """
        event_handler = _SaveHandler(self.try_trigger)
        self.observer = Observer()
        self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()
        print(f"[System] Watching files in: {path}")

    def start_window_monitor(self):
        """ Starts the blocking loop for window monitoring """
        print("[System] Monitoring window changes...")
        last_window = ""
        try:
            while True:
                window_id = win32gui.GetForegroundWindow()
                window_title = win32gui.GetWindowText(window_id)
                
                if window_title != last_window and window_title != "":
                    last_window = window_title
                    
                    # Custom Logic for Window Types
                    if "VS Code" in window_title or "PyCharm" in window_title:
                        self.try_trigger("coding")
                    else:
                        self.try_trigger("app_switch")
                
                time.sleep(0.3)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """ Clean shutdown """
        if self.observer:
            self.observer.stop()
            self.observer.join()
        print("\n[System] Praise the Sun! (Shutting down)")

# --- INTERNAL HELPER CLASS ---
class _SaveHandler(FileSystemEventHandler):
    def __init__(self, callback_func):
        self.trigger_callback = callback_func

    def on_modified(self, event):
        if not event.is_directory:
            self.trigger_callback("save")