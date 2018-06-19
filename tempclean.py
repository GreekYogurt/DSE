import numpy as np
import matplotlib.pyplot as plt
def A_rad(Q_req, T_rad):
    #Returns the required radiator area based on the power it must output and its temperature
    eps_rad = 0.78
    A = Q_req/ (eps_rad * T_rad**4 * sigma)
    return A
def SurfaceArea(dim):
    #Calculates surface area of a rectangular component
    W = dim[0]
    H = dim[1]
    L = dim[2]
    return W*H*2 + W*L*2 + W*L * 2
def TempBox(Q_rad, Q_int, q_UAV, A_box, A_box_exp):
    ###Calculates equilibrium temp of a box!
    eps_box = 0.03 #7 layer MLI, https://app.knovel.com/web/view/khtml/show.v/rcid:kpSTCHVFT2/cid:kt007RIOO4/viewerType:khtml/root_slug:spacecraft-thermal-control/url_slug:blanket-design-requirements?&b-toc-cid=kpSTCHVFT2&b-toc-url-slug=radiator-effectiveness&b-toc-title=Spacecraft%20Thermal%20Control%20Handbook%2C%20Volume%201%20-%20Fundamental%20Technologies%20(2nd%20Edition)&page=6&view=collapsed&zoom=1&q=kg
    if A_box == A_boxUAV:
        base = 0
        eps_box_exp = 0.7 #White pain, SMAD
    elif A_box == A_boxBASE:
        base = 1
        eps_box_exp = 0.92 #Also white paint, SMAD
    alpha_box = 0.17
    if Q_rad + Q_int + q_UAV * A_box * alpha_box>0 and base == 0:
        T_box = ((Q_rad + Q_int + q_UAV * A_box * alpha_box)/(2* sigma * (eps_box_exp * A_box_exp + eps_box* (A_box - A_box_exp))))**0.25
    elif Q_rad + Q_int + q_UAV * A_box * alpha_box>0 and base == 1:
        T_box = ((Q_rad + Q_int + q_UAV * A_box * alpha_box)/(sigma * (eps_box_exp * A_box_exp + eps_box* (A_box - A_box_exp))))**0.25

    else:
        T_box = 6000
    return T_box
def EqTemp(eps, alpha, Q_int, q_sun, A_top, A_bot, q_ir):
    ####New equilibrium temperature calculator
    #Oututs the equilibrium temperature in K, plus the radiated heat and the internal heat used
    #Input stuff in SI units
    #Assumes 50% heat lost due to convection
#    eps = 0.04 #vapor deposited aluminium
#    alpha = 0.2 #BOL, vapor deposited aluminium, SMAD
    Q_sun = q_sun * A_top * alpha
    Q_IR = q_ir * A_bot * alpha
    Q_rad = (Q_IR + Q_sun + Q_int)/2
    T_eq = (1/2 * (Q_int + Q_sun + Q_IR)/(eps * sigma * (A_top + A_bot)))**0.25
    return T_eq, [Q_rad, Q_int]
def minheat(QT):
    QT = np.array(QT)
    i = np.where(np.abs(QT[:,0])==np.min(np.abs(QT[:,0])))
    return QT[i][0]
sigma = 5.670373e-8 #Boltzmann constant
#https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html
            ###Temperature model
#https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19890018252.pdf
q_vik_sum = [25, 130, 250, 360, 440, 500, 530, 500, 440, 360, 250, 130, 25] #Viking summertime irradiance, hourly, 6-18
q_vik_win = [10, 45, 90, 140, 170, 180, 170, 140, 90, 45, 10]
q_sum = np.zeros(24)
q_win = np.zeros(24)
q_win[6:17] = q_vik_win
q_sum[5:18] = q_vik_sum
q_ir = [120, 162] #W/m^2, SMAD pdf page 227
#https://www.gfdl.noaa.gov/bibliography/related_files/rjw0001.pdf taken from fig5
T_sum = [175, 175, 170, 170, 170, 180, 190, 210, 225, 240, 250, 270, 270, 275, 270, 260, 255, 250, 225, 210, 200, 180, 175, 175 ]
T_win = np.array(T_sum)-30 #https://mars.nasa.gov/mer/spotlight/20070612.html looks like it's around 30
# =============================================================================
#             ####Equilibrium temperature calculations
# =============================================================================
L_base = 3.431 #m
H_base = 0.545 #m
#Assume its an ellipsoid
def S_bot(L, H):
    #Calculates base station bottom area, assume its an ellipsoid
    a = L/2
    b = L/2
    c = H
    S = 1/2 * 4 * np.pi * (((a*b)**1.6 + (a*c)**1.6 + (b*c)**1.6)/3)**(1/1.6)
    return S
