# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:32:11 2019

@author: feynman
"""

import numpy as np
#import matplotlib.pylab as plt

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
        self.Ic = self._criticalCurrent(Delta, RN)
        self.LJ = self._SQUID_Inductance()
        self.L = self._SQUID_LineicInductance(a) #- 30e-6
        self.fp = self._JosephsonPlasmaFreq(CJ, A)
        self.fn = self._resonanceFreq(C, l)
        self.th_Zres = self._teoreticalZres()
        self.Zres = self._actualZres(C, l)
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
    
    def _criticalCurrent(self, Delta, RN, Fi=0.):
        '''
        Calculates the critical current of the SQUID
        --------------------------------
        Parameters:
        Delta : float Superconducting gap in eV
        RN    : float SQUIDs 15 mK tunnel resistance in ohm
        Fi    : float applied external flux un Wb
        --------------------------------
        Returns:
        Ic : float Critical current in A
        '''
        e = 1.602176634e-19 # Elementary charge in Coulomb
        Fi0 = 2.067833848e-15 # Magnetic flux quantum in Wb
        Delta = Delta * e  # Convert Delta from eV to joule
        Ic = np.pi*Delta*abs(np.cos(Fi/(2*Fi0)))/(e*RN)
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
    
    def _actualZres(self, C, l):
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

        
    
if __name__== "__main__":
    ZL = 25.8e3 # Impedance to be matched in ohms
    l = 350e-6  # SQUID array length in m
    a = 5e-6    # Distance between neighbouring SQUIDs in m
    R_N = 720   # SQIDs room temperature tunnel resistance
    RN = R_N + R_N*17/100 # SQUIDs 15 mK tunnel resistance
    Delta = 180e-6  # Superconducting gap in eV
    CJ = 80e-15 # SQUID capacitance in F/um^2
    C = 84.3    # cpw lineic capacitance in pF/m
    A = 0.5     # Single Junctin area in um^2
    n = 1       # Number of resonance frequency
    
    
    tuner = SQUID_ImpedanceMatching(ZL, l, a, RN, Delta, CJ, A, C)
    print('Reference impedance =', tuner.Z0, "ohm")
    print('Theoretical equivalent LC lamped impedance =', tuner.th_Zres, "ohm")
    print('CPW impedance =', tuner.Z1, "ohm")
    print('Theoretical quality factor =', tuner.th_Q)
    print('Critical current =', tuner.Ic, "A")
    print('SQUID inductance =', tuner.LJ, "H")
    print('SQUID lineic inductance =', tuner.L, "H")
    print('Josephson Plasma Freq =', tuner.fp/1e9, "GHz")
    print('First rersonance Freq =', tuner.fn/1e9, "GHz")
    print('Actual equivalent LC lamped impedance =', tuner.Zres, "ohm")
    print('Actual quality factor =', tuner.Q)