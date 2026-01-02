import sys
import os

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- CONFIGURATION START ---

# 1. THE LIST OF APPS
# The "Progress Saved" notification will ONLY trigger if the active 
# window title contains one of these words. (Case insensitive)
WATCHED_APPS = [
    "VS Code",
    "PyCharm",
    "Visual Studio",
    "Notepad",
    "Sublime",
    "Blender",
    "Unity",
    "Godot",
    "Word",
    "Excel"
]

# 2. NOTIFICATIONS
NOTIFICATIONS = {
    "save": {
        "text": "PROGRESS SAVED",
        "chance": 0.05, 
        "color": "#d4af37" 
    },
    "app_switch": {
        "text": "AREA DISCOVERED",
        "chance": 0.01,
        "color": "#d4af37"
    },
    "coding": {
        "text": "HUMANITY RESTORED",
        "chance": 0.2,
        "color": "#d4af37"
    },
    "error": {
        "text": "YOU DIED",
        "chance": 0.05,
        "color": "#880000" 
    }
}

FONT_PATH = get_resource_path("assets/OptimusPrinceps.ttf")
SOUND_PATH = get_resource_path("assets/new_area.mp3")