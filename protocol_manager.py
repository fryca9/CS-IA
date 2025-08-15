
import json

class ProtocolManager:
  def add_protocol(self, protocol):
    entry = protocol.get_protocol_parameters()
    try:
      with open("protocol_manager.json", "r") as f:
        data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
      data = []
    data.append(entry)
    with open("protocol_manager.json", "w") as f:
      json.dump(data, f, indent=2)

  def remove_protocol(self, protocol):
      self.protocols.remove(protocol)

  def load_protocols(self):
    try:
      with open("protocol_manager.json", "r") as f:
        self.protocols = json.load(f)
        return self.protocols
    except (FileNotFoundError, json.JSONDecodeError):
      self.protocols = []
      return self.protocols
