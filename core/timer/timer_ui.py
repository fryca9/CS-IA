from core.data_manager import DataManager
import tkinter as tk
from core.helper_methods import HelperMethods as Helper
import simpleaudio as sa
from core.sessions.add_session import AddSession

class TimerUI:
    def __init__(self, root, protocol):
        self.root = root
        self.data_manager = DataManager()
        self.protocol = protocol
        
        self.window = tk.Toplevel(self.root)
        self.window.title("Timer")
        self.window.geometry("320x480")
        
        field = tk.Frame(self.window)
        field.pack(pady=5, fill="x", expand=True)
        field.columnconfigure(0, weight=1)
        field.columnconfigure(1, weight=1)

        tk.Label(field, text=f"Protocol: {self.protocol['Protocol Name']}", width=16).grid(
            row=0, column=0, columnspan=2, pady=5, sticky="ew"
        )

        self.set_label = tk.Label(field, text=f"Set: 1/{self.protocol['Total Sets']}",
                                  font=("Arial", 16), pady=5, padx=5, anchor="center")
        self.set_label.grid(row=1, column=0)

        self.rep_label = tk.Label(field, text=f"Rep: 1/{self.protocol['Reps Per Set']}",
                                  font=("Arial", 16), pady=5, padx=5, anchor="center")
        self.rep_label.grid(row=1, column=1)

        self.remaining_label = tk.Label(field, text=f"00:00", font=("Arial", 36), pady=10)
        self.remaining_label.grid(row=2, column=0, columnspan=2)

        self.timer_mode_label = tk.Label(field, text=f"PRESS START", font=("Arial", 16), pady=5)
        self.timer_mode_label.grid(row=3, column=0, columnspan=2)

        buttons_field = tk.Frame(self.window)
        buttons_field.pack(pady=10)
        for i in range(4):
            buttons_field.columnconfigure(i, weight=1)

        self.prev_btn = tk.Button(buttons_field, text="Previous")
        self.prev_btn.grid(row=0, column=0, sticky="ew")

        self.start_btn = tk.Button(buttons_field, text="Start")
        self.start_btn.grid(row=0, column=1, sticky="ew")

        self.stop_btn = tk.Button(buttons_field, text="Stop")
        self.stop_btn.grid(row=0, column=2, sticky="ew")

        self.next_btn = tk.Button(buttons_field, text="Next")
        self.next_btn.grid(row=0, column=3, sticky="ew")
        
        self.quit_btn = tk.Button(buttons_field, text="Quit", command=self.window.destroy)
        self.quit_btn.grid(row=1, column=1, columnspan=2, sticky="ew")

        self.color_field = tk.Frame(self.window, height=100)
        self.color_field.pack(fill="both", expand=True)
        self.colors = {
            "WORK": "green",
            "REST": "red",
            "REST BETWEEN SETS": "red",
            "DELAY": "orange",
            "DONE": "gray",
            "PAUSED": "yellow",
            "PRESS START": "lightgray"
        }
        self.color_field.config(bg=self.colors.get("PRESS START", "lightgray"))
        
    def bind_to_logic(self, timer_logic):
        # Bind the timer logic to the UI buttons; otherwise circular import occurs
        self.timer_logic = timer_logic
        self.start_btn.config(command=timer_logic.start_timer)
        self.stop_btn.config(command=timer_logic.stop_timer)
        self.prev_btn.config(command=timer_logic.previous_round)
        self.next_btn.config(command=timer_logic.next_round)

        # ---------- UI update ----------
    def update_labels(self, remaining, timer_mode, current_set=1, current_rep=1):
        # Update text fields based on current state. If remaining None, keep current label text.
        self.set_label.config(text=f"Set: {current_set}/{self.protocol['Total Sets']}")
        self.rep_label.config(text=f"Rep: {current_rep}/{self.protocol['Reps Per Set']}")
        self.timer_mode_label.config(text=f"{timer_mode}")

        if remaining is not None:
            self.remaining_label.config(text=f"{remaining // 60:02}:{remaining % 60:02}")
        # update color
        color = self.colors.get(timer_mode, "gray")
        self.color_field.config(bg=color)

    def schedule(self, callback, delay, *args):
        # Wrapper for after to allow easier testing/mocking
        return self.window.after(delay * 1000, callback, *args)
    
    def cancel(self, after_id):
        if after_id:
            try:
                self.window.after_cancel(after_id)
            except Exception:
                pass
    
    # helpers to change button text/commands when paused/resumed
    def set_buttons_paused_state(self):
        self.start_btn.config(text="Resume", command=self.timer_logic.resume_timer)
        self.stop_btn.config(text="Reset", command=self.timer_logic.reset_timer)

    def set_buttons_default(self):
        self.start_btn.config(text="Start", command=self.timer_logic.start_timer)
        self.stop_btn.config(text="Stop", command=self.timer_logic.stop_timer)
