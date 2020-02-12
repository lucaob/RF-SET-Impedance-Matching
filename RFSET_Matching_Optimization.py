# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:32:11 2019

@author: feynman
"""

import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pylab as plt

class SQUID_ImpedanceMatching:
    '''
    Class that calculates impedance matcing to the reference impedance
    of a resistive load by means of a series of squid loops according to
    C. Altimiras, O. Parlavecchio, P. Joyez, D. Vion, P. Roche, D. Esteve
    and F. Portier, "Tunable microwave impedance matching to a high impedance
    source using a Josephson metamaterial", Appl. Phys. Lett, 103, 212601 (2013)
    '''
    
    def __init__(self, ZL, l, a, RN, Delta, CJ, A, C, Z0=50., n=1):
        self.Z0 = Z0 # Characteristic impedance, default 50 ohm
        
        self.Z1 = self._cpwImpedance(ZL)
        self.Ic = self._criticalCurrent(A)
        self.LJ = self._SQUID_Inductance()
        self.L = self._SQUID_LineicInductance(a) #- 30e-6
        self.fp = self._JosephsonPlasmaFreq(CJ, A)
        self.fn = self._resonanceFreq(C, l)
        self.th_Zres = self._teoreticalZres()
        self.Zres = self._actualZres(C)
        self.th_Q = self._teoreticalQ()
        self.Q = self._actualQ()
    
    def _cpwImpedance(self, ZL):
        '''
        Calculates the impedance the coplanar tuner should have to match ZL to Z0
        at the resonance frequencies f_n = (2n+1)c/4l with l = length of the  cpw
        and c = phase velocity
        --------------------------------
        Parameters:
        ZL : float Load impedance in ohm
        --------------------------------
        Returns:
        Z1 : float cpw Impedance in ohm
        '''
        Z1 = np.sqrt(ZL*self.Z0)
        return Z1
    
    def _teoreticalZres(self):
        '''
        Calculates the equivalent theoretical lamped LC circuit impedance
        --------------------------------
        Parameters:
        None
        --------------------------------
        Returns:
        Zres : float equivalent theoretical lamped LC circuit impedance on ohm
        '''
        th_Zres = 4*self.Z1/np.pi
        return th_Zres

    def _teoreticalQ(self):
        '''
        Calculates the theoretical quality factor
        --------------------------------
        Parameters:
        None
        --------------------------------
        Returns:
        th_Q : float theoretical quality factor
        '''
        th_Q = np.pi*self.Z1/(4*self.Z0)
        return th_Q
    
    def _criticalCurrent(self, A):
        '''
        Calculates the critical current of the SQUID according to INRIM
        experimental law
        --------------------------------
        Parameters:
        A : SQUID junction area in um^2
        --------------------------------
        Returns:
        Ic : float Critical current in A
        '''
        Ic = 8.47475*A*1e-6
        return Ic
    
    def _SQUID_Inductance(self):
        '''
        Calculates the inductance of the SQUID
        --------------------------------
        Parameters:
        none
        --------------------------------
        Returns:
        Lj : float SQUID inductance in H
        '''
        e = 1.602176634e-19 # Elementary charge in Coulomb
        hbar = 1.054571817e-34 # Plank Constant/2pi in J*s
        LJ = hbar/(2*e*self.Ic)
        return LJ
        
    def _SQUID_LineicInductance(self, a):
        '''
        Calculates the lineic inductance of the SQUID array
        --------------------------------
        Parameters:
        a : float Distance between neighbouring SQUIDs in m
        --------------------------------
        Returns:
        L : float SQUID array lineic inductance in H/m
        '''
        L = self.LJ/a
        return L
    
    def _JosephsonPlasmaFreq(self, CJ, A):
        '''
        Calculates the Josephson plasma frequency of the SQUID
        --------------------------------
        Parameters:
        CJ : float SQUID capacitance in F/um^2
        A  : float Single Junctin area in um^2
        --------------------------------
        Returns:
        fp : float SQUID Josephson plasma frequency
        '''
        fp = 1/(2*np.pi*np.sqrt(self.LJ*CJ*2*A))
        return fp
    
    def _resonanceFreq(self, C, l):
        '''
        Calculates the first resonance frequency of the cpw impedance adapter
        --------------------------------
        Parameters:
        C : float SQUID array lineic capacitance in pF/m
        l : float SQUID array length in m
        --------------------------------
        Returns:
        fn : float first resonance frequency of the cpw impedance adapter
        '''
        C = C*1e-12 # Convert C into F/m
        fn = 1/(2*np.pi*np.sqrt(self.L*l*C*l))
        return fn
    
    def _actualZres(self, C):
        '''
        Calculates the equivalent lamped LC circuit impedance
        --------------------------------
        Parameters:
        C : float SQUID array lineic capacitance in pF/m
        l : float SQUID array length in m
        --------------------------------
        Returns:
        Zres : float equivalent lamped LC circuit impedance on ohm
        '''
        C = C*1e-12 # Convert C into F/m
        Zres = np.sqrt(self.L/C)
        return Zres

    def _actualQ(self):
        '''
        Calculates the actual quality factor
        --------------------------------
        Parameters:
        None
        --------------------------------
        Returns:
        Q : float actual quality factor
        '''
        Z1 = np.pi*self.Zres/4
        Q = np.pi*Z1/(4*self.Z0)
        return Q

class SQUID_ImpedanceMatching2(SQUID_ImpedanceMatching): # Facendo così SQUID_ImpedanceMatching2 diventa figlia di
                                                         # SQUID_ImpedanceMatching e ne eredita tutti i metodi
    '''
    This class allow doing the same calculation as its parent, but with a different oxidation of the Junctions
    '''
    
    def __init__(self, ZL, l, a, RN, Delta, CJ, A, C, Z0=50., n=1):
        SQUID_ImpedanceMatching.__init__(self, ZL, l, a, RN, Delta, CJ, A, C, Z0=50., n=1) # In questo modo faccio
                                                                                           # tutto quello che c'è in __init__
                                                                                           # di SQUID_ImpedanceMatching
        #self.parameters = ['gamma1', 'a1'] # Posso ridefinire cose di una classe dalla classe figlia e quello
                                           # che non ridefinisco rimane com'è
                                           
    def _criticalCurrent(self, A):
        '''
        Calculates the critical current of the SQUID according to
        S. V. Lotkhov, E. M. Tolkacheva, D. V. Balashov, M. I. Khabipov, F.-I. Buchholz and A. B. Zorin
        "Low hysteretic behavior of Al/AlOx/Al Josephson junctions"
        Applied Physics Letters, 89, 132115 (2006)
        --------------------------------
        Parameters:
        A : SQUID junction area in um^2
        --------------------------------
        Returns:
        Ic : float Critical current in A
        '''
        Ic = 10*A*1e-6
        return Ic
                                           
def f(A, N, ZL, a, Delta, CJ, C):
    l = N*a               # SQUID array length in m
    R_N = 33.81 / A       # SQIDs room temperature tunnel resistance
                          # according to V. Ambegaokar, A. Baratoff, "Tunneling
                          # between superconductors", 1963
    RN = R_N + R_N*17/100 # SQUIDs 15 mK tunnel resistance
    #print(a)
    tuner = SQUID_ImpedanceMatching(ZL, l, a, RN, Delta, CJ, A, C)
    return abs(tuner.Zres - tuner.th_Zres)


### TROVARE UN MODO PER CALCOLARE LA RESISTENZA NORMALE E LA CAPACITA' DI GIUNZIONE SENZA PASSARLE
### DALL'ESTERNO COME VIENE FATTO ADESSO PERCHE' NON E' PRATICO
### PROBABILMENTE BISOGNA MODIFICARE ENTRAMBE LE CLASSI
### LA CAPACITà DI GIUNZIONE SI PUO' LASCIARE COM'E' MA, ANZICHE' PASSARLA SEMPRE DALL'ESTERNO
### SI PUO' FISSARE UN VALORE DI DEFAULT PER OGNI CLASSE, RIMANE COMUNQUE LA POSSIBILITA' DI
### PASSARLA DA FUORI
    
if __name__== "__main__":
    
    squids = [20, 100]           # Number of SQUIDS
    ZL = 100e3                   # Impedance to be matched in ohms
    #a = 5e-6                     # Distance between neighbouring SQUIDs in m
    d = list(range(3, 11, 1))    # Distance between neighbouring SQUIDs in um
    Delta = 180e-6               # Superconducting gap in eV
    CJ = 4.46741e-14             # SQUID capacitance in F/um^2 according to L. Wang, "Fabrication
                                 # stability of josephson junctions for superconducting qubits"
    C = 84.3                     # cpw lineic capacitance in pF/m
    #A = 0.5                      # Single Junctin area in um^2
    #n = 1                        # Number of resonance frequency
    
    
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
            tuner = SQUID_ImpedanceMatching(ZL, l, a, RN, Delta, CJ, A, C)
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