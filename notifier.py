import tkinter as tk
import pygame
import threading
import time
from options import SOUND_PATH

class SoulNotifier:
    def __init__(self):
        pygame.mixer.init()
        
    def show_message(self, text, color):
        threading.Thread(target=self._animate_sequence, args=(text, color)).start()

    def _animate_sequence(self, text, color):
        root = tk.Tk()
        
        # --- 1. WINDOW SETUP ---
        root.overrideredirect(True) # Remove title bar
        root.attributes("-topmost", True) # Keep on top
        root.config(bg="black") # The bar color
        
        # Start invisible (Alpha 0)
        root.attributes("-alpha", 0.0)

        # --- 2. GEOMETRY (THE BLACK BAR) ---
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        bar_height = 180 
        y_pos = (screen_height // 2) - (bar_height // 2)
        root.geometry(f"{screen_width}x{bar_height}+0+{y_pos}")

        # --- 3. THE TEXT ---
        label = tk.Label(
            root, 
            text=text, 
            font=("OptimusPrinceps", 56, "bold"), 
            fg=color, 
            bg="black",
            wraplength=screen_width - 100
        )
        label.place(relx=0.5, rely=0.5, anchor="center")

        # --- 4. ANIMATION CONFIG ---
        fade_in_steps = 50
        hold_time = 0.5 
        fade_out_steps = 40
        step_delay = 0.02 
        target_alpha = 0.85 

        # --- 5. EXECUTION ---
        try:
            # AUDIO FADE IN SETUP
            pygame.mixer.music.load(SOUND_PATH)
            pygame.mixer.music.play() 
            pygame.mixer.music.set_volume(0) 
            
            # --- FADE IN LOOP ---
            for i in range(fade_in_steps + 1):
                # Visual Alpha
                current_alpha = (i / fade_in_steps) * target_alpha
                root.attributes("-alpha", current_alpha)
                
                # Audio Volume (0.0 to 1.0)
                current_volume = (i / fade_in_steps) * 1.0
                pygame.mixer.music.set_volume(current_volume)
                
                root.update()
                time.sleep(step_delay)

            # --- HOLD ---
            time.sleep(hold_time)

            # --- FADE OUT LOOP (FIXED) ---
            # We removed the generic fadeout() call. 
            # We now manually lower volume inside the loop to sync with visuals.
            
            for i in range(fade_out_steps, -1, -1):
                # Visual Alpha
                current_alpha = (i / fade_out_steps) * target_alpha
                root.attributes("-alpha", current_alpha)
                
                # Audio Volume (Syncs exactly with opacity)
                current_volume = (i / fade_out_steps) * 1.0
                pygame.mixer.music.set_volume(current_volume)
                
                root.update()
                time.sleep(step_delay)

        except Exception as e:
            print(f"Animation Error: {e}")
        finally:
            # Clean up
            root.destroy()
            try:
                # Pump generic events one last time to prevent ghost windows
                root.update_idletasks() 
            except:
                pass