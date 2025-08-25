from core.data_manager import DataManager
from core.helper_methods import HelperMethods as Helper
import tkinter as tk

from core.timer.timer_logic import TimerLogic
from core.timer.timer_ui import TimerUI

class SelectProtocol:
    def __init__(self, root):
        self.root = root
        self.data_manager = DataManager()

        self.protocol_window = tk.Toplevel(root)
        self.protocol_window.title("Timer - select protocol")
        self.protocol_window.geometry("320x180")

        field = tk.Frame(self.protocol_window)
        field.pack(pady=10)
        field.columnconfigure(0, weight=1)
        field.columnconfigure(1, weight=1)

        tk.Label(field, text="Select Protocol:", anchor="e", width=16).grid(
            row=0, column=0, pady=5, padx=(0, 10), sticky="e"
        )

        protocol_names = Helper.get_protocol_names(self.data_manager.load_protocols())
        self.protocol_var = tk.StringVar(value=protocol_names[0] if protocol_names else "")
        protocol_menu = tk.OptionMenu(field, self.protocol_var, *protocol_names)
        protocol_menu.grid(row=0, column=1, pady=5, sticky="ew")

        field.grid_columnconfigure(0, weight=1)
        tk.Button(field, text="Select", command=self.protocol_selected).grid(
            row=1, column=0, columnspan=2, pady=10
        )

    def protocol_selected(self):
        """Load protocol, destroy selector, create UI + logic and wire them."""
        protocol_name = self.protocol_var.get()
        protocol = self.data_manager.get_protocol(protocol_name)
        self.protocol_window.destroy()

        # Create UI first
        timer_ui = TimerUI(self.root, protocol)
        # Create logic and pass ui to it
        timer_logic = TimerLogic(self.root, protocol, timer_ui)
        # Wire ui buttons to logic methods
        timer_ui.bind_to_logic(timer_logic)
