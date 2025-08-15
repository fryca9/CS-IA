
from tkinter import messagebox


class HelperFunctions:
    @staticmethod
    def get_date(date_entry, errors):
        try:
            return date_entry.get_date()
        except Exception:
            errors.append("Invalid date")
            return

    @staticmethod
    def get_float(entry, name, errors, positive=True):
      val = entry.get().strip()
      if not val:
          return None
      try:
          val = float(val)
          if positive:
              if val <= 0:
                  raise ValueError
          else:
              if val < 0:
                  raise ValueError
          return val
      except Exception:
          if positive:
              errors.append(f"{name} must be a positive number")
          else:
              errors.append(f"{name} must be a non-negative number")
          return

    @staticmethod
    def get_int(entry, name, errors, min_val=1, max_val=10):
        val = entry.get()
        if not val:
            return None
        try:
            val = int(val)
            if not min_val <= val <= max_val:
                raise ValueError
            return val
        except Exception:
            errors.append(f"{name} must be an integer between {min_val} and {max_val}")
            return
