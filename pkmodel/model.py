import numpy as np
from scipy.integrate import solve_ivp
from typing import List 
from pkmodel.protocol import Dosing_Protocol  # Import the dosing protocol function from protocol.py

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


    def ODE(self, t, q, dosing_protocol, transition_constant: List[float], clearance_rate: float, volume_c: float, volume_p: List[float], absorption_constant: float):
        # check input and set attributes
        if volume_c > 0 :
             self.volume_c = float(volume_c)
        if np.all(volume_p) >0:
             self.volume_p = map(float,volume_p)
        if clearance_rate >= 0:
            self.clearance_rate = float(clearance_rate)
        else:
            raise ValueError("Clearance rate must be greater or equal to zero.")
        if  absorption_constant != None:
            if absorption_constant >= 0:
                self.absorption_constant = float(absorption_constant)
        elif  absorption_constant == None:
            self.absorption_constant = None
        else:
            raise ValueError("Absorption constant must be greater or equal to zero.")
            
        self.dosing_protocol = dosing_protocol(t)
            
        if self.dosing_type == 'Bolus':
            qc, *qp = q 
            input = dosing_protocol(t)
        elif self.dosing_type == 'Subcutaneous':
            q0, qc, *qp = q 
            input = absorption_constant * q0
        else:
            raise ValueError('We do not have this type of dosing in this library')
        
        conc_difference = [qc/volume_c - p/vp for p, vp in zip(qp, volume_p)]
        flux = [k * diff for k, diff in zip(transition_constant, conc_difference)]

        dq_dt = [0.0] * len(q)

        if self.dosing_type == 'Bolus':

            # Calculate for the central compartment
            dq_dt[0] = input - clearance_rate * qc/volume_c - np.sum(flux)

            # Calculate for the peripheral compartments
            for i in range(len(transition_constant)):
                dq_dt[i + 1] = flux[i]

        elif self.dosing_type == 'Subcutaneous':
            # Calculate for the additional compartment from which the drug is absorbed to the central c
            dq_dt[0] = dosing_protocol(t) - input
            
            # Calculate for the central compartment
            dq_dt[1] = input - clearance_rate * qc/volume_c - np.sum(flux)
            
            # Calculate for the peripheral compartments
            for i in range(len(transition_constant)):
                dq_dt[i + 2] = flux[i]
        
        return dq_dt

    def solve_ODE(self, initial_values, dosing_protocol, transition_constant, clearance_rate, volume_c, volume_p, t_span, t_eval, absorption_constant=None):
        solution = solve_ivp(
            fun=lambda t, q: self.ODE(t, q, dosing_protocol, transition_constant, clearance_rate, volume_c, volume_p, absorption_constant),
            t_span=t_span,
            y0=initial_values, 
            t_eval=t_eval)
        
        return solution.y  
        # for the 'Bolus' type: solution[0,:] represents the drug quantity in central compartments; solution[i,:] represents the drug quantity in the ith peripheral compartment.
        # for the 'Sub' type: solution[0,:] represents the drug quantity in the absorption compartment; solution[1,:] represents the drug quantity in central compartments; the other dimensions represent that in the peripheral compartments.

