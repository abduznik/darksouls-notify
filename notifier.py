import tkinter as tk
import pygame
import threading
import time
from options import SOUND_PATH

class SoulNotifier:
    def __init__(self):
        pygame.mixer.init()
        self.current_thread = None
        self.stop_event = threading.Event()

    def show_message(self, text, color):
        # 1. KILL PREVIOUS INSTANCE
        if self.current_thread and self.current_thread.is_alive():
            # Signal the running thread to stop
            self.stop_event.set()
            # Wait for it to finish cleaning up (brief blocking)
            self.current_thread.join()
            # Reset the flag for the new thread
            self.stop_event.clear()

        # 2. START NEW INSTANCE
        self.current_thread = threading.Thread(target=self._animate_sequence, args=(text, color))
        self.current_thread.start()

    def _animate_sequence(self, text, color):
        root = tk.Tk()
        
        # --- WINDOW SETUP ---
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.config(bg="black")
        root.attributes("-alpha", 0.0)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        bar_height = 180 
        y_pos = (screen_height // 2) - (bar_height // 2)
        root.geometry(f"{screen_width}x{bar_height}+0+{y_pos}")

        label = tk.Label(
            root, text=text, font=("OptimusPrinceps", 56, "bold"), 
            fg=color, bg="black", wraplength=screen_width - 100
        )
        label.place(relx=0.5, rely=0.5, anchor="center")

        # --- ANIMATION CONFIG ---
        fade_in_steps = 40
        hold_time = 0.8
        fade_out_steps = 40
        step_delay = 0.02 
        target_alpha = 0.85 

        try:
            pygame.mixer.music.load(SOUND_PATH)
            pygame.mixer.music.play(loops=-1) 
            pygame.mixer.music.set_volume(0) 
            
            # --- FADE IN LOOP ---
            for i in range(fade_in_steps + 1):
                if self.stop_event.is_set(): return # <--- Kill Check

                current_alpha = (i / fade_in_steps) * target_alpha
                root.attributes("-alpha", current_alpha)
                
                current_volume = (i / fade_in_steps) * 1.0
                pygame.mixer.music.set_volume(current_volume)
                
                root.update()
                time.sleep(step_delay)

            # --- HOLD LOOP ---
            # We break the sleep into chunks to check for 'kill' signals more often
            start_hold = time.time()
            while time.time() - start_hold < hold_time:
                if self.stop_event.is_set(): return # <--- Kill Check
                root.update()
                time.sleep(0.05) # Check every 50ms

            # --- FADE OUT LOOP ---
            for i in range(fade_out_steps, -1, -1):
                if self.stop_event.is_set(): return # <--- Kill Check

                current_alpha = (i / fade_out_steps) * target_alpha
                root.attributes("-alpha", current_alpha)
                
                current_volume = (i / fade_out_steps) * 1.0
                pygame.mixer.music.set_volume(current_volume)
                
                root.update()
                time.sleep(step_delay)

            pygame.mixer.music.stop()

        except Exception as e:
            print(f"Animation Error: {e}")
        finally:
            # Ensure window is destroyed and thread exits cleanly
            root.destroy()
            try:
                root.mainloop() # Flush final events
            except:
                pass