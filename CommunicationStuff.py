import numpy as np
        ###Tables generator
        ###sheizze man
        ###Mars parameters
mu = 4.282837e13   
R_mars = 3390*1000 #km
def TOrbital(r_p, r_a):
    #calculates orbital period of satellite, insert in km
    #returns in seconds
    r_p +=R_mars
    r_a +=R_mars
    r_p *=1000
    r_a *=1000
    
    a = (r_p+r_a)/2
    return 2*np.pi* np.sqrt(a**3/mu)
a_sat = 400000
DegToRad = np.pi/180
e_min = 5*DegToRad #deg, from SMAD, minimum elevation for contact
rho = np.arcsin(R_mars/(R_mars + a_sat)) #rad, angular radius of Mars seen by sat
n_max = np.arcsin(np.sin(rho) * np.cos(e_min)) #max Mars nadir angle
lam_max = 90*DegToRad - e_min - n_max #maximum nadir angle, rad
D_max = R_mars * np.sin(lam_max)/np.sin(n_max) #Max range
