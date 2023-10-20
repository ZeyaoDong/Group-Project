# 2023 Software Engineering Group Project: pkmodel
Brief description: `pkmodel` is a Python library for solving Pharmacokinetic (PK) models. It allows users to specify dosing types (Bolus or Subcutaneous), dosing protocols, and customize the number of compartments to suit their needs.
-----
# Details 

## Table of contents
-[Features](#Features)
-[Installation](#Installation)
-[Usage](#Usage)
-[Contact](#Contact)


## Features
+ Supports PK models with multi-compartments
+ Outputs drug quantity over time in different compartments
+ Visualize drug quantity/concentration over time in different compartment



# Installation
Clone this repository to your own computer and then you can install `pkmodel` using pip:

```bash
cd Group-Project/
pip install ./
```
------

# Usage: 
here is an example of how to use pkmodel
```bash
import numpy as np
import matplotlib.plt as plt
from scipy.integrate import solve_ivp
from pkmodel.protocol import Dosing_Protocol
from pkmodel.model import PKModel
from pkmode.visualiser import visualize

dosing_function = Dosing_Protocol(dosing_method = 1, dose_amount = 10, interval = 0) # secify a dosing function for a step dosing of 10 ng at t = 0.

initial_values = [0.0, 0.0] # there is no drug in the body at the initial step.
t_span = (0,10)
t_eval = np.linspace(t_span[0],t_span[1],100)

model = PKModel('Bolus',1,initial_values) # use 'Bolus' dosing type, only one peripheral compartement.
print(model) # print out your model setup for check

quantity = model.solve_ODE(initial_values, dosing_function.get_dose_function(), transition_rate =  [0.1], elimination_rate = 0.1, volume_c = 1, volume_q = [1], t_span = t_span, t_eval = t_eval) # solve the equation

p =visualize(model = model, solution = quantity, t_eval = t_eval) # plot the solutions for all compartments with detailed labels
p.savefig('test_visualization.png')/p.show() #save or show this figure. 
```
### Documentation
For detailed instructions on modules and functions, please see our documentation: https://pkmodel-library.readthedocs.io/en/latest/


# Contact
For any questions, bug reports, or feature requests, feel free to contact:
+ King Ifashe, email: ifasheking@gmail.com
+ Ryan Demel, email: rdemel99@gmail.com
+ Thomas Wise, email: thomaskennedywise@outlook.com
+ Zeyao Dong, email: zeyao.dong@jesus.ox.ac.uk

------

