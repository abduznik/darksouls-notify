import tkinter as tk
import pygame
import threading
import time
from options import SOUND_PATH

class SoulNotifier:
    def __init__(self):
        pygame.mixer.init()
        
    def show_message(self, text, color):
        # Run UI in a separate thread to not block the main logic
        threading.Thread(target=self._create_overlay, args=(text, color)).start()

    def _create_overlay(self, text, color):
        root = tk.Tk()
        
        # 1. Remove window decorations (borders, title bar)
        root.overrideredirect(True)
        
        # 2. Keep on top
        root.attributes("-topmost", True)
        
        # 3. Make the background transparent
        # We set the bg to black, then tell Windows that "black" is the transparent color
        root.config(bg="black")
        root.attributes("-transparentcolor", "black")

        # 4. Geometry: Full screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")

        # 5. The Text Label
        # Note: You might need to install the font on Windows for Tkinter to see "OptimusPrinceps"
        label = tk.Label(
            root, 
            text=text, 
            font=("OptimusPrinceps", 48, "bold"), 
            fg=color, 
            bg="black"
        )
        label.place(relx=0.5, rely=0.5, anchor="center")

        # 6. Play Sound
        try:
            pygame.mixer.music.load(SOUND_PATH)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Sound error: {e}")

        # 7. Animation Sequence (Simple Flash)
        root.after(3000, root.destroy) # Destroy window after 3 seconds
        
        root.mainloop()