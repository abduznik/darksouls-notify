import time
import random
import win32gui
import keyboard 
import options

class EventManager:
    def __init__(self, notifier):
        self.notifier = notifier
        self.last_trigger_time = 0
        self.cooldown_delay = 2.0
        self.running = False

        # Global Hotkey: Triggers "Progress Saved" ONLY if active window matches list
        keyboard.add_hotkey('ctrl+s', self._on_save_pressed)

    def _on_save_pressed(self):
        """Called automatically when Ctrl+S is pressed"""
        if not self.running: return

        # 1. Get the current active window title
        try:
            window_id = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(window_id)
        except Exception:
            return # Safety catch if window handle fails

        # 2. Check if the active window is in our "Watched List"
        # We convert both to lowercase so "Notepad" matches "notepad"
        is_target_app = any(app.lower() in window_title.lower() for app in options.WATCHED_APPS)

        if is_target_app:
            self.try_trigger("save")

    def try_trigger(self, event_type):
        current_time = time.time()
        if current_time - self.last_trigger_time < self.cooldown_delay:
            return 

        config = options.NOTIFICATIONS.get(event_type)
        if not config:
            return

        if random.random() < config["chance"]:
            print(f"[Event] Triggering: {config['text']}")
            self.last_trigger_time = current_time 
            self.notifier.show_message(config["text"], config["color"])

    def start_window_monitor(self):
        """ Starts the blocking loop for window monitoring """
        print("[System] Monitoring window changes & hotkeys...")
        self.running = True
        last_window = ""
        
        try:
            while self.running:
                window_id = win32gui.GetForegroundWindow()
                window_title = win32gui.GetWindowText(window_id)
                
                if window_title != last_window and window_title != "":
                    last_window = window_title
                    
                    # Optional: Reuse the same list for "Humanity Restored" triggers?
                    # Or keep specific logic for coding apps here:
                    if "VS Code" in window_title or "PyCharm" in window_title:
                        self.try_trigger("coding")
                    else:
                        self.try_trigger("app_switch")
                
                time.sleep(0.3)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self):
        """ Clean shutdown """
        self.running = False
        keyboard.unhook_all() # Stop listening to keys
        print("\n[System] Praise the Sun! (Shutting down)")