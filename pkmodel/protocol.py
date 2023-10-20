
class Dosing_Protocol:
    def __init__(self, dosing_method, dose_amount=0, interval=0, duration=0):
        self.dosing_method = dosing_method
        self.dose_amount = dose_amount
        self.interval = interval
        self.duration = duration
        if dose_amount < 0:
            raise ValueError("Dose_amount must be positive")
        if interval < 0:
            raise ValueError("Time interval for drug adminitration must be positive")
        if interval != 0 and dosing_method == 1:
            raise ValueError("For dosing method 1, no interval argument is needed")
        if duration < 0:
            raise ValueError("Time duration for dosing method 2 has to be positive")
        if duration != 0 and dosing_method == 1:
            raise ValueError("For dosing method 1, no duration argument is needed")
        if dosing_method != 1 and dosing_method != 2:
            raise ValueError("Invalid dosing method")

    def get_dose(self, t):
        if self.dosing_method == 1:
            # Single, time-independent administration
            if t == 0:
                return self.dose_amount
            else:
                return 0

        elif self.dosing_method == 2:
            # Repeated administration at equal intervals
            if t < self.duration:
                if t % self.interval == 0:
                    return self.dose_amount
                else:
                    return 0
            else:
                return 0

        else:
            raise ValueError("Invalid dosing method")

    def get_dose_function(self):
        if self.dosing_method == 1:
            # Single, time-independent administration
            return lambda t: self.get_dose(t)

        elif self.dosing_method == 2:
            # Repeated administration at equal intervals
            return lambda t: self.get_dose(t)

        else:
            raise ValueError("Invalid dosing method")

