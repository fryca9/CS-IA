import time

class Timer:
    def __init__(self, protocol):
      self.protocol = protocol
      
    def start(self, param_name):
      print(f"Starting countdown for: {param_name}")
      remaining = self.protocol.params[param_name]
      while remaining > 0:
        print(f"Time remaining: {remaining} seconds")
        time.sleep(1)
        remaining -= 1
      print("Time's up!")
      
    def operate(self):
      self.start("Delay Start")
      for i in range(self.protocol.params["Total Sets"]):
        print(f"Starting set {i + 1} of {self.protocol.params['Total Sets']}")
        for j in range(self.protocol.params["Reps Per Set"]):
          print(f"Performing rep {j + 1} of {self.protocol.params['Reps Per Set']}")
          self.start("Hang Time")
          if j < self.protocol.params["Reps Per Set"] - 1:
            self.start("Rest Time")      
        if i < self.protocol.params["Total Sets"] - 1:
          self.start("Rest Between Sets")

    
