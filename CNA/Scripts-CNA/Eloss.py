############################ RiP ###################################
## Script to calculate the beam energy loss for each beam energy  ##
## deppending on the Sn film thickness                            ##
####################################################################

## --------------------------------------- ##
from include.ReadData import Material2List
## --------------------------------------- ##

def EnergyLoss(Ebeam, thickness_nm):
    """
    Calculate energy loss (keV) for a given film thickness (in nm)
    for a proton beam of given energy.

    Parameters:
    Ebeam(float): Beam energy in MeV
    thickness_nm (float): Thickness of the film in nanometers
    """

    # Load stopping power data
    energies, stopPow = Material2List('data/Sn.txt')  # units of MeV, MeV/cm

    thickness_cm = thickness_nm * 1e-7  # Convert to cm

    #print('Ebeam (MeV) \t Thickness (nm) \t Eloss (keV)\n')

    E = Ebeam
    dx = 0.0000001  # cm step size
    x = 0.
    dE_total = 0.

    while x < thickness_cm and E > min(energies):
        # Interpolate stopping power for current energy
        for i in range(len(energies) - 1):
            if energies[i] <= E <= energies[i + 1]:
                # Linear interpolation
                frac = (E - energies[i]) / (energies[i + 1] - energies[i])
                S = stopPow[i] + frac * (stopPow[i + 1] - stopPow[i])
                break
        else:
            S = stopPow[-1]  # if E < lowest data point

        dE = S * dx  # energy loss in this small step (MeV)
        dE_total += dE
        E -= dE
        x += dx

    print(f"  {Ebeam:.3f} \t {thickness_nm:.0f} \t\t\t {dE_total * 1000:.0f}")  # Convert MeV → keV

    return


## Beam energies and Sn target thicknesses
Ebeam = [3.2, 3.5, 3.9, 4.3, 4.7, 5.0]  # MeV
thickness_nm = [1368., 1353., 1283., 1226., 1585., 1640.]  # nanometers
halfThick_nm = [th / 2 for th in thickness_nm]  # half thicknesses

## Check energy loss in the full thickness of the Sn target
print(f"Energy lost in the full thickness of the Sn target:")
print('Ebeam (MeV) \t Thickness (nm) \t Eloss (keV)\n')
for i in range(len(Ebeam)):
    EnergyLoss(Ebeam[i], thickness_nm[i])

## Check energy lost in half-thickness
print(f"Energy loss in !! Half-Thickness !! of Sn target:")
print('Ebeam (MeV) \t Thickness (nm) \t Eloss (keV)\n')
for i in range(len(Ebeam)):
    EnergyLoss(Ebeam[i], halfThick_nm[i])
