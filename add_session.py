import json
from session_log import SessionLog
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import date


class AddSession:
    def __init__(self, root):
        """Open the Add Session GUI window"""
        add_session_window = tk.Toplevel(root)
        add_session_window.title("Add Session")
        add_session_window.geometry("275x350")

        entries_field = tk.Frame(add_session_window)
        entries_field.pack(padx=10, pady=10)
        entries_field.columnconfigure(0, weight=1)
        entries_field.columnconfigure(1, weight=1)

        # Session Date
        tk.Label(entries_field, text="Session Date:", anchor="w", width=15).grid(
            row=0, column=0, pady=5, sticky="w"
        )
        session_date_entry = DateEntry(entries_field, date_pattern="yyyy-mm-dd")
        session_date_entry.grid(row=0, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Protocol
        with open("protocol_manager.json", "r") as f:
            protocols = json.load(f)
        protocol_names = [p["Protocol Name"] for p in protocols]
        tk.Label(entries_field, text="Protocol:", anchor="w", width=20).grid(
            row=1, column=0, pady=5, sticky="w"
        )
        protocol_var = tk.StringVar(value=protocol_names[0] if protocol_names else "")
        protocol_menu = tk.OptionMenu(entries_field, protocol_var, *protocol_names)
        protocol_menu.grid(row=1, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Added Weight
        tk.Label(entries_field, text="Added Weight:", anchor="w", width=16).grid(
            row=2, column=0, pady=5, sticky="w"
        )
        added_weight_entry = tk.Entry(entries_field)
        added_weight_entry.grid(row=2, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Total Weight
        tk.Label(entries_field, text="Total Weight:", anchor="w", width=16).grid(
            row=3, column=0, pady=5, sticky="w"
        )
        total_weight_entry = tk.Entry(entries_field)
        total_weight_entry.grid(row=3, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Difficulty
        tk.Label(entries_field, text="RPI (difficulty):", anchor="w", width=16).grid(
            row=4, column=0, pady=5, sticky="w"
        )
        difficulty_var = tk.IntVar(value=1)
        difficulty_spinbox = tk.Spinbox(
            entries_field, from_=1, to=10, textvariable=difficulty_var
        )
        difficulty_spinbox.grid(row=4, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Completed
        tk.Label(entries_field, text="Completed:", anchor="w", width=16).grid(
            row=5, column=0, pady=5, sticky="w"
        )
        completed_var = tk.BooleanVar()
        completed_checkbox = tk.Checkbutton(entries_field, variable=completed_var)
        completed_checkbox.grid(row=5, column=1, pady=5, padx=(10, 0), sticky="w")

        # Notes
        tk.Label(entries_field, text="Notes:", anchor="w", width=16).grid(
            row=6, column=0, pady=5, sticky="w"
        )
        notes_entry = tk.Entry(entries_field)
        notes_entry.grid(row=6, column=1, pady=5, padx=(10, 0), sticky="ew")

        # Buttons
        buttons_field = tk.Frame(add_session_window)
        buttons_field.pack(padx=10, pady=10)
        buttons_field.columnconfigure(0, weight=1)
        buttons_field.columnconfigure(1, weight=1)

        tk.Button(
            buttons_field,
            text="Save",
            command=lambda: self.try_save_session(
                session_date_entry,
                protocol_var,
                added_weight_entry,
                total_weight_entry,
                difficulty_var,
                completed_var,
                notes_entry,
                add_session_window,
            ),
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(
            buttons_field, text="Cancel", command=add_session_window.destroy
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def try_save_session(
        self,
        session_date_entry,
        protocol_var,
        added_weight_entry,
        total_weight_entry,
        difficulty_var,
        completed_var,
        notes_entry,
        window,
    ):
        """
        Attempt to save session; if validation fails, show errors but do NOT close window
        """
        errors = []

        # Session Date
        session_date_str = session_date_entry.get()
        try:
            session_date = date.fromisoformat(session_date_str)
        except Exception:
            errors.append("Session date must be in YYYY-MM-DD format")

        # Protocol
        protocol = protocol_var.get()
        if not isinstance(protocol, str) or not protocol.strip():
            errors.append("Please select a valid protocol")

        # Added Weight
        try:
            added_weight = float(added_weight_entry.get())
            if added_weight < 0:
                raise ValueError
        except Exception:
            errors.append("Added weight must be a non-negative number")

        # Total Weight
        try:
            total_weight = float(total_weight_entry.get())
            if total_weight < 0:
                raise ValueError
        except Exception:
            errors.append("Total weight must be a non-negative number")

        # Difficulty
        try:
            difficulty = int(difficulty_var.get())
            if not 1 <= difficulty <= 10:
                raise ValueError
        except Exception:
            errors.append("Difficulty must be an integer between 1 and 10")

        # Completed
        completed = completed_var.get()
        if not isinstance(completed, bool):
            errors.append("Completed must be True or False")

        # Notes
        notes = notes_entry.get()
        if not isinstance(notes, str):
            errors.append("Notes must be a string")

        if errors:
            # Convert errors into bullet points
            error_message = "\n".join([f"• {e}" for e in errors])
            messagebox.showerror("Invalid Input", error_message, icon="error")
            return  # Do NOT close window; let user fix inputs

        # All validations passed
        SessionLog().add_session(
            session_date,
            protocol,
            added_weight,
            total_weight,
            difficulty,
            completed,
            notes,
        )
        messagebox.showinfo("Success", "Session saved successfully!")
        window.destroy()
