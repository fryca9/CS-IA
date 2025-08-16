from core.data_manager import DataManager
import tkinter as tk
from tkinter import messagebox
from core.helper_methods import HelperMethods as Helper

class ProtocolForm:
    """
    Reusable Add/Edit protocol form.
    - initial: dict with keys Date, Protocol, Added Weight, Total Weight, Difficulty, Completed, Notes
    - on_save: callback(values_dict) called when validation passes. Return True if saved, else False/raise.
    """
    def __init__(self, root, title, initial_data=None, on_save=None):
        self.root = root
        self.on_save = on_save
        self.initial_data = initial_data or {}
        self.data_manager = DataManager()

        self.window = tk.Toplevel(root)
        self.window.title(title)
        self.window.geometry("320x380")
        self.build_UI()
        self.populate_initial()

    def build_UI(self):
        entries_field = tk.Frame(self.window)
        entries_field.pack(padx=10, pady=10)
        entries_field.columnconfigure(0, weight=1)
        entries_field.columnconfigure(1, weight=1)

        # Protocol Name
        tk.Label(entries_field, text="Protocol Name:", anchor="w", width=16).grid(
            row=0, column=0, pady=5, sticky="w"
        )
        self.protocol_name_entry = tk.Entry(entries_field)
        self.protocol_name_entry.grid(row=0, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Total Sets
        tk.Label(entries_field, text="Total Sets:", anchor="w", width=16).grid(
            row=1, column=0, pady=5, sticky="w"
        )
        self.total_sets_var = tk.IntVar(value=1)
        self.total_sets_spinbox = tk.Spinbox(
            entries_field, from_=1, to=100, textvariable=self.total_sets_var
        )
        self.total_sets_spinbox.grid(row=1, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Reps Per Set
        tk.Label(entries_field, text="Reps Per Set:", anchor="w", width=16).grid(
            row=2, column=0, pady=5, sticky="w"
        )
        self.reps_per_set_var = tk.IntVar(value=1)
        self.reps_per_set_spinbox = tk.Spinbox(
            entries_field, from_=1, to=100, textvariable=self.reps_per_set_var
        )
        self.reps_per_set_spinbox.grid(row=2, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Hang Time
        tk.Label(entries_field, text="Hang Time:", anchor="w", width=16).grid(
            row=3, column=0, pady=5, sticky="w"
        )
        self.hang_time_var = tk.IntVar(value=1)
        self.hang_time_spinbox = tk.Spinbox(
            entries_field, from_=1, to=3600, textvariable=self.hang_time_var
        )
        self.hang_time_spinbox.grid(row=3, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Rest Time
        tk.Label(entries_field, text="Rest Time:", anchor="w", width=16).grid(
            row=4, column=0, pady=5, sticky="w"
        )
        self.rest_time_var = tk.IntVar(value=1)
        self.rest_time_spinbox = tk.Spinbox(
            entries_field, from_=1, to=3600, textvariable=self.rest_time_var
        )
        self.rest_time_spinbox.grid(row=4, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Rest Between Sets
        tk.Label(entries_field, text="Rest Between Sets:", anchor="w", width=16).grid(
            row=5, column=0, pady=5, sticky="w"
        )
        self.rest_between_sets_var = tk.IntVar(value=1)
        self.rest_between_sets_spinbox = tk.Spinbox(
            entries_field, from_=1, to=3600, textvariable=self.rest_between_sets_var
        )
        self.rest_between_sets_spinbox.grid(row=5, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Delay Start
        tk.Label(entries_field, text="Delay Start:", anchor="w", width=16).grid(
            row=6, column=0, pady=5, sticky="w"
        )
        self.delay_start_var = tk.IntVar(value=1)
        self.delay_start_spinbox = tk.Spinbox(
            entries_field, from_=1, to=3600, textvariable=self.delay_start_var
        )
        self.delay_start_spinbox.grid(row=6, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Notes
        tk.Label(entries_field, text="Notes:", anchor="w", width=16).grid(
            row=7, column=0, pady=5, sticky="w"
        )
        self.notes_entry = tk.Entry(entries_field)
        self.notes_entry.grid(row=7, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Buttons
        buttons_field = tk.Frame(self.window)
        buttons_field.pack(padx=10, pady=10)
        buttons_field.columnconfigure(0, weight=1)
        buttons_field.columnconfigure(1, weight=1)

        tk.Button(buttons_field, text="Save", command=self.save_protocol).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(buttons_field, text="Cancel", command=self.window.destroy).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def populate_initial(self):
        if not self.initial_data:
            return
        try:
          self.protocol_name_entry.insert(0, self.initial_data["Protocol Name"])
          self.total_sets_var.set(self.initial_data["Total Sets"])
          self.reps_per_set_var.set(self.initial_data["Reps Per Set"])
          self.hang_time_var.set(self.initial_data["Hang Time"])
          self.rest_time_var.set(self.initial_data["Rest Time"])
          self.rest_between_sets_var.set(self.initial_data["Rest Between Sets"])
          self.delay_start_var.set(self.initial_data["Delay Start"])
          self.notes_entry.insert(0, self.initial_data["Notes"])
        except Exception as e:
          messagebox.showerror("Error", f"Failed to populate initial data: {e}")
          return

    def validate_inputs(self):
          errors = []

          protocol = self.protocol_name_entry.get().strip()
          if not protocol:
              errors.append("Protocol Name is required")
          total_sets = Helper.get_int(self.total_sets_var, "Total Sets", errors)
          reps_per_set = Helper.get_int(self.reps_per_set_var, "Reps Per Set", errors)
          hang_time = Helper.get_int(self.hang_time_var, "Hang Time", errors)
          rest_time = Helper.get_int(self.rest_time_var, "Rest Time", errors)
          rest_between_sets = Helper.get_int(self.rest_between_sets_var, "Rest Between Sets", errors)
          delay_start = Helper.get_int(self.delay_start_var, "Delay Start", errors)
          notes = self.notes_entry.get().strip()

          entry = {
                "Protocol Name": protocol,
                "Total Sets": total_sets,
                "Reps Per Set": reps_per_set,
                "Hang Time": hang_time,
                "Rest Time": rest_time,
                "Rest Between Sets": rest_between_sets,
                "Delay Start": delay_start,
                "Notes": notes
            }
          if "ID" in self.initial_data:
            entry["ID"] = self.initial_data["ID"]
          return errors, entry
  

    def save_protocol(self):
          errors, entry = self.validate_inputs()
          # Show errors if any
          if errors:
              messagebox.showerror("Invalid Input", "\n".join([f"• {e}" for e in errors]), icon="error")
              return

          # Save the protocol
          try:
              self.on_save(entry)
              self.window.destroy()
          except Exception as e:
              messagebox.showerror("Error", f"Failed to save protocol: {e}")
