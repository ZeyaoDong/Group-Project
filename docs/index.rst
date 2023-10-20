.. PKmodel-library documentation master file, created by
   sphinx-quickstart on Fri Oct 20 11:38:11 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pkmodel Library Documentation
============================

Brief Description
-----------------

`pkmodel` is a Python library designed for solving Pharmacokinetic (PK) models. It provides a flexible framework that allows users to specify dosing types (Bolus or Subcutaneous), dosing protocols, and customize the number of compartments to suit their needs.

PKModel Class
--------------

The core component of `pkmodel` is the `PKModel` class, which allows you to define and solve PK models.

pkmodel.PKModel(dosing_type, number_of_p_compartments, initial_values)
~~~~~~~~~~~~~~~~~~~~~~~

You can create a PK model by instantiating the `PKModel` class. This class constructor takes the following parameters:

- `dosing_type`: Specify the type of dosing (Bolus or Subcutaneous).
- `number_of_p_compartments`: Customize the number of peripheral compartments.
- `initial_values`: Provide initial drug quantities in each compartment, including the central and peripheral compartments.

**Caution**: The `initial_values` parameter should be a list. For 'Bolus' dosing, the first value should represent the initial quantity in the central compartment, and the rest should represent the peripheral compartments. For 'Subcutaneous' dosing, the first value should represent the initial quantity in the absorption part, the second value the central compartment, and the rest the peripheral compartments.

pkmodel.PKModel.ODE(t, q, *args)
~~~~~~~~~~~~~~~~~~~~~~~~

Once you've created a PK model, you can specify the parameters that define the PK model and obtain the time derivatives of each compartment.

- `t`: Time.
- `q`: Drug quantities in compartments.
- `*args`: Parameters for the PK model, including protocol, transition rates, elimination rates, compartment volumes, and the absorption rate for 'Subcutaneous' type dosing which is set to be None for 'Bolus'.

The protocol function is imported from another module called `protocol`, where you can specify the dosing method, time steps, and dosing amounts. See Section protocol for more details.

pkmodel.PKModel.solve_ODE(*args)
~~~~~~~~~~~~~~~~~~~~~~~~

To solve the PK model, use the `solve_ODE` method. It returns a solution with dimensions `(number_of_compartments, number_of_time_steps)`. In the first dimension (`solution[i, :]`), you can observe the temporal changes in drug quantity in each compartment, corresponding to the order of your initial values.



protocol
----------
The `protocol` module is for specifying dosing protocols.

- `dosing_method`:  dosing_method == 1 'Single, time-independent administration', dosing_method == 2 'Repeated administration at equal intervals'.
- `dose_amount`: the quantity of drug you want to dose.
- `interval`: default = 0, only valid to be an integer for dosing_method == 2, defining the time interval for repeated administration
- `duration`: default = 0, only valid to be an integer for dosing_method == 2, defining the time span for repeated administration

The input to set up and solve a PKModel can be obtained by calling a sub-defined function `.get_dose_function()`, which is a function of dosing quantity with time.


Visualizer
----------

The `visualizer` module, located in `visuliser.py`, is a separate Python file for visualization purposes. You can import it as a function within the `pkmodel` library. The required inputs include the defined PK model, the corresponding solutions, and time.

The `visualizer` function returns a `plt` object, allowing users to further customize the figure configuration for specific needs.

For more information or if you have any questions, please feel free to contact us.





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
