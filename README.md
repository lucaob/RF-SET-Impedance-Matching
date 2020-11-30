RF-SET Impedance Matching

This project is the implementation of a Python class to design a superconductive impedace matching network to match high impedance loads (such as RF-SET, typically 100 kohm) with the low impedance of a conventional transmission line (typically 50 ohm).

The class is implemented according to:
C. Altimiras, O. Parlavecchio, P. Joyez, D. Vion, P. Roche, D. Esteve and F. Portier
"Tunable microwave impedance matching to a high impendance source using a Josephson metamaterial"
Applied Physics Letters, 103, 212601 (2013)
https://doi.org/10.1063/1.4832074

Actually there are two classes, one parent and one child, each one performs che calculation with a different oxidation of the Josephson junctions.
The parent class takes the values from the following sources:

- Junction Capacitance: L. Wang, "Fabrication stability of Josephson junctions for superconducting qubits",   Technische Universitat Munchen, 2015
- Normal Resistance: V. Ambegaokar and A. Baratoff, "Tunneling Between Superconductors", 1963
- Critical Current: fenomenological curve from our experimental data

The child class takes the falues of the same parameters from S. V. Lotkhov, E. M. Tolkacheva, D. V. Balashov, M. I. Khabipov, F.-I. Buchholz and A. B. Zorin, "Low hysteretic behavior of Al/AlOx/Al Josephson junctions", Applied Physics Letters, 89, 132115 (2006)

The script calculation.py performs the calculations by importing the two classes from the file RFSET_Matching_Optimization.py: it finds the best junction area vs distance between neighbouring SQUIDS and calculate the resonance frequency vs distance between neighbouring SQUIDS for two SQUID array lenght.

The script plots a 3D picture of the resonance frequency vs distance between neighbouring SQUIDS vs number of flux quanta and a picture of the resonance frequency vs number of flux quanta for a selected distance between neighbouring SQUIDS.

Script saves results in a text file.


