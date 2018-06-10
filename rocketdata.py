#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
#def p_mars(alt):
#    return 699*np.exp(-0.009*alt)
#
#
#def T_mars(alt): 
#    return 242.15 - 0.0009*alt
#
#
#def rho_mars(alt):
#    p = p_mars(alt)
#    T = T_mars(alt)
#    return p/192.1/T
g_mars = 3.71
def T_mars(h):
    if h<7000:
        return -23.4 - 0.00222 * h + 273.15
    else:
        return -31 - 0.000998 * h + 273.15
def p_mars(h):
    #return pressure in Pa
    return 0.699 * np.exp(-0.00009*h)*1000
def rho_mars(h):
    #return density in kg/m^3
    p = p_mars(h)/1000. #use KPa
    T = T_mars(h)
    rho = p / (.1921 * (T))
    return rho
def vol(h, T_ball):
    #Calculate volume of balloon to lift 1 kg of PL
    #Input altitude and temp of baloon
    rho_atm = rho_mars(h)    
    R_he = 2077. #Helium gas constant
    rho_gas = p_mars(h)/R_he/T_ball
    V = 1/(rho_atm - rho_gas)
    return V, rho_gas
def vol_mat(vol_bal,t):
    A = 4*np.pi*((3./4/np.pi*vol_bal)**0.333)**2
    return t*A
def r_fromball(V):
    r = (3./4/np.pi*V)**0.3333
    return r
# Ligher than air

#rho_gas = p_mars(alt)/R_helium/T_mars(alt)

#Q = mass/(rho_atm - rho_gas)

#print 'Blimp calcs !..!,'
##print 'Everythign per kilogram of payload mass'
#print 'Volume m^3', Q
#print 'Gas density kg/m^3', rho_gas
#print 'Atmospheric density kg/m^3', rho_atm
#print'Temperature', T_mars(alt)
#print 'Pressure', p_mars(alt)
#print 'Cube length', Q**0.3333333
#print 'Helium weight', Q*rho_gas
Hlist, Vlist = [], []
for h in np.arange(0000,20000,500):
    T_ball = T_mars(h)
    V_perkg, rho_h =vol(h, T_ball)
    print 'H', h,'[m], V/m',V_perkg , '[m^3/kg], M_He/m_pl', rho_h*V_perkg
    Hlist.append(h)
    Vlist.append(V_perkg*2000)
h = 500  #m, set altitude
m_pl = 50 #kg, base station mass
V_perkg, rho_g = vol(h, T_mars(h))
V_ball = V_perkg*m_pl #m^3, spherical baloon volume
M_he = m_pl * rho_g #kg
r = r_fromball(V_ball) #m, radius of baloon
t_ball = 11e-6 #11 micrometer thickness
V_mat = vol_mat(V_ball, t_ball) #m^3 balloon skin volume 
rho_mat = 1370 #kg/m^3 polyester density
m_mat = V_mat * 1370 #kg
print "With a base station of", m_pl,"kg, at",h, "km altitude, need a baloon volume of", V_ball, 'm^3 and a helium mass of', M_he ,'kg'
print 'This requires baloon radius of', r, 'at a thickness of', t_ball, 'need a material volume of', V_mat, 'm^3, leading to a balloon skin mass of', m_mat, 'kg'
# sources
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html
# https://www.grc.nasa.gov/WWW/K-12/rocket/atmosmrm.html
#plt.plot(Hlist, Vlist)
#plt.ylabel('Volume')
#plt.xlabel('Height')
#plt.show()
