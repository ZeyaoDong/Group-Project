import numpy as np
from scipy.integrate import solve_ivp


class BolusModel:
    def __init__(self, number_of_p_compartments,initial_values):
        self.p_compartmemts = number_of_p_compartments
        self.initial_values = initial_values

    def __str__(self):
        return 'This is a PK model for intravenous bolus dosing with '+ f'{self.p_compartmemts} peripheral compartment(s)'

    def ODE(self, t, q, transition_rate, elimination_rate, volume_c, volume_q):
    #def ODE(self, t, transition_rate, elimination_rate, volume_c, volume_q):
        qc, *qp = q 
        dosing_protocol = 0 # get dosing protocol from another .py file
        conc_difference = [qc/volume_c - p/volume_q for p in qp] #Defining difference in concentration of drug between central compartments and all peripheral compartments
        flux = [k*diff for k, diff in zip(transition_rate, conc_difference)] #Defining flux allowing for multiple peripheral compartments 


        dq_dt = [0.0]*len(q)

        # calculate for the central compartment
        dq_dt[0] = dosing_protocol - elimination_rate*qc/volume_c - np.sum(flux)

        # calculate for the peripheral compartments
        
        for i in range(len(transition_rate)):
            dq_dt[i+1] = flux[i]
        
        
        return dq_dt
    
    # use another separat.py file to solve the ODE?
    def solve_ODE(self, initial_values, transition_rate, elimination_rate, volume_c, volume_q, t_span, t_eval):
        solution = solve_ivp(
            fun = lambda t, q: self.ODE(t,q, transition_rate, elimination_rate, volume_c, volume_q), 
            t_span = t_span,
            y0 = initial_values, 
            t_eval = t_eval)
        
        return solution.y

class SubcutaneousModel:
    def __init__(self, number_of_p_compartments):
        self.p_compartmemts = number_of_p_compartments

    def __str__(self, number_of_compartments):
        return 'This is a PK model for subcutaneous dosing with '+ f'{self.p_compartmemts} peripheral compartment(s)'
