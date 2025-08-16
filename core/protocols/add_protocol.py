from core.protocols.protocol_form import ProtocolForm
from core.data_manager import DataManager

class AddProtocol:
    def __init__(self, root, update_callback=None):
        self.data_manager = DataManager()
        self.update_callback = update_callback
        ProtocolForm(root, title="Add Protocol", initial_data=None, on_save=self._on_save)

    def _on_save(self, values):
        # values is a dict; data_manager handles IDs
        self.data_manager.append_protocol(values)
        if self.update_callback:
            self.update_callback()
