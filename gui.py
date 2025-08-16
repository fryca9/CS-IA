import tkinter as tk
from core.protocols.manage_protocols import ManageProtocols
from core.sessions.view_sessions import ViewSessions
from core.sessions.add_session import AddSession
class GUI:
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Main Menu")
    self.root.geometry("400x300")
    self.root.eval('tk::PlaceWindow . center')

    self.buttonframe = tk.Frame(self.root)
    self.buttonframe.columnconfigure(0, weight=1)
    self.buttonframe.columnconfigure(1, weight=1)

    self.protocol_btn = tk.Button(self.buttonframe, text="Protocol", command=lambda: ManageProtocols(self.root))
    self.protocol_btn.grid(row=0, column=0, sticky="ew")

    self.session_log_btn = tk.Button(self.buttonframe, text="Session Log", command=lambda: ViewSessions(self.root))
    self.session_log_btn.grid(row=0, column=1, sticky="ew")

    self.add_session_btn = tk.Button(self.buttonframe, text="Add Session", command=lambda: AddSession(self.root))
    self.add_session_btn.grid(row=1, column=0, columnspan=2, sticky="ew")

    self.buttonframe.pack(pady=20)
  
    self.root.mainloop()
  
  
GUI()  # Create an instance of the GUI class to run the application


# TODO find a way to move all logic related to opening and saving the session window to the SessionLog class. work on further GUI components
