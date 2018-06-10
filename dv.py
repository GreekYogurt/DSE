import numpy as np
#Gravitational parameters
muE = 3.98600436233E+14 
muS = 1.32712440040944E+20
muM = 4.2828375214E+13 
AU = 149597870700 #m
#Velocity around Earth at LEO
#r_LEO = 24582.*1000
r_LEO = (6378+200)*1000.
V_LEO = np.sqrt(muE/r_LEO)

#Velocity around Mars at LMO (125)
r_LMO = (3390 + 125)*1000. #assuming 125 km circular orbit
V_LMO = np.sqrt(muM/r_LMO)

#Velocities around Sun
r_E = 1 * AU
V_E = np.sqrt(muS/r_E) #At Earth
r_M = 1.524 * AU
V_M = np.sqrt(muS/r_M) #At Mars
a_tr = (r_E + r_M)/2. #semi-major axis for transfer orbit

#Heliocentric velocities
#At departure position
V1_helio = np.sqrt(muS * (2. / r_E - 1 / a_tr)) #heliocentric velocity at LEO
#At target position
V2_helio = np.sqrt(muS * (2 / r_M - 1 / a_tr)) #heliocentric at Mars

#Excess velocities
#At departure
V1_inf = np.abs(V1_helio-V_E)
#At target
V2_inf = np.abs(V2_helio-V_M)

#Velocity in pericenter of hyperbola
#At departure
V_0 = np.sqrt(2*muE/r_LEO + V1_inf**2)
#At target
V_1 = np.sqrt(2*muM/r_LMO + V2_inf**2)

#Maneuvers
#In pericenter around Earth
DV0 = np.abs(V_0 - V_LEO)
#In pericenter around Mars
DV1 = np.abs(V_1 - V_LMO)
DVtot = DV0 + DV1 + V_LEO + 2000
print 'Delta V needed', DVtot