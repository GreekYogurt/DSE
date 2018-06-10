import numpy as np

sig = 5.670373e-8 #Boltzmann constant
#https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html
alpha_alb= 0.25 #Bond albedo
q_sun = 586.2 #W/m^2
#https://www.quora.com/What-is-the-convective-heat-transfer-coefficient-at-Mars-surface
k_low = 3.482 #W/m^2/K Convective heat transfer coefficient at .5 m/s
k_high = 9.2360 #W/m^2/K At 4 m/s



#==============================================================================
#             ##Mars temperatures and solar irradiance
#==============================================================================
Q_sum = np.zeros(24)
#https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19890018252.pdf
Q_vik = [25, 130, 250, 360, 440, 500, 530, 500, 440, 360, 250, 130, 25] #Viking summertime irradiance, hourly, 6-18
Q_sum[5:18] = Q_vik
T_max = 35 #C
T_avg = -50 #deg C
T_min = -90 #deg C
T_min, T_avg, T_max =T_min + 273, T_avg + 273, T_max + 273 #Kelvin


#==============================================================================
#             ##Surface coating
#==============================================================================
eps = 0.04
alpha = 0.08
q_alb = q_sun * alpha_alb
#Q_alb = q_alb * Aeff * alpha #radiating heat albedo
#Q_ir = q_ir * Aeff * alphair #radiating heat from Mars
#Q_sun = q_sun * Aeff * alpha #radiating heat from sun    
#Q_int = 
