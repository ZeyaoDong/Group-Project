import numpy as np
from scipy.integrate import solve_ivp
from protocol import Dosing_Protocol  # Import the dosing protocol function from protocol.py

class PKModel:
    def __init__(self, dosing_type, number_of_p_compartments,initial_values):
        self.dosing_type = dosing_type
        self.p_compartmemts = number_of_p_compartments
        self.initial_values = initial_values

    def __str__(self):
        if self.dosing_type == 'Bolus':
            return 'This is a PK model for intravenous bolus dosing with '+ f'{self.p_compartmemts} peripheral compartment(s)'
        elif self.dosing_type =='Subcutaneous': 
            return 'This is a PK model for subcutaneous dosing with '+ f'{self.p_compartmemts} peripheral compartment(s)'
        else:
            raise ValueError('We do not have this type of dosing in this libaray')

    def ODE(self, t, q, dosing_protocol, transition_rate, elimination_rate, volume_c, volume_q, absorbed):
        if self.dosing_type == 'Bolus':
            qc, *qp = q 
            input = dosing_protocol(t)
        elif self.dosing_type  == 'Subcutaneous':
            q0, qc, *qp = q 
            input = absorbed*q0
        else:
            raise ValueError('We do not have this type of dosing in this libaray')
        
        density_difference = [qc/volume_c - p/v_q for p, v_q in zip(qp,volume_q)]
        flux = [k*diff for k, diff in zip(transition_rate, density_difference)]

        dq_dt = [0.0]*len(q)

        if self.dosing_type == 'Bolus':
            # calculate for the cental compartment
            dq_dt[0] = input - elimination_rate*qc - np.sum(flux)

            # calculate for the peripheral compartments
        
            for i in range(len(transition_rate)):
                dq_dt[i+1] = flux[i]

        elif self.dosing_type  == 'Subcutaneous':
            #calculate for the additional compartment from which te drug is absrobed to the central c
            dq_dt[0] = dosing_protocol(t)- input
            # calculate for the cental compartment
            dq_dt[1] = input- elimination_rate*qc - np.sum(flux)
            # calculate for the peripheral compartments
        
            for i in range(len(transition_rate)):
                dq_dt[i+2] = flux[i]
        
        return dq_dt
    
    # use another separat.py file to solve the ODE?
    def solve_ODE(self, initial_values, dosing_protocol, transition_rate, elimination_rate, volume_c, volume_q, t_span, t_eval, absorbed = None):
        solution = solve_ivp(
            fun = lambda t, q: self.ODE(t,q, dosing_protocol, transition_rate,  elimination_rate, volume_c, volume_q, absorbed), 
            t_span = t_span,
            y0 = initial_values, 
            t_eval = t_eval)
        
        return solution.y  
        # for the 'Bolus' type: solution[0,:] represents the drug quantity in central compartments; solution[i,:] represents the drug quantity in the ith peripheral compartment.
        # for the 'Sub' type: solution[0,:] represents the drug quantity in the absorption compartment; solution[1,:] represents the drug quantity in central compartments; the other dimensions represent that in the peripheral compartments.

