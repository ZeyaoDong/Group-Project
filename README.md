# 2023 Software Engineering Group Project: pkmodel
Brief description: `pkmodel` is a Python library for solving Pharmacokinetic (PK) models. It allows users to specify dosing types (Bolus or Subcutaneous), dosing protocols, and customize the number of compartments to suit their needs.
-----
# Details

##Table of contents
-[pkmodel.PKModel]
-[pkmodel.PKModel.ODE]
-[visualiser]
-[Features]
-[Installation]
-[Contact]


## pkmodel.PKModel(dosing_type, number_of_p_compartments,initial_values)
You can specify the basic form of a PK model by defining the type of dosing (Bolus or Subscutaneous), the number of peripheral compartments which have two-side transitions with the central compartment, and the initial quantity of drug in each compartments including the central, peripheral compartments (for 'Subscutaneous', also include the initial quantity in the absorption part)
Caution: the input of initial values should be a list. For 'Bolus' dosing, the first value should represent the initial quantity in the central compartment, the other should represent the peripheral compartments. For 'Subscutaneous' dosing, the first value should represent the initial quantity in the part from which the drug is absorbed to the central compartment, the second value should represent the central one, and the other should represent the peripheral ones. 


## pkmodel.PKModel.ODE(t, q, *args)
Here you can specify the parameters contained in a PK model, including protocol, transition rate between the central and peripheral compartments, elimination rate, the volume of each compartments, absorption rate to the central compartment for 'Subscutaneous' type. The protocol function is imported from another module called pkmodel.protocol.Dosing_Protocol() where you can specify either a step dosing at the initial time step or dosing at several time steps with a fixed time interval, and the amount of dosing. 

It will return the time derivatives of each compartment.

## pkmodel.PKModel.solve_ODE(*args)
This is used to solve the PK model you just defined. The solution will have a dimension of (the number of all compartments, the number of time steps). In the first dimension (solution[i,:]), you can see the temporal changes of drug quantity in each compartment in the same order of your input of initial values.

## visualiser
The visuliser.py file is a separate python file for visulisation. It can be imported as a function in this library. The required inputs include the defined PK model, the corresponding solutions, and time. 
It will return 'plt' which allows the users to further change the configuration of this figure for any specific needs.

##Features
Supports one-compartment and two-compartment models
Outputs drug concentration over time in different compartments
Can be used to calculate the following variables:
+ Maximum cooncentration- Cmax
+ Time to reach Cmax
+ Minimum concentration- Cmin
+ Volume of distribution
+ CLearance at steady state- CLss
+ Bioavailability- F
+ Steady state concentration- Css


# Installation
You can install `pkmodel` using pip:

```bash
pip install pkmodel
```
------

# Usage: here is an example of how to use pkmodel
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


# Contact
For any questions, bug reports, or feature requests, feel free to contact the project maintainer:
Name:
Email Address:
------

