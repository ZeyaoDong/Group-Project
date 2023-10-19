#
# Protocol class
#

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
            raise TypeError("For dosing method 1, no interval argument is needed")
        if duration < 0:
            raise ValueError("Time duration for dosing method 2 has to be positive")
        if duration != 0 and dosing_method == 1:
            raise TypeError("For dosing method 1, no duration argument is needed")
            

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

#Stuck my bits in here-sorry Tom

# X-axis time parametres- in this moment in time, there are no units- usually in hours

tmin = 0
tmax = 1000
tres = 100

# dosing concentrations

# Two compartment rate constant between the different compartments- numbers can be adjusted
VD1= 10
k1->2 = 1
k2->1 = 0.5
k1->0 = 2

# Initial concentration in the different compartments
C1 = 10
C2 = 0

C1(t) = C1 * np.exp(-k1->0  *  tmin)  + (k1->2 * C1/ (k2->1 - k1->0)) * (np.exp(k1->0 * t) - np.exp(-k>
C2 (t) = (k1->2 * C1/(k2->1 - k1->0)) * (np.exp(-k1->0 * tmin) - np.exp(-k2_>1 * tmin))

# Time points
t = np.linspace(0, 50, 10)  # Time point from from time point 0 to 50 with intervals of 10 between 0 a>

# Concentration-time plot
plt.title('Two compartment Pharmacokinetics Model')
plt.xlabel('Time (Hours)')
plt.ylabel('Plasma concentration')
plt.figure(t, C1, label =  'Central Compartment)
plt.figure(t, C2, label =  'Peripheral compartment)
plt.legend()
plt.figure(figsize = (10, 10)
plt.grid
plt.show

# To be modified


