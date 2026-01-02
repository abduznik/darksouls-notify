import tkinter as tk
import pygame
import threading
import time
import ctypes
import os
from options import SOUND_PATH, FONT_PATH # Make sure FONT_PATH is imported or defined

class SoulNotifier:
    def __init__(self):
        pygame.mixer.init()
        self.current_thread = None
        self.stop_event = threading.Event()
        
        # --- NEW: LOAD FONT FROM FILE ---
        self.load_custom_font(FONT_PATH)

    def load_custom_font(self, font_path):
        """ 
        Loads a font file (.ttf) into memory so Tkinter can use it 
        without installation. Windows only.
        """
        if not os.path.exists(font_path):
            print(f"[Warning] Font file not found: {font_path}")
            return

        # Uses Windows GDI to register the font privately for this process
        # 0x10 = FR_PRIVATE (Only this app can see the font)
        # 0x0  = Reserved
        try:
            ctypes.windll.gdi32.AddFontResourceExW(os.path.abspath(font_path), 0x10, 0)
        except Exception as e:
            print(f"Error loading font: {e}")

    def show_message(self, text, color):
        if self.current_thread and self.current_thread.is_alive():
            self.stop_event.set()
            self.current_thread.join()
            self.stop_event.clear()

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

        # --- FONT USAGE ---
        # Note: Even though we load the FILE, we must refer to the font by its
        # INTERNAL FAMILY NAME. For OptimusPrinceps.ttf, the family name is usually
        # just "OptimusPrinceps".
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
                if self.stop_event.is_set(): return 

                current_alpha = (i / fade_in_steps) * target_alpha
                root.attributes("-alpha", current_alpha)
                
                current_volume = (i / fade_in_steps) * 1.0
                pygame.mixer.music.set_volume(current_volume)
                
                root.update()
                time.sleep(step_delay)

            # --- HOLD LOOP ---
            start_hold = time.time()
            while time.time() - start_hold < hold_time:
                if self.stop_event.is_set(): return 
                root.update()
                time.sleep(0.05) 

            # --- FADE OUT LOOP ---
            for i in range(fade_out_steps, -1, -1):
                if self.stop_event.is_set(): return 

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
            root.destroy()
            try:
                root.mainloop() 
            except:
                pass