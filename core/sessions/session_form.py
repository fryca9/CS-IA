from core.data_manager import DataManager
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from core.helper_methods import HelperMethods as Helper

class SessionForm:
      """
    Reusable Add/Edit session form.
    - initial: dict with keys Date, Protocol, Added Weight, Total Weight, Difficulty, Completed, Notes
    - on_save: callback(values_dict) called when validation passes. Return True if saved, else False/raise.
    """
      def __init__(self, root, title, initial_data=None, on_save=None, protocol_name=None):
        self.root = root
        self.on_save = on_save
        self.initial_data = initial_data or {}
        self.data_manager = DataManager()
        self.protocol_name = protocol_name

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

            # Session Date
            tk.Label(entries_field, text="Session Date:", anchor="w", width=16).grid(
                row=0, column=0, pady=5, sticky="w"
            )
            self.session_date_entry = DateEntry(entries_field, date_pattern="yyyy-mm-dd")
            self.session_date_entry.grid(row=0, column=1, pady=5, padx=(10, 0), sticky="ew")

            # Protocol
            protocols = self.data_manager.load_protocols()
            protocol_names = Helper.get_protocol_names(protocols)
            tk.Label(entries_field, text="Protocol:", anchor="w", width=16).grid(
                row=1, column=0, pady=5, sticky="w"
            )
            self.protocol_var = tk.StringVar(value=protocol_names[0] if protocol_names else "")
            if self.protocol_name:
                self.protocol_var.set(self.protocol_name)
            protocol_menu = tk.OptionMenu(entries_field, self.protocol_var, *protocol_names)
            protocol_menu.grid(row=1, column=1, pady=5, padx=(10, 0), sticky="ew")

            # Added Weight
            tk.Label(entries_field, text="Added Weight:", anchor="w", width=16).grid(
                row=2, column=0, pady=5, sticky="w"
            )
            self.added_weight_var = tk.DoubleVar(value=0.00)
            self.added_weight_spinbox = tk.Spinbox(
                entries_field, from_=0.00, to=1000.00, increment=0.50, textvariable=self.added_weight_var, format="%.2f"
            )
            self.added_weight_spinbox.grid(row=2, column=1, pady=5, padx=(10, 0), sticky="ew")

            # Total Weight
            tk.Label(entries_field, text="Total Weight:", anchor="w", width=16).grid(
                row=3, column=0, pady=5, sticky="w"
            )
            self.total_weight_var = tk.DoubleVar(value=0.00)
            self.total_weight_spinbox = tk.Spinbox(
                entries_field, from_=0.00, to=1000.00, increment=0.50, textvariable=self.total_weight_var, format="%.2f"
            )
            self.total_weight_spinbox.grid(row=3, column=1, pady=5, padx=(10, 0), sticky="ew")

            # Difficulty
            tk.Label(entries_field, text="RPI (difficulty):", anchor="w", width=16).grid(
                row=4, column=0, pady=5, sticky="w"
            )
            self.difficulty_var = tk.IntVar(value=1)
            difficulty_spinbox = tk.Spinbox(
                entries_field, from_=1, to=10, textvariable=self.difficulty_var
            )
            difficulty_spinbox.grid(row=4, column=1, pady=5, padx=(10, 0), sticky="ew")

            # Completed
            tk.Label(entries_field, text="Completed:", anchor="w", width=16).grid(
                row=5, column=0, pady=5, sticky="w"
            )
            self.completed_var = tk.BooleanVar()
            completed_checkbox = tk.Checkbutton(entries_field, variable=self.completed_var)
            completed_checkbox.grid(row=5, column=1, pady=5, padx=(10, 0), sticky="w")

            # Notes
            tk.Label(entries_field, text="Notes:", anchor="w", width=16).grid(
                row=6, column=0, pady=5, sticky="w"
            )
            self.notes_entry = tk.Entry(entries_field)
            self.notes_entry.grid(row=6, column=1, pady=5, padx=(10, 0), sticky="ew")

            # Buttons
            buttons_field = tk.Frame(self.window)
            buttons_field.pack(padx=10, pady=10)
            buttons_field.columnconfigure(0, weight=1)
            buttons_field.columnconfigure(1, weight=1)

            tk.Button(buttons_field, text="Save", command=self.save_session).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            tk.Button(buttons_field, text="Cancel", command=self.window.destroy).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

      def populate_initial(self):
        if not self.initial_data:
            return
        try:
          self.session_date_entry.set_date(self.initial_data["Date"])
          self.protocol_var.set(self.initial_data["Protocol"])
          self.added_weight_var.set(self.initial_data["Added Weight"])
          self.total_weight_var.set(self.initial_data["Total Weight"])
          self.difficulty_var.set(self.initial_data["Difficulty"])
          self.completed_var.set(self.initial_data["Completed"])
          self.notes_entry.delete(0, tk.END)
          self.notes_entry.insert(0, self.initial_data["Notes"])
        except Exception as e:
          messagebox.showerror("Error", f"Failed to populate initial data: {e}")
          return

      def validate_inputs(self):
          errors = []

          session_date = self.session_date_entry.get_date() # if the input is invalid it adds today's date
          protocol = self.protocol_var.get() # no way to give an invalid input
          added_weight = Helper.get_float(self.added_weight_var, "Added Weight", errors)
          total_weight = Helper.get_float(self.total_weight_var, "Total Weight", errors)
          if (added_weight is not None) and (total_weight is not None):
              if total_weight < added_weight:
                  errors.append("Total Weight must be greater than or equal to Added Weight")
          difficulty = Helper.get_int(self.difficulty_var, "Difficulty", errors, min_val=1, max_val=10, restriction=True)
          completed = self.completed_var.get()
          notes = self.notes_entry.get().strip()

          entry = {
                "Date": session_date.isoformat(),
                "Protocol": protocol,
                "Added Weight": added_weight,
                "Total Weight": total_weight,
                "Difficulty": difficulty,
                "Completed": completed,
                "Notes": notes
            } 
          if "ID" in self.initial_data:
            entry["ID"] = self.initial_data["ID"]
          return errors, entry
  

      def save_session(self):
          errors, entry = self.validate_inputs()
          # Show errors if any
          if errors:
              messagebox.showerror("Invalid Input", "\n".join([f"• {e}" for e in errors]), icon="error")
              return

          # Save the session
          try:
              self.on_save(entry)
              self.window.destroy()
          except Exception as e:
              messagebox.showerror("Error", f"Failed to save session: {e}")
