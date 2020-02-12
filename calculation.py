# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:36:26 2020

@author: feynman
"""

import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pylab as plt

# Choose what oxidation do you want to consider in the calculation

oxidation = 0

if oxidation == 0:
    from RFSET_Matching_Optimization import SQUID_ImpedanceMatching as SQUIDmatch
    
    CJ = 4.46741e-14      # SQUID capacitance in F/um^2 according to L. Wang, "Fabrication
                          # stability of josephson junctions for superconducting qubits"
    coeff_R_N = 33.81     # SQIDs room temperature tunnel resistance
                          # according to V. Ambegaokar, A. Baratoff, "Tunneling
                          # between superconductors", 1963
else:
    from RFSET_Matching_Optimization import SQUID_ImpedanceMatching2 as SQUIDmatch
    
    CJ = 7.5e-14          # SQUID capacitance in F/um^2 according to S. V. Lotkhov, E. M. Tolkacheva,
                          # D. V. Balashov, M. I. Khabipov, F.-I. Buchholz and A. B. Zorin
                          # "Low hysteretic behavior of Al/AlOx/Al Josephson junctions"
                          # Applied Physics Letters, 89, 132115 (2006)
    coeff_R_N = 22.0      # SQIDs room temperature tunnel resistance
                          # according to V. Ambegaokar, A. Baratoff, "Tunneling
                          # between superconductors", 1963

def f(A, N, ZL, a, Delta, CJ, C):
    l = N*a               # SQUID array length in m
    R_N = coeff_R_N / A   # SQIDs room temperature tunnel resistance
                          # according to V. Ambegaokar, A. Baratoff, "Tunneling
                          # between superconductors", 1963
    RN = R_N + R_N*17/100 # SQUIDs 15 mK tunnel resistance

    tuner = SQUIDmatch(ZL, l, a, RN, Delta, CJ, A, C)
    return abs(tuner.Zres - tuner.th_Zres)


### TROVARE UN MODO PER CALCOLARE LA RESISTENZA NORMALE SENZA PASSARLE
### DALL'ESTERNO COME VIENE FATTO ADESSO PERCHE' NON E' PRATICO
### PROBABILMENTE BISOGNA MODIFICARE ENTRAMBE LE CLASSI

    
if __name__== "__main__":
    
    squids = [20, 100]           # Number of SQUIDS
    ZL = 100e3                   # Impedance to be matched in ohms
    d = list(range(3, 11, 1))    # Distance between neighbouring SQUIDs in um
    Delta = 180e-6               # Superconducting gap in eV
    C = 84.3                     # cpw lineic capacitance in pF/m

    
    
    # Being A the parameter of the optimization, it is in um^2 and can vary
    # betwen teh value defined in "bounds"
    firtsResonanceFreq = []
    andamento = []
    for N in squids:
        ja = []
        resFreq = []
        junctionArea = []
        #print("!!!!!!!!!!!!!!!!!", N)
        for a in d:
            a = a*1e-6 # Transform the distance between neighbouring SQUIDs in m
            res = minimize_scalar(f, bounds=(0.0025, 5), args=(N, ZL, a, Delta, CJ, C), method='bounded', options={'xatol': 1e-10, 'maxiter': 500, 'disp': 0})
            A = res.x   # Single Junctin area in um^2 coming from minimization
            junctionArea.append(A)
            
            l = N*a     # SQUID array length in m
            R_N = 33.81 / A # SQIDs room temperature tunnel resistance
                            # according to V. Ambegaokar, A. Baratoff, "Tunneling
                            # between superconductors", 1963
            RN = R_N + R_N*17/100 # SQUIDs 15 mK tunnel resistance
            tuner = SQUIDmatch(ZL, l, a, RN, Delta, CJ, A, C)
            goodness = abs(tuner.Zres-tuner.th_Zres)/tuner.th_Zres
            success = []
            if goodness < 0.00035:
                success.append(True)
            else:
                success.append(False)
            resFreq.append(tuner.fn/1e9)
            #print("Goodness: ", a, A, goodness, "%", success)
        firtsResonanceFreq.append(resFreq)

    fig, axis = plt.subplots(1,3, squeeze = True, figsize=(10,5))
    ax = axis[0]
    ax.set_ylabel('Junction Area / um^2')
    #ax.set_xlabel('Distance between neighbouring SQUIDs / um')
    ax.plot(d, junctionArea)
    for i, N in enumerate(squids):
        ax = axis[i+1]
        ax.set_title("Number of SQUIDs = %i" %N)
        ax.set_ylabel('First rersonance Frequency / GHz')
        if i == 0:
            ax.set_xlabel('Distance between neighbouring SQUIDs / um')
        ax.plot(d, firtsResonanceFreq[i])
    fig.tight_layout()

    '''
    #Se voglio vedere i singoli valori mi basta calcolare un "tuner" passandogli i
    # valori richiesti e poi printare le singole voci
   
    print('Reference impedance =', tuner.Z0, "ohm")
    print('CPW impedance =', tuner.Z1, "ohm")
    print('Theoretical quality factor =', tuner.th_Q)
    print('SQUID inductance =', tuner.LJ, "H")
    print('SQUID lineic inductance =', tuner.L, "H")
    print('Josephson Plasma Freq =', tuner.fp/1e9, "GHz")
    print('First rersonance Freq =', tuner.fn/1e9, "GHz")
    print('Actual quality factor =', tuner.Q)
    print()
    print('Theoretical equivalent LC lamped impedance =', tuner.th_Zres, "ohm")
    print('Actual equivalent LC lamped impedance =', tuner.Zres, "ohm")
    print('Critical current =', tuner.Ic, "A")
    print('Junction AREA =', A, 'um^2')
    print('Normal Resistance at room temp. =', R_N, 'ohm')
    
    '''