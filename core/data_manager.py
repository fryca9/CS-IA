import json
from tkinter import messagebox
import uuid
from datetime import date

FILENAME_SESSIONS = "data/session_log.json"
FILENAME_PROTOCOLS = "data/protocol_manager.json"

class DataManager:
    """Centralised JSON read/write for sessions."""

    def __init__(self, sessions_filename=FILENAME_SESSIONS, protocol_filename=FILENAME_PROTOCOLS):
        self.sessions_filename = sessions_filename
        self.protocol_filename = protocol_filename

    def load_sessions(self):
        """Return a list of session dicts (safe even for missing/empty files)."""
        try:
            with open(self.sessions_filename, "r") as f:
                sessions = json.load(f)
            return sessions
        except (FileNotFoundError, json.JSONDecodeError):
            # file exists but is empty/invalid -> treat as no sessions
            return []

    def load_protocols(self):
        """Load protocols from the protocol manager JSON file."""
        try:
            with open(self.protocol_filename, "r") as f:
                protocols = json.load(f)
            return protocols
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_sessions(self, sessions):
        """Save list of session dicts in the 'one entry after another' style."""
        # Make sure any non-json types (dates) are converted before saving
        with open(self.sessions_filename, "w") as f:
            json.dump(sessions, f, indent=2, default=self._json_default)
    
    def save_protocols(self, protocols):
        """Save protocols to the protocol manager JSON file."""
        with open(self.protocol_filename, "w") as f:
            json.dump(protocols, f, indent=2)

    def append_session(self, session):
        """Append a session dict. Ensures an ID exists."""
        sessions = self.load_sessions()
        if "ID" not in session:
            session["ID"] = str(uuid.uuid4())
        sessions.append(session)
        self.save_sessions(sessions)
        messagebox.showinfo("Success", "Session added successfully!")
        return session["ID"]
    
    def append_protocol(self, protocol):
        """Append a protocol dict. Ensures an ID exists."""
        protocols = self.load_protocols()
        if "ID" not in protocol:
            protocol["ID"] = str(uuid.uuid4())
        protocols.append(protocol)
        self.save_protocols(protocols)
        messagebox.showinfo("Success", "Protocol added successfully!")
        return protocol["ID"]

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

    def update_protocol(self, protocol_id, new_data):
        """Find protocol by ID and update its fields (in place). Return True if updated."""
        protocols = self.load_protocols()
        updated = False
        for p in protocols:
            if p.get("ID") == protocol_id:
                p.update(new_data)
                updated = True
                break
        if updated:
            self.save_protocols(protocols)
        return updated

    def delete_sessions_by_ids(self, ids):
        """Delete sessions whose 'ID' is in ids list."""
        sessions = self.load_sessions()
        sessions = [s for s in sessions if s.get("ID") not in set(ids)]
        self.save_sessions(sessions)

    def delete_protocols_by_ids(self, ids):
        """Delete protocols whose 'ID' is in ids list."""
        protocols = self.load_protocols()
        protocols = [p for p in protocols if p.get("ID") not in set(ids)]
        self.save_protocols(protocols)

    @staticmethod
    def _json_default(o):
        # fallback for date objects
        if isinstance(o, date):
            return o.isoformat()
        return str(o)
