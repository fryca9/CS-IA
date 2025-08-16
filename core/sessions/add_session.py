from core.sessions.session_form import SessionForm
from core.data_manager import DataManager

class AddSession:
    def __init__(self, root, update_callback=None):
        self.data_manager = DataManager()
        self.update_callback = update_callback
        SessionForm(root, title="Add Session", initial_data=None, on_save=self._on_save)

    def _on_save(self, values):
        # values is a dict; data_manager handles IDs
        self.data_manager.append_session(values)
        if self.update_callback:
            self.update_callback()
