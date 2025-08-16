class HelperMethods:
    @staticmethod
    def get_float(entry, name, errors):
        try:
            val = float(entry.get())
            if val < 0:
                errors.append(f"{name} must be a non-negative number")
            return val
        except Exception:
            errors.append(f"Invalid {name} format. Must be a non-negative number")
            return None

    @staticmethod
    def get_int(entry, name, errors, min_val=1, max_val=3600, restriction=False, positive=True):
        try:
            val = int(entry.get())
            if positive and val < 1:
                errors.append(f"{name} must be a positive integer")
            if restriction and not (min_val <= val <= max_val):
                errors.append(f"{name} must be between {min_val} and {max_val}")
            return val
        except Exception:
            errors.append(f"Invalid {name} format. Must be an integer between {min_val} and {max_val}")
            return None

    @staticmethod
    def get_protocol_names(protocols):
        try:
            return [p["Protocol Name"] for p in protocols]
        except Exception:
            return []
