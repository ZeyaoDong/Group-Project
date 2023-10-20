import numpy as np
import unittest
from pkmodel.model import PKModel
from pkmodel.protocol import Dosing_Protocol 


class Dosing_Protocol_test(unittest.TestCase):
    """
    Tests the :class:`Dosing_Protocol` class.
    """
    def test_create(self):
        """
        Tests Protocol creation
    """
        #Test Dosing_protocol with specified parameters as expected values
        protocol = Dosing_Protocol(2, 3, 4, 5)
        self.assertEqual(protocol.dosing_method, 2)
        self.assertEqual(protocol.dose_amount, 3)
        self.assertEqual(protocol.interval, 4)
        self.assertEqual(protocol.duration, 5)
        
        
        #Test Dosing_Protocol with optional parameters unspecified
        protocol = Dosing_Protocol(1)
        self.assertEqual(protocol.dose_amount, 0)
        self.assertEqual(protocol.interval, 0)
        self.assertEqual(protocol.duration, 0)
        
        #Test for expected exceptions now
        with self.assertRaises(ValueError):
            protocol = Dosing_Protocol(2, -3, 4, 5) # A negative dose amount should raise a value error.
    
        with self.assertRaises(ValueError):
            protocol = Dosing_Protocol(2, 3, -4, 5) # A negative interval time should raise a value error.
        with self.assertRaises(ValueError):
            protocol = Dosing_Protocol(2, 3, 4, -5) # A negative duration time for drug administration should raise a value error.
        with self.assertRaises(ValueError):
            protocol = Dosing_Protocol(1, 2, 3) # A non-zero interval time for dosing method 1 should raise a type error.
        with self.assertRaises(ValueError):
            protocol = Dosing_Protocol(1, 2, 0, 4) # A nonzero duration time for drug administration for dosing method 1 should raise a type error.
        with self.assertRaises(ValueError):
            protocol = Dosing_Protocol(3, 4, 5, 6) # Any value other than 1 or 2 for the dosing method should raise a value error.
    
        
        
    def test_get_dose(self):
        """
        Tests the get_dose method for different dosing methods.
        """
        # Test Dosing_protocol with dosing_method 1
        protocol = Dosing_Protocol(1, 10)  # Single, time-independent administration
        self.assertEqual(protocol.get_dose(0), 10)
        self.assertEqual(protocol.get_dose(5), 0)  # No dosing after t = 0

        # Test Dosing_protocol with dosing_method 2
        protocol = Dosing_Protocol(2, 7, 3, 10)  # Repeated administration at intervals
        # Dosing at t=0, t=3, t=6, t=9 (up to duration of 10)
        self.assertEqual(protocol.get_dose(0), 7)
        self.assertEqual(protocol.get_dose(5), 0)  # No dosing in between intervals
        self.assertEqual(protocol.get_dose(12), 0)  # No dosing after the duration

        
            
        
    
    def test_get_dose_function(self):
       """
       Tests the get_dose_function method for different dosing methods.
       """
       # Test Dosing_protocol with dosing_method 1
       protocol = Dosing_Protocol(1, 10)  # Single, time-independent administration
       dose_function = protocol.get_dose_function()
       self.assertEqual(dose_function(0), 10)
       self.assertEqual(dose_function(5), 0)

       # Test Dosing_protocol with dosing_method 2
       protocol = Dosing_Protocol(2, 7, 3, 10)  # Repeated administration at intervals
       dose_function = protocol.get_dose_function()
       self.assertEqual(dose_function(0), 7)
       self.assertEqual(dose_function(5), 0)
       self.assertEqual(dose_function(12), 0)

