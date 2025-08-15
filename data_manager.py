import json
import os
from tkinter import messagebox
import uuid
from datetime import date

FILENAME = "session_log.json"

class DataManager:
    """Centralised JSON read/write for sessions."""

    def __init__(self, filename=FILENAME):
        self.filename = filename

    def load_sessions(self):
        """Return a list of session dicts (safe even for missing/empty files)."""
        if not os.path.exists(self.filename):
            messagebox.showerror("Error", "Session log file not found.")
            return []
        try:
            with open(self.filename, "r") as f:
                sessions = json.load(f)
            if not isinstance(sessions, list):
                messagebox.showerror("Error", "Session log file is not in the expected format.")
                return []
            return sessions
        except (json.JSONDecodeError, ValueError):
            # file exists but is empty/invalid -> treat as no sessions
            messagebox.showerror("Error", "Failed to load sessions.")
            return []

    def save_sessions(self, sessions):
        """Save list of session dicts in the 'one entry after another' style."""
        # Make sure any non-json types (dates) are converted before saving
        with open(self.filename, "w") as f:
            json.dump(sessions, f, indent=2, default=self._json_default)

    def append_session(self, session):
        """Append a session dict. Ensures an ID exists."""
        sessions = self.load_sessions()
        if "ID" not in session:
            session["ID"] = str(uuid.uuid4())
        sessions.append(session)
        self.save_sessions(sessions)
        messagebox.showinfo("Success", "Session added successfully!")
        return session["ID"]

    def update_session(self, session_id, new_data):
        """Find session by ID and update its fields (in place). Return True if updated."""
        sessions = self.load_sessions()
        updated = False
        for s in sessions:
            if s.get("ID") == session_id:
                s.update(new_data)
                updated = True
                break
        if updated:
            self.save_sessions(sessions)
        return updated

    def delete_sessions_by_ids(self, ids):
        """Delete sessions whose 'ID' is in ids list."""
        sessions = self.load_sessions()
        sessions = [s for s in sessions if s.get("ID") not in set(ids)]
        self.save_sessions(sessions)

    @staticmethod
    def _json_default(o):
        # fallback for date objects
        if isinstance(o, date):
            return o.isoformat()
        return str(o)

# CLEAN UP THE CODE
