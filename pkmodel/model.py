import numpy as np
from scipy.integrate import solve_ivp
from protocol import Dosing_Protocol
from typing import List 

class PKModel:
    def __init__(self, dosing_type, number_of_p_compartments, initial_values, dosing_protocol):
        self.dosing_type = dosing_type
        self.p_compartments = number_of_p_compartments
        self.initial_values = initial_values
        self.dosing_protocol = Dosing_Protocol(dosing_method, dose_amount, interval, duration)

        
            
    def __str__(self):
        if self.dosing_type == 'Bolus':
            if self.dosing_protocol.dosing_method == 1: 
                return f'This is a PK model for a single intravenous bolus dose with {self.p_compartments} peripheral compartment(s)'
            if self.dosing_protocol.dosing_method == 2:
                return f'This is a PK model for a multiple intravenous bolus doses over a time period self.dosing_protocol.duration with doses being administered in self.dosing_protocol.interval time intervals (in hours) with {self.p_compartments} peripheral compartment(s)'
            else:
                raise ValueError("Dosing method unspecified or invalid")
        elif self.dosing_type == 'Subcutaneous':
            if self.dosing_protocol.dosing_method == 1: 
                return f'This is a PK model for a single subcutaneous dose with {self.p_compartments} peripheral compartment(s)'
            if self.dosing_protocol.dosing_method == 2:
                return f'This is a PK model for a multiple ubcutaneous doses over a time period self.dosing_protocol.duration with doses being administered in self.dosing_protocol.interval time intervals (in hours) with {self.p_compartments} peripheral compartment(s)'
            else:
                raise ValueError("Dosing method unspecified or invalid")
        else:
            raise ValueError('We do not have this type of dosing in this library')

    def ODE(self, t: float, q: List[float], transition_constant: List[float], clearance_rate: float, volume_c: float, volume_p: List[float], absorption_constant: float):
        if volume_c > 0 :
             self.volume_c = float(volume_c)
        # Need to input the same constraint on volume_p as above but allowing for multiple values of volume_p for each compartment
        if clearance_rate >= 0:
            self.clearance_rate = float(clearance_rate)
        else:
            raise ValueError("Clearance rate must be greater or equal to zero.")
        if absorption_constant >= 0:
            self.absorption_constant = float(absorption_constant)
        else:
            raise ValueError("Absorption constant must be greater or equal to zero.")
            
        if self.dosing_type == 'Bolus':
            qc, *qp = q 
            input = self.dosing_protocol.get_dose(t)
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
            dq_dt[0] = self.dosing_protocol.get_dose(t) - input
            
            # Calculate for the central compartment
            dq_dt[1] = input - clearance_rate * qc - np.sum(flux)
            
            # Calculate for the peripheral compartments
            for i in range(len(transition_constant)):
                dq_dt[i + 2] = flux[i]
        
        return dq_dt

    def solve_ODE(self, initial_values, transition_constant, clearance_rate, volume_c, volume_p, t_span, t_eval, absorption_constant=None):
        solution = solve_ivp(
            fun=lambda t, q: self.ODE(t, q, transition_constant, clearance_rate, volume_c, volume_p, absorption_constant),
            t_span=t_span,
            y0=initial_values, 
            t_eval=t_eval)
        
        return solution.y  
        # for the 'Bolus' type: solution[0,:] represents the drug quantity in central compartments; solution[i,:] represents the drug quantity in the ith peripheral compartment.
        # for the 'Sub' type: solution[0,:] represents the drug quantity in the absorption compartment; solution[1,:] represents the drug quantity in central compartments; the other dimensions represent that in the peripheral compartments.
# These are the pharmacokinetic metrics
def calculate_Cmax(C1):
    return np.max(C1)

def calculate_Vd(C1_0, V1, Cmax):
    return (C1_0 * V1) / Cmax

def calculate_Tmax(t, C1):
    return t[np.argmax(C1)]

def calculate_Bioavailability(AUC_sub, AUC_IV):
    return AUC_sub / AUC_IV

def calculate_HalfLife(k10):
    return 0.693 / k10
