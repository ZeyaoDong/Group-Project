import numpy as np
import matplotlib.pyplot as plt

def visualize(model, solution, t_eval):
    #Create a list of compartment names for labeling. The first is always 'Central'.
    compartments = ['Central'] + [f'Peripheral-{i+1}' for i in range(model.p_compartmemts)]
    
    #If the dosing type is 'Subcutaneous', it means there's an extra 'Absorption' compartment.
    if model.dosing_type == 'Subcutaneous':
        compartments = ['Absorption'] + compartments  # Prepend 'Absorption' to the compartment list.

    plt.figure()
    #Loop through each compartment and plot its drug concentration over time.
    for i, comp in enumerate(compartments):
        plt.plot(t_eval, solution[i, :], label=comp)  # 'solution[i, :]' is the drug concentration data for compartment 'i'.
    
    #Set the title, labels, and legend for the plot.
    plt.title(f'Drug concentration over time ({model.dosing_type} dosing)')
    plt.xlabel('Time step')
    plt.ylabel('Drug concentration')
    plt.legend()  # Display a legend to differentiate the compartments.
    plt.grid(True)  # Add a grid for better readability of the plot.
    #plt.show()  # Display the plot.
    return plt # for users' any potential changes to this figure

