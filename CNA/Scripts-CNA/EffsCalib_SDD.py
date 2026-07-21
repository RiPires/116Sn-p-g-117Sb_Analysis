################################### RiP #######################################
## Script to calculate SDD detection efficiencies from the calibration runs ##
###############################################################################

## ---------------------------- ##
import os
import numpy as np
import matplotlib.pyplot as plt
from include.ReadData import *
## ---------------------------- ##

## Dictionary difining each source energies
source_energies = {
    '133Ba': [4.285, 4.619, 4.936, 30.625, 30.974, 34.964, 35.822], # keV
    '152Eu': [5.633, 6.205, 6.587, 7.178, 39.522, 40.117, 45.370, 46.578],
    '137Cs': [],
    '60Co':  [] } # keV



## Dictionary defining each source number of decays and uncertainty
source_decays = {
    '133Ba': [3.3183e6, 0.001e6], 
    '152Eu': [3.2807e6, 0.010e6]}

## Number of channels to sum on each side of the selected peak
channel_window = 5

## Dictionary to store calculated efficiencies and uncertainties by distance, source and energy
efficiencies = {}

## SDD detector path
calibPathSDD = '../Calibrations/SDD/CalibrationRuns_PosExp/'
## Loop over SDD calibration runs 
for file in os.listdir(calibPathSDD):
    if str(file).endswith('.mca'):
        name_no_ext = os.path.splitext(file)[0]
        parts = name_no_ext.split('_')
        source_name = parts[1] if len(parts) > 1 else None
        distance = next((part for part in parts if part in ['2mm', '16mm']), None)

        if source_name is None or distance is None:
            continue

        y, ch, _ = MCA2Lists(str(calibPathSDD + file))
        energies = [(ch[i]*0.031059-0.004137) for i in range(len(ch))]

        # Create nested dictionaries for this distance and source if needed
        if distance not in efficiencies:
            efficiencies[distance] = {}
        if source_name not in efficiencies[distance]:
            efficiencies[distance][source_name] = {}

        # Calculate efficiencies for each energy of the source, using a channel window
        for energy in source_energies[source_name]:
            # Find the index of the closest energy in the measured energies
            idx = int((np.abs(np.array(energies) - energy)).argmin())
            start = max(0, idx - channel_window)
            end = min(len(y), idx + channel_window + 1)
            counts = np.sum(y[start:end])
            print(distance,'\t', energy,'\t',counts)
            decay_value = source_decays[source_name][0]
            decay_uncertainty = source_decays[source_name][1]
            efficiency = counts / decay_value
            counting_error = np.sqrt(counts) / decay_value
            decay_error = efficiency * (decay_uncertainty / decay_value)
            error = np.sqrt(counting_error**2 + decay_error**2)
            efficiencies[distance][source_name][energy] = {
                'efficiency': efficiency,
                'error': error
            }

# Define the distances to plot and print
plot_distances = ['2mm', '16mm']

# Print efficiencies and energies for each distance as a dictionary
for distance in plot_distances:
    if distance not in efficiencies:
        continue

    distance_dict = {}
    for source_name, energy_values in efficiencies[distance].items():
        for energy, data in energy_values.items():
            distance_dict[float(energy)] = float(data['efficiency'])

    formatted_dict = {energy: f'{value:.3e}' for energy, value in distance_dict.items()}
    #print(f'{distance}: {formatted_dict}')

# Plot one efficiency curve per distance
plt.figure(figsize=(8, 5))

for distance in plot_distances:
    if distance not in efficiencies:
        continue

    x_values = []
    y_values = []
    y_errors = []
    for source_name, energy_values in efficiencies[distance].items():
        for energy, data in energy_values.items():
            x_values.append(float(energy))
            y_values.append(float(data['efficiency']))
            y_errors.append(float(data['error']))

    if x_values:
        x_array = np.array(x_values)
        y_array = np.array(y_values)
        yerr_array = np.array(y_errors)
        order = np.argsort(x_array)
        plt.errorbar(
            x_array[order],
            y_array[order],
            yerr=yerr_array[order],
            fmt='.-',
            capsize=3,
            elinewidth=1.2,
            label=distance
        )

plt.xlabel('Energy (keV)')
plt.ylabel('Efficiency')
plt.title('SDD efficiency curves for different source-detector distances')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()