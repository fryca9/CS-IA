import uuid
from timer import Timer
import json

class SessionLog:
    def add_session(self, session_date, protocol, added_weight, total_weight, difficulty, completed, notes):
        """Add a session to the session_log.json file"""
        
        entry = {
            "Date": session_date.isoformat(),
            "Protocol": protocol,
            "Added Weight": added_weight,
            "Total Weight": total_weight,
            "Difficulty": difficulty,
            "Completed": completed,
            "Notes": notes,
            "ID": str(uuid.uuid4())
        }   

        try:
            with open("session_log.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(entry)
        with open("session_log.json", "w") as f:
            json.dump(data, f, indent=2)

    def run_timer(self, protocol):
        """Run a timer session and log it"""
        timer = Timer(protocol)
        timer.operate()
        added_weight, total_weight, difficulty, completed, session_date = self.input_session_parameters()
        self.add_session(protocol, added_weight, total_weight, difficulty, completed, session_date)
        print("Session logged after running the timer.")

    def load_sessions(self, filename="session_log.json"):
        try:
            with open(filename, "r") as f:
                sessions = json.load(f)
            return sessions
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No sessions found in {filename}.")
            return []

    def print_sessions(self, filename="session_log.json"):
        sessions = self.load_sessions(filename)
        for i, session in enumerate(sessions, 1):
            print(f"Session {i}:")
            print(f"  Protocol: {session['Protocol']}")
            print(f"  Added Weight: {session['Added Weight']}")
            print(f"  Total Weight: {session['Total Weight']}")
            print(f"  Difficulty: {session['Difficulty']}")
            print(f"  Completed: {session['Completed']}")
            print(f"  Date: {session['Date']}\n")

    def clear_sessions(self, filename="session_log.json"):
        with open(filename, 'w') as f:
            f.write('')
        print(f"Cleared all sessions in {filename}.")

    
