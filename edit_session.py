import json
import pandas as pd
from session_log import SessionLog
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import date
from helper_functions import HelperFunctions as Helper


class EditSession:
    def __init__(self, root, session_data, update_callback):
        """Open the Edit Session GUI window"""
        self.edit_session_window = tk.Toplevel(root)
        self.edit_session_window.title("Edit Session")
        self.edit_session_window.geometry("275x350")
        self.session_data = session_data
        self.update_callback = update_callback

        # Populate fields with existing session data
        self.date_entry = DateEntry(self.edit_session_window, date_pattern="yyyy-mm-dd")
        self.date_entry.set_date(session_data["Date"])

        entries_field = tk.Frame(self.edit_session_window)
        entries_field.pack(padx=10, pady=10)
        entries_field.columnconfigure(0, weight=1)
        entries_field.columnconfigure(1, weight=1)

        # Session Date
        tk.Label(entries_field, text="Session Date:", anchor="w", width=16).grid(
            row=0, column=0, pady=5, sticky="w"
        )
        self.session_date_entry = DateEntry(entries_field, date_pattern="yyyy-mm-dd")
        self.session_date_entry.set_date(session_data["Date"])
        self.session_date_entry.grid(row=0, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Protocol
        with open("protocol_manager.json", "r") as f:
            protocols = json.load(f)
        protocol_names = [p["Protocol Name"] for p in protocols]
        tk.Label(entries_field, text="Protocol:", anchor="w", width=16).grid(
            row=1, column=0, pady=5, sticky="w"
        )
        self.protocol_var = tk.StringVar(value=session_data["Protocol"])
        protocol_menu = tk.OptionMenu(entries_field, self.protocol_var, *protocol_names)
        protocol_menu.grid(row=1, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Added Weight
        tk.Label(entries_field, text="Added Weight:", anchor="w", width=16).grid(
            row=2, column=0, pady=5, sticky="w"
        )
        self.added_weight_entry = tk.Entry(entries_field)
        self.added_weight_entry.insert(0, session_data["Added Weight"])
        self.added_weight_entry.grid(row=2, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Total Weight
        tk.Label(entries_field, text="Total Weight:", anchor="w", width=16).grid(
            row=3, column=0, pady=5, sticky="w"
        )
        self.total_weight_entry = tk.Entry(entries_field)
        self.total_weight_entry.insert(0, session_data["Total Weight"])
        self.total_weight_entry.grid(row=3, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Difficulty
        tk.Label(entries_field, text="RPI (difficulty):", anchor="w", width=16).grid(
            row=4, column=0, pady=5, sticky="w"
        )
        self.difficulty_var = tk.IntVar(value=int(session_data["Difficulty"]))
        difficulty_spinbox = tk.Spinbox(
            entries_field, from_=1, to=10, textvariable=self.difficulty_var
        )
        difficulty_spinbox.grid(row=4, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Completed
        tk.Label(entries_field, text="Completed:", anchor="w", width=16).grid(
            row=5, column=0, pady=5, sticky="w"
        )
        self.completed_var = tk.BooleanVar(value=session_data["Completed"])
        completed_checkbox = tk.Checkbutton(entries_field, variable=self.completed_var)
        completed_checkbox.grid(row=5, column=1, pady=5, padx=(10, 0), sticky="w")

        # Notes
        tk.Label(entries_field, text="Notes:", anchor="w", width=16).grid(
            row=6, column=0, pady=5, sticky="w"
        )
        self.notes_entry = tk.Entry(entries_field)
        self.notes_entry.insert(0, session_data["Notes"])
        self.notes_entry.grid(row=6, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Buttons
        buttons_field = tk.Frame(self.edit_session_window)
        buttons_field.pack(padx=10, pady=10)
        buttons_field.columnconfigure(0, weight=1)
        buttons_field.columnconfigure(1, weight=1)

        tk.Button(
            buttons_field,
            text="Save",
            command=lambda: self.save_session()
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(
            buttons_field, text="Cancel", command=self.edit_session_window.destroy
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def save_session(self):
        """
        Attempt to save session; if validation fails, show errors but do NOT close window
        """
        errors = []

        session_date = Helper.get_date(self.session_date_entry, errors)
        protocol = self.protocol_var.get()
        added_weight = Helper.get_float(self.added_weight_entry, "Added Weight", errors, False)
        total_weight = Helper.get_float(self.total_weight_entry, "Total Weight", errors)
        difficulty = Helper.get_int(self.difficulty_var, "Difficulty", errors)
        completed = self.completed_var.get()
        notes = self.notes_entry.get().strip()

        # Show errors if any
        if errors:
            messagebox.showerror("Invalid Input", "\n".join([f"• {e}" for e in errors]), icon="error")
            return

        try:
            # Load all sessions
            with open("session_log.json", "r") as f:
                sessions = json.load(f)

            # Find the session by ID and update it
            for session in sessions:
                if session["ID"] == self.session_data["ID"]:
                    session.update({
                        "Date": session_date.isoformat(),
                        "Protocol": protocol,
                        "Added Weight": added_weight,
                        "Total Weight": total_weight,
                        "Difficulty": difficulty,
                        "Completed": completed,
                        "Notes": notes
                    })
                    break

            # Write back to JSON
            with open("session_log.json", "w") as f:
                json.dump(sessions, f, indent=2)
            # this format is needed to pass the arguments to update treeview
            df = pd.read_json("session_log.json")
            df["Date"] = pd.to_datetime(df["Date"]).dt.date

            # Close window and update treeview
            self.edit_session_window.destroy()
            self.update_callback(df)
            messagebox.showinfo("Success", "Session updated successfully!")  

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session: {e}")
