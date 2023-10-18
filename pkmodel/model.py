import numpy as np
from scipy.integrate import solve_ivp


# model setup (the users can specify dosing type, the number of compartments, and the initial values of drug quantity in each compartments)
class PKModel:
    def __init__(self, dosing_type, number_of_p_compartments,initial_values):
        self.dosing_type = dosing_type
        self.p_compartmemts = number_of_p_compartments
        self.initial_values = initial_values

    # to print out the model setup to check if the library works well
    def __str__(self):
        if self.dosing_type == 'Bolus':
            return 'This is a PK model for intravenous bolus dosing with '+ f'{self.p_compartmemts} peripheral compartment(s)'
        elif self.dosing_type =='Subcutaneous': 
            return 'This is a PK model for subcutaneous dosing with '+ f'{self.p_compartmemts} peripheral compartment(s)'
        else:
            raise ValueError('We do not have this type of dosing in this libaray') # just in case the users want to solve another type of dosing

    # define the differential equation for a particular type of dosing
    def ODE(self, t, q, dosing_protocol, transition_rate, elimination_rate, volume_c, volume_q, absorbed):
        if self.dosing_type == 'Bolus':
            qc, *qp = q 
            input = dosing_protocol # input means the direct input of drug to the central compartment, it differs from 'Bolus' to 'Sub' due to an additional absorption
        elif self.dosing_type  == 'Subcutaneous':
            q0, qc, *qp = q 
            input = absorbed*q0 # as described above
        else:
            raise ValueError('We do not have this type of dosing in this libaray')

        # calculate the transition flux in each central-peripheral pair
        density_difference = [qc/volume_c - p/v_q for p, v_q in zip(qp, volume_q)]
        flux = [k*diff for k, diff in zip(transition_rate, density_difference)] 

        # create a space to store dq/dt according to the dimension (length) of q, i.e., how many compartments we need to solve at the same time
        dq_dt = [0.0]*len(q)

        # define the specific differential equations for each type of dosing
        if self.dosing_type == 'Bolus':
            # calculate for the cental compartment
            dq_dt[0] = dosing_protocol - elimination_rate*qc - np.sum(flux)

            # calculate for the peripheral compartments
            for i in range(len(transition_rate)):
                dq_dt[i+1] = flux[i]

        elif self.dosing_type  == 'Subcutaneous':
            #calculate for the additional compartment from which te drug is absrobed to the central c
            dq_dt[0] = dosing_protocol- input
            
            # calculate for the cental compartment
            dq_dt[1] = input- elimination_rate*qc - np.sum(flux)
            
            # calculate for the peripheral compartments
            for i in range(len(transition_rate)):
                dq_dt[i+2] = flux[i]
        
        return dq_dt # the dimension of the solution should be (number_of_compartments, number_of_time_steps)

    def solve_ODE(self, initial_values, dosing_protocol, transition_rate, elimination_rate, volume_c, volume_q, t_span, t_eval, absorbed = None):
        solution = solve_ivp(
            fun = lambda t, q: self.ODE(t,q, dosing_protocol, transition_rate,  elimination_rate, volume_c, volume_q, absorbed), 
            t_span = t_span,
            y0 = initial_values, 
            t_eval = t_eval)
        
        return solution.y  
        # for the 'Bolus' type: solution[0,:] represents the drug quantity in central compartments; solution[i,:] represents the drug quantity in the ith peripheral compartment.
        # for the 'Sub' type: solution[0,:] represents the drug quantity in the absorption compartment; solution[1,:] represents the drug quantity in central compartments; the other dimensions represent that in the peripheral compartments.