A_base_bot = S_bot(L_base, H_base) #Bottom area, half of ellipsoid surface m^2
A_base_top = np.pi * L_base**2 / 4 #Top area, assume circle surface area m^2
A_base = A_base_bot+A_base_top
A_UAV = 2.5 * 2.30 #Wetted surface area

Q_int_base_peak = 150 #W
Q_int_base_nom = 25 #W both sorta assumed, refer to systems design sheet

Q_int_UAV_cruise = 15 #W, taken from Wout
Q_int_UAV_charge = 50 #W, taken from Wout
Q_int_UAV_standby = 5 #W, low value taken
#Surface oatings

eps_base = 0.06 #bare aluminium
alpha_base = 0.14 #bare aluminium
eps_UAV = eps_base #Also bare aluminium
alpha_UAV = alpha_base #And here
#Power dissipated
Q_int_base_nom = 25 #W, Bare aluminium, SMAD
Q_int_base_peak = 150 #W, Bare aluminium, SMAD
T_base_winnight, Q_base_win = EqTemp(eps_base, alpha_base, Q_int_base_nom, np.min(q_vik_win), A_base_top, A_base_bot, np.min(q_ir))
T_base_sumday, Q_base_sum = EqTemp(eps_base, alpha_base, Q_int_base_peak, np.max(q_vik_sum), A_base_top, A_base_bot, np.max(q_ir))
print('---------------------------------------')
print('Base station equilibrium temperatures')
print('Winter night. Q_int=', Q_base_win[1], 'W, T_eq=', T_base_winnight,'K')
print('Summer day. Q_int=', Q_base_sum[1], 'W, T_eq=', T_base_sumday, 'K')


T_UAV_winnight, Q_UAV_win = EqTemp(eps_UAV, alpha_UAV, Q_int_UAV_standby, np.min(q_vik_win), A_UAV/2, A_UAV/2, np.min(q_ir))
T_UAV_sumday_cruise, Q_UAV_sumday_cruise = EqTemp(eps_UAV, alpha_UAV, Q_int_UAV_cruise, np.max(q_vik_sum), A_UAV/2, A_UAV/2, np.max(q_ir))
T_UAV_sumday_charge,Q_UAV_sumday_charge = EqTemp(eps_UAV, alpha_UAV, Q_int_UAV_charge, np.max(q_vik_sum), A_UAV/2, A_UAV/2, np.max(q_ir))


print('UAV equilibrium temperatures')
print('Winter night, standby, Q_int=', Q_UAV_win[1], 'W, T_eq=', T_UAV_winnight,'K')
print('Summer day, charging. Q_int=', Q_UAV_sumday_charge[1], 'W, T_eq=', T_UAV_sumday_charge, 'K')
print('Summer day, cruising. Q_int=', Q_UAV_sumday_cruise[1], 'W, T_eq=', T_UAV_sumday_cruise, 'K')
# =============================================================================
#                 ###Heat radiated by UAV/Base
# =============================================================================
q_rad_base_winnight = Q_base_win[0]/A_base #radiated flux, base, winter [W/m^2]
q_rad_base_sumday = Q_base_sum[0]/A_base #Radiated flux, base, summer [W/m^2]
q_rad_UAV_winnight = Q_UAV_win[0]/A_UAV
q_rad_UAV_sumday_cruise = Q_UAV_sumday_cruise[0]/A_UAV
q_rad_UAV_sumday_charge = Q_UAV_sumday_charge[0]/A_UAV

# =============================================================================
#             ###Box sizing
# =============================================================================
dim_boxUAV = np.array([300, 180, 200])/1000
dim_boxBASE = np.array([450, 360, 300])/1000 #Taken according to base station size constraints
V_boxUAV = np.prod(dim_boxUAV) #UAV box volume
V_boxBASE = np.prod(dim_boxBASE) #BS box volume
A_boxUAV = SurfaceArea(dim_boxUAV) #UAV box area
A_boxBASE = SurfaceArea(dim_boxBASE) #BASE box area
A_expBASE = dim_boxBASE[1]*dim_boxBASE[2] + dim_boxBASE[0] * dim_boxBASE[1]/2
#A_expUAV = (4524+ 3136 + 10670.89 + 676)/10**6 #Exposed box area
A_expUAV = dim_boxUAV[0] * dim_boxUAV[1]

t_MLI = (0.16 + 0.025 + 0.01)*7/1000 #MLI thickness

Qint_UAVCruise = 34 #W, batteries being discharged + CDH
Qint_UAVSleep = 6.6 #W, batteries not being used
Qint_base = 50.2 #W, receive mode
            ###Required temperatures
