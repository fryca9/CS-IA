from core.sessions.session_form import SessionForm
from core.data_manager import DataManager

class EditSession:
    def __init__(self, root, session_data, update_callback=None):
        self.data_manager = DataManager()
        self.update_callback = update_callback
        # session_data should be the JSON dict (including "ID")
        SessionForm(root, title="Edit Session", initial_data=session_data, on_save=self._on_save)

    def _on_save(self, entry):
        # entry contains updated fields and "ID"
        session_id = entry.get("ID")
        if not session_id:
            raise RuntimeError("Session ID missing for update")
        self.data_manager.update_session(session_id, entry)
        if self.update_callback:
            self.update_callback()
