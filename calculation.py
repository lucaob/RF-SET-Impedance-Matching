# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:36:26 2020

@author: feynman
"""

#import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pylab as plt
from mpl_toolkits import mplot3d
import numpy as np
import csv

def f(A, N, ZL, a, Delta, CJ, C):
    l = N*a               # SQUID array length in m
    R_N = coeff_R_N / A   # SQIDs room temperature tunnel resistance
                          # according to V. Ambegaokar, A. Baratoff, "Tunneling
                          # between superconductors", 1963
    RN = R_N + R_N*17/100 # SQUIDs 15 mK tunnel resistance

    tuner = SQUIDmatch(ZL, l, a, RN, Delta, CJ, A, C)
    return abs(tuner.Zres - tuner.th_Zres)


    
if __name__== "__main__":
    
    squids = 20                  # Number of SQUIDS
    ZL = 100e3                   # Impedance to be matched in ohms
    #ZL = 25.8e3                  # Impedance to be matched in ohms
    d = list(range(3, 11, 1))    # Distance between neighbouring SQUIDs in um
    Delta = 180e-6               # Superconducting gap in eV
    C = 84.3                     # cpw lineic capacitance in pF/m

    line = []
    line.append("# ZL = " + str(ZL) + " ohm" + "\n")
    line.append("# Number of SQUIDS = " + str(squids) + "\n")
    line.append("# Superconducting gap Delta = " + str(Delta) + " eV" + "\n")
    line.append("# CPW lineic capacitance = " + str(C) + " pF/m" + "\n")
                
    # Choose what oxidation do you want to consider in the calculation
    
    oxidation = 1
    
    if oxidation == 0:
        from RFSET_Matching_Optimization import SQUID_ImpedanceMatching as SQUIDmatch
        
        CJ = 4.46741e-14      # SQUID capacitance in F/um^2 according to L. Wang, "Fabrication
                              # stability of josephson junctions for superconducting qubits"
        coeff_R_N = 33.81     # SQIDs room temperature tunnel resistance
                              # according to V. Ambegaokar, A. Baratoff, "Tunneling
                              # between superconductors", 1963
        line.append("# Normal resistance at room temperature = " + str(coeff_R_N) + "/A ohm with junctin area A in um^2" + "\n")
        line.append("# Critical current = 8.47475*A uA with junctin area A in um^2" + "\n")
        line.append("# Junction capacitance = " + str(CJ) + "*A F with junctin area A in um^2" + "\n")
    else:
        from RFSET_Matching_Optimization import SQUID_ImpedanceMatching2 as SQUIDmatch
        
        CJ = 7.5e-14          # SQUID capacitance in F/um^2 according to S. V. Lotkhov, E. M. Tolkacheva,
                              # D. V. Balashov, M. I. Khabipov, F.-I. Buchholz and A. B. Zorin
                              # "Low hysteretic behavior of Al/AlOx/Al Josephson junctions"
                              # Applied Physics Letters, 89, 132115 (2006)
        coeff_R_N = 22.0      # SQIDs room temperature tunnel resistance
                              # according to the same paper
                              
        line.append("# Normal resistance at room temperature = " + str(coeff_R_N) + "/A ohm with junctin area A in um^2" + "\n")
        line.append("# Critical current = 10.0*A uA with junctin area A in um^2" + "\n")
        line.append("# Junction capacitance = " + str(CJ) + "*A F with junctin area A in um^2" + "\n")
    line.append("#\n")
    line.append("# Distance between neighbouring SQUIDs / um"+"\t"+"Junctin area / um^2"+"\t"+"IC / A"+"\t"+"Normal Resistance T amb / ohm"+"\t"+"Normal Resistance at mK / ohm"+"\t"+"Junction Capacitance / F"+"\t"+"SQUID Inductance Lj / H"+"\t"+"SQUID Array Lineic Inductance / H/m"+"\t"+"Plasma Frequency / Hz"+"\t"+"Resoance Frequency / Hz"+"\t"+"Z1 / ohm"+"\t"+"Theoretical Zres / ohm"+"\t"+"Actual Zres / ohm"+"\t"+"Theoretical Q / ohm"+"\t"+"Actual Q / ohm"+"\t"+"Minimization godness / %"+"\t"+"Minimization success"+"\n")
                
    linenumber = list(range(len(line)))

    filename = "RFSET_Matching_ox"+str(oxidation)+"_ZL"+str(ZL)+"_N"+str(squids)+".txt"
    text_file = open(filename, "w")
    for i in linenumber:
        text_file.write(line[i])
    text_file.close()
    
    junctionArea = []
    ic = []
    normalResistanceTamb = []
    normalResistance_mK = []
    junctionCapacitance = []
    SQUIDInductance = []
    SQUIDArrayLineicInductance = []
    plasmaFrequency = []
    resonanceFrequency = []
    z1 = []
    theoreticalZres = []
    actualZres = []
    theoreticalQ = []
    actualQ = []
    gd = []
    success = []
    
    # Being A the parameter of the optimization, it is in um^2 and can vary
    # betwen teh value defined in "bounds"
    for a in d:
        a = a*1e-6 # Transform the distance between neighbouring SQUIDs in m
        res = minimize_scalar(f, bounds=(0.0025, 5), args=(squids, ZL, a, Delta, CJ, C), method='bounded', options={'xatol': 1e-10, 'maxiter': 500, 'disp': 0})
        A = res.x   # Single Junctin area in um^2 coming from minimization
        junctionArea.append(A)
        
        l = squids*a     # SQUID array length in m
        R_N = coeff_R_N / A
        RN = R_N + R_N*17/100 # SQUIDs 15 mK tunnel resistance
        
        tuner = SQUIDmatch(ZL, l, a, RN, Delta, CJ, A, C)
        goodness = (abs(tuner.Zres-tuner.th_Zres)/tuner.th_Zres)*100

        if goodness < 0.035:
            success.append(True)
        else:
            success.append(False)
            
        ic.append(tuner.Ic)
        normalResistanceTamb.append(R_N)
        normalResistance_mK.append(RN)
        junctionCapacitance.append(CJ*A)
        SQUIDInductance.append(tuner.LJ)
        SQUIDArrayLineicInductance.append(tuner.L)
        plasmaFrequency.append(tuner.fp)
        resonanceFrequency.append(tuner.fn)
        z1.append(tuner.Z1)
        theoreticalZres.append(tuner.th_Zres)
        actualZres.append(tuner.Zres)
        theoreticalQ.append(tuner.th_Q)
        actualQ.append(tuner.Q)
        gd.append(goodness)
        #print("Goodness: ", a, A, goodness, "%", success)
        
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(zip(d,junctionArea,ic,normalResistanceTamb,normalResistance_mK,junctionCapacitance,SQUIDInductance,SQUIDArrayLineicInductance,plasmaFrequency,resonanceFrequency,z1,theoreticalZres,actualZres,theoreticalQ,actualQ,gd,success))
    f.close()
       
    # Make a 3D plot of Resonance Frequency vs Distance between neighbouring SQUIDs and Number of flux quanta
    
    n_flux_quanta = [x * 0.25 for x in range(0, 26)] # it's the cosine argument in the Ic equation

    resonance_vs_fluxquanta = []
    
    for a in d:
        A = junctionArea[d.index(a)]
        R_N = coeff_R_N / A
        RN = R_N + R_N*17/100
        a = a*1e-6
        l = squids*a
        
        resonance = []
        
        for flux in n_flux_quanta:
            tuner = SQUIDmatch(ZL, l, a, RN, Delta, CJ, A, C, flux_quanta=flux)
            resonance.append(tuner.fn)
        resonance_vs_fluxquanta.append(resonance)
        
    y = np.array(d)
    x = np.array(n_flux_quanta)
    
    X, Y = np.meshgrid(x, y)
    Z = np.array(resonance_vs_fluxquanta)/1e9
    
    fig = plt.figure(num=None, figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
    ax = plt.axes(projection='3d')
    #ax.contour3D(X, Y, Z, 50, cmap='binary')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_ylabel('Distance between neighbouring SQUIDs / um')
    ax.set_xlabel('Cosine argument in the Ic equation / radians')
    ax.set_zlabel('Resonance Frequency / GHz');
    ax.view_init(45, 35)
    ax.ticklabel_format(axis="z", style="plain", scilimits=(0,0))
    
    # Plot Resonance Frequency vs number of flux quanta for fixed values of the other parameters by slicing the previous 3D plot
    # at a fixed distance between neighbouring SQUIDs in um
    
    distance = 7 # chosen distance between neighbouring SQUIDs in um
    slice = d.index(distance)
    fig1 = plt.figure()
    ax1 = plt.plot(n_flux_quanta,Z[slice,:])
    plt.ylabel('Resonance Frequency / GHz')
    plt.xlabel('Cosine argument in the Ic equation / radians')