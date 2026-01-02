from notifier import SoulNotifier
from triggers import EventManager

if __name__ == "__main__":
    print("Souls Notifier Initializing...")

    # 1. Initialize the GUI/Audio system
    notifier = SoulNotifier()

    # 2. Initialize the Logic Manager
    manager = EventManager(notifier)

    # 3. Start Background Tasks
    # You can change "." to any specific path like "C:/Coding"
    manager.start_file_watch(".") 

    # 4. Start Main Loop (Blocking)
    manager.start_window_monitor()