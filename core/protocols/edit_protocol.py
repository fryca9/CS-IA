from core.protocols.protocol_form import ProtocolForm
from core.data_manager import DataManager

class EditProtocol:
    def __init__(self, root, protocol_data, update_callback=None):
        self.data_manager = DataManager()
        self.update_callback = update_callback
        # protocol_data should be the JSON dict (including "ID")
        ProtocolForm(root, title="Edit Protocol", initial_data=protocol_data, on_save=self._on_save)

    def _on_save(self, entry):
        # entry contains updated fields and "ID"
        protocol_id = entry.get("ID")
        if not protocol_id:
            raise RuntimeError("Protocol ID missing for update")
        self.data_manager.update_protocol(protocol_id, entry)
        if self.update_callback:
            self.update_callback()
