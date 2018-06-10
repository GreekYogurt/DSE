# -*- coding: utf-8 -*-
"""
Created on Wed May 09 17:24:35 2018

@author: Robbert
"""
from math import *
import numpy as np
import matplotlib.pyplot as plt

#vol = 524.
#t = 12.7E-6
#m = 7.4
#pl = 3.0
#r = (vol/(4*pi()/3))**(1/3)
#rho = m/(4*pi()*r**2 * t)
#
##mass per m^3
#
#
#def mskin(rb):
#    return rho*t*4*pi()*rb**2

def Cd(Re):
    a = 24./Re
    b = (2.6*0.2*Re)/(1.+(.2*Re)**1.52)
    c = (.411*(Re/(2.63*10**-5))**(-7.94))/(1.+(Re/(2.63*10**-5))**(-8.00))
    d = (0.25*Re*10**-6)/(1.+Re*10**-6)
    return a+b+c+d

Re = 300000.
V = np.arange(0., 30., 0.1)
d = 70.

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

def D(V, d):
    return Cd(300000)*0.5*rho_mars(7000.)*V*V*0.25*pi*d**2

def P(D, V):
    return D(V,d)*V

for i in range(1,7):
    print 'V:', 5*i, 'Drag:', round(D(5*i,d),2), 'N', 'Power:', round(D(5*i,d)*5*i,2), 'W'

plt.plot(V, D(V,d))
plt.plot(V, P(D,V))
plt.xlabel('Velocity [m/s]')
plt.ylim(0,500)
plt.ylabel('Drag [N] / Power [W]')
plt.show()