import time
import random
import win32gui
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import options
from notifier import SoulNotifier

notifier = SoulNotifier()

# --- TRIGGER LOGIC ---
def try_trigger(event_type):
    config = options.NOTIFICATIONS.get(event_type)
    if not config:
        return

    # Roll the dice
    if random.random() < config["chance"]:
        print(f"Triggering: {config['text']}")
        notifier.show_message(config["text"], config["color"])

# --- EVENT HANDLERS ---

# 1. File System Handler (Detects 'Save')
class SaveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            # You can filter by file extension here (e.g., .py, .c)
            if event.src_path.endswith(".py"):
                try_trigger("save")

# 2. Window Monitor (Detects App Switches / Tab Changes)
def monitor_windows():
    last_window = ""
    while True:
        try:
            window_id = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(window_id)
            
            if window_title != last_window and window_title != "":
                last_window = window_title
                # Trigger logic based on title keywords
                if "VS Code" in window_title or "PyCharm" in window_title:
                    try_trigger("coding")
                else:
                    try_trigger("app_switch")
            
            time.sleep(0.5) # Poll every 0.5 seconds
        except Exception as e:
            print(f"Monitor error: {e}")

if __name__ == "__main__":
    print("Souls Notifier Started... Praise the Sun!")
    
    # Start File Watcher (Change path to your coding directory)
    path_to_watch = "." 
    event_handler = SaveHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)
    observer.start()

    try:
        # Run Window Monitor in main thread
        monitor_windows()
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()