T_base_req = [-10, 40] #Atomic clock
T_base_min = np.min(T_base_req)+273 #Batteries
T_base_max = np.max(T_base_req)+273 #Batteries
T_UAV_req = [0, 35] #Spectrometer, batteries
T_UAV_min = np.min(T_UAV_req)+273 #Spectrometer, batteries
T_UAV_max = np.max(T_UAV_req)+273 #Spectrometer, batteries
            

Q_int_UAVbox_nom = 7 #W, based on power dissipated
Q_int_UAVbox_peak = 20  #W, based on power dissipated

Q_int_Basebox_nom = 61.6 #W, based on power dissipated
Q_int_Basebox_peak = 100 #W, peak, based on nominal dissipated +40W

            ###UAV box
            #Cold case, winter night, nominal heat
for Q in np.arange(0,75, 1):
    T_box_UAV_temp = TempBox(Q, Q_int_UAVbox_nom,q_rad_UAV_winnight, A_boxUAV, A_expUAV)
    if T_box_UAV_temp>T_UAV_min:
        print('Cold, UAV Box, Heat required', Q, 'W for an equil temp of', T_box_UAV_temp, 'K')
        Q_box_cold = Q
        break
            #Warm case
Q_box_UAV_hot = []
for Q in np.arange(-75,75, 1):
    T_box_UAV_temp = TempBox(Q, Q_int_UAVbox_peak,q_rad_UAV_sumday_cruise, A_boxUAV, A_expUAV)
    if T_box_UAV_temp>T_UAV_min:
        if T_box_UAV_temp<T_UAV_max:
            Q_box_UAV_hot.append([Q, T_box_UAV_temp])
print('Hot, UAV Box, Temp of',minheat(Q_box_UAV_hot)[1], 'with a heat added/removed', minheat(Q_box_UAV_hot)[0])
            ###Base station box
Q_box_base_hot = []
Q_box_base_cold = []
            #Hot scenario
for Q in np.arange(-75,75, 1):
    T_box_base_temp = TempBox(Q, Q_int_Basebox_peak, q_rad_base_sumday, A_boxBASE, A_expBASE)
    if T_box_base_temp>T_base_min:
        if T_box_base_temp<T_base_max:
            Q_box_base_hot.append([Q, T_box_base_temp])
print('Hot, Base Box, Temp of',minheat(Q_box_base_hot)[1], 'with a heat added/removed', minheat(Q_box_base_hot)[0])
for Q in np.arange(-75,75, 1):
    T_box_base_temp = TempBox(Q, Q_int_Basebox_nom, q_rad_base_winnight, A_boxBASE, A_expBASE)
    if T_box_base_temp>T_base_min:
        if T_box_base_temp<T_base_max:
            Q_box_base_cold.append([Q, T_box_base_temp])
print('Cold, Base Box, Temp of',minheat(Q_box_base_cold)[1], 'with a heat added/removed', minheat(Q_box_base_cold)[0])

            ###Radiator sizing UAV
T_rad = 303 #K, temperature the radiator is kept at https://arc.aiaa.org/doi/abs/10.2514/3.26072?journalCode=jsr
A_req_rad_UAVbox = A_rad(Q_box_cold, T_rad) #Required radiator area for UAV
A_req_rad_Basebox = A_rad(1/2 * Q_int_Basebox_nom, T_rad) #Radiator area for Base
rho_MLI = 0.37 #kg/m^2, 15 layers, SMAD
rho_rad = 3.3 #kg/m^2, SMAD
rho_pipe = 0.15 #kg/m heat pipe, SMAD
            ###Mass estimates
            #UAV
            
M_sensor = 0.03 #Tayco temp sensors
M_radUAV = A_req_rad_UAVbox * rho_rad #Box 1 radiator mass
M_MLIUAV = (A_boxUAV-A_expUAV)*rho_MLI
M_pipeUAV = (1*rho_pipe) #Assuming 1 meter of heatpipes
M_TC_UAV = M_radUAV + M_MLIUAV + M_pipeUAV + M_sensor
            #Base station
M_MLIBASE = (A_boxBASE - A_expBASE) * rho_MLI
M_radBase = A_req_rad_Basebox * rho_rad 
M_pipeBase = (2 * rho_pipe) #Assuming 2 meters of heatpipes
M_TC_base = M_MLIBASE + M_pipeUAV + M_radBase + M_sensor
print('Mass breakdown, UAV:')
print('Total', M_TC_UAV, 'Pipes', M_pipeUAV, 'Radiator', M_radUAV, 'MLI', M_MLIUAV)
print('Power required, during nights:', Q_box_cold)
print('Mass breakdown, Base:')
print('Total', M_TC_base, 'Pipes', M_pipeBase, 'Radiator', M_radBase, 'MLI', M_MLIBASE)