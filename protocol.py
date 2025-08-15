class Protocol:
  def __init__(self):
    self.input_parameters()

  def __init__(self, protocol_name, total_sets, reps_per_set, hang_time, rest_time, rest_between_sets, delay_start):
    self.params = {
      "Protocol Name": protocol_name,
      "Total Sets": total_sets,
      "Reps Per Set": reps_per_set,
      "Hang Time": hang_time,
      "Rest Time": rest_time,
      "Rest Between Sets": rest_between_sets,
      "Delay Start": delay_start
    }

  def get_protocol_parameters(self):
    return self.params

  def validate_inputs(self, total_sets, reps_per_set, hang_time, rest_time, rest_between_sets, delay_start):
    try:
      total_sets = int(total_sets)
      reps_per_set = int(reps_per_set)
      hang_time = int(hang_time)
      rest_time = int(rest_time)
      rest_between_sets = int(rest_between_sets)
      delay_start = int(delay_start)
    except (ValueError, TypeError):
      raise ValueError("All numeric inputs must be convertible to integers.")

    if total_sets <= 0:
      raise ValueError("Total sets must be a positive integer.")
    if reps_per_set <= 0:
      raise ValueError("Reps per set must be a positive integer.")
    if hang_time < 0:
      raise ValueError("Hang time must be a non-negative integer.")
    if rest_time < 0:
      raise ValueError("Rest time must be a non-negative integer.")
    if rest_between_sets < 0:
      raise ValueError("Rest between sets must be a non-negative integer.")
    if delay_start < 0:
      raise ValueError("Delay before start must be a non-negative integer.")
    
  def input_parameters(self):
    protocol_name = input("Enter protocol name: ")
    total_sets = int(input("Enter total sets: "))
    reps_per_set = int(input("Enter reps per set: "))
    hang_time = int(input("Enter hang time (seconds): "))
    rest_time = int(input("Enter rest time (seconds): "))
    rest_between_sets = int(input("Enter rest between sets (seconds): "))
    delay_start = int(input("Enter delay before start (seconds): "))

    self.validate_inputs(total_sets, reps_per_set, hang_time, rest_time, rest_between_sets, delay_start)
    
    return Protocol(protocol_name, total_sets, reps_per_set, hang_time, rest_time, rest_between_sets, delay_start)
