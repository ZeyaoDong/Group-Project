import numpy as np
import unittest
from pkmodel.model import PKModel
from pkmodel.protocol import Dosing_Protocol 

class ModelTest(unittest.TestCase):
    def test_bolus_model(self):
        # Test a PK model with bolus dosing without dosing but with initial quantity of drug in the central compartment
        dosing_type = 'Bolus'
        num_p_compartments = 1  #  try 1 peripheral compartments
        initial_values = [1.0, 0.0]  # set: the central compartment contains 1 ng of drug at t = 0
        model = PKModel(dosing_type, num_p_compartments, initial_values)

        # Define required parameters for this testing
        dosing_function = Dosing_Protocol(dosing_method = 1, dose_amount = 0, interval = 0) # try no dosing

        transition_constant = [0.1] 
        clearance_rate = 0.05  
        volume_c = 1  
        volume_p = [1] 
        t_span = (0, 10) 
        t_eval = np.linspace(0, 10, 100) 

        # Run the ODE solver
        solution = model.solve_ODE(initial_values, dosing_function.get_dose_function(), transition_constant, clearance_rate, volume_c, volume_p, t_span, t_eval)

        self.assertTrue(np.all(solution >= 0) & np.all(solution <= 1))  # there should not be any time steps with either a negative drug quantity (non-physical) or > 1ng drug (mass conservation) 

    def test_subcutaneous_model(self):
        # Test a PK model with subcutaneous dosing
        dosing_type = 'Subcutaneous'
        num_p_compartments = 1  
        initial_values = [0.0, 1.0, 0.0]  # still try  the central compartment contains 1 ng of drug at t = 0 and there is nothing in the absorption and peripheral compartments in the beginning.
        model = PKModel(dosing_type, num_p_compartments, initial_values)

        # Define required parameters for this testing
        dosing_function = Dosing_Protocol(dosing_method = 1, dose_amount = 0, interval = 0) # try no dosing

        transition_constant = [0.1]  
        clearance_rate = 0.05 
        volume_c = 0.5
        volume_p = [0.1]
        t_span = (0, 10) 
        t_eval = np.linspace(0, 10, 100) 
        absorption_constant = 0.7

        # Run the ODE solver
        solution = model.solve_ODE(initial_values, dosing_function.get_dose_function(), transition_constant, clearance_rate, volume_c, volume_p, t_span, t_eval, absorption_constant = absorption_constant)
        
        self.assertTrue(np.all(solution >= 0) & np.all(solution <= 1))  # there should not be any time steps with either a negative drug quantity (non-physical) or > 1ng drug (mass conservation) 

