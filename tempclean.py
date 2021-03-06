import numpy as np
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
        eps_box_exp = 0.92 #Also white paint, SMAD, Z93
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

Q_int_base_peak = 150 #W, based on charging efficiency and component outside of thermal box power usage
Q_int_base_nom = 25 #W, based on components outside of box power usage

Q_int_UAV_cruise = 15 #W, based on mechanical power transfer efficiency
Q_int_UAV_charge = 50 #W, based on charging efficiency
Q_int_UAV_standby = 5 #W, based on component heat dissipated during standby
#Surface oatings

eps_base = 0.06 #bare aluminium
alpha_base = 0.14 #bare aluminium
eps_UAV = eps_base #Also bare aluminium
alpha_UAV = alpha_base #And here
#Power dissipated
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

t_MLI = (0.16 + 0.025 + 0.01)*7/1000 #MLI thickness, 0.16mm dacron netting insulation, 0.025 mm coated and backet kapton, 0.01 mm aluminized kaptop per layer
            ###Required temperatures
T_base_req = [-10, 40] #Atomic clock
T_base_min = np.min(T_base_req)+273 #Batteries
T_base_max = np.max(T_base_req)+273 #Batteries
T_UAV_req = [0  , 35] #Spectrometer, batteries
T_UAV_min = np.min(T_UAV_req)+273 #Spectrometer, batteries
T_UAV_max = np.max(T_UAV_req)+273 #Spectrometer, batteries
            

Q_int_UAVbox_nom = 7 #W, based on power dissipated
Q_int_UAVbox_peak = 20  #W, based on power dissipated

Q_int_Basebox_nom = 61.6 #W, based on nominal power dissipated
Q_int_Basebox_peak = 100 #W, peak, based on nominal dissipated +40W from transmission

            ###UAV box
            #Cold case, winter night, nominal heat
for Q in np.arange(0,75, 1):
    T_box_UAV_temp = TempBox(Q, Q_int_UAVbox_nom,q_rad_UAV_winnight, A_boxUAV, A_expUAV)
    if T_box_UAV_temp>T_UAV_min:
        print('Cold, UAV Box, Heat required', Q, 'W for an equil temp of', T_box_UAV_temp, 'K')
        Q_box_cold = Q
        T_UAVbox_C = T_box_UAV_temp
        break
            #Warm case
Q_box_UAV_hot = []
for Q in np.arange(-75,75, 1):
    T_box_UAV_temp = TempBox(Q, Q_int_UAVbox_peak,q_rad_UAV_sumday_cruise, A_boxUAV, A_expUAV)
    if T_box_UAV_temp>T_UAV_min:
        if T_box_UAV_temp<T_UAV_max:
            Q_box_UAV_hot.append([Q, T_box_UAV_temp])
print('Hot, UAV Box, Temp of',minheat(Q_box_UAV_hot)[1], 'with a heat added/removed', minheat(Q_box_UAV_hot)[0])
print('--------------')
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
rho_MLI = 0.37 #kg/m^2, average MLI thickness, SMAD
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
print('Mass and power, UAV:')
print('Total', M_TC_UAV, 'Pipes', M_pipeUAV, 'Radiator', M_radUAV, 'MLI', M_MLIUAV)
print('Power required, during nights:', Q_box_cold, 'W')
print('Mass breakdown, Base:')
print('Total', M_TC_base, 'Pipes', M_pipeBase, 'Radiator', M_radBase, 'MLI', M_MLIBASE)


print('Verification, average Mars surface temperature, neglecting atmosphere', EqTemp(0.9, 0.75, 0, 1362/1.52**2, 144.8*10**15/2, 144.8*10**15/2, 0)[0]-273,'C')
print('Sensitivity Analysis')
def Diff(v1, v2):
    #Outputs the value and the % change between two values
    return v2-v1, int((v2-v1)/v1*100)
#Changes in inputs
Q_int_base_peak2 = 150*0.8 #W, 20% decrease
Q_int_base_nom2 = 25*0.8 #W
Q_int_UAV_cruise2 = 15*0.8 #W
Q_int_UAV_standby2 = 5*0.8 #W
T_box_UAV_tempW = TempBox(Q_box_cold, Q_int_UAVbox_nom,q_rad_UAV_winnight, A_boxUAV, A_expUAV)
T_box_UAV_tempD = TempBox(minheat(Q_box_UAV_hot)[0], Q_int_UAVbox_peak,q_rad_UAV_sumday_cruise, A_boxUAV, A_expUAV)
T_box_base_tempD = TempBox(minheat(Q_box_base_hot)[0], Q_int_Basebox_peak, q_rad_base_sumday, A_boxBASE, A_expBASE)
T_box_base_tempW = TempBox(minheat(Q_box_base_cold)[0], Q_int_Basebox_nom, q_rad_base_winnight, A_boxBASE, A_expBASE)

print('Int outside heat diff [Abs, %], UAVwin, UAVsum, Basewin, Basesum', Diff(Q_int_UAV_standby,Q_int_UAV_standby2), Diff(Q_int_UAV_cruise,Q_int_UAV_cruise2), Diff(Q_int_base_nom,Q_int_base_nom2), Diff(Q_int_base_peak,Q_int_base_peak2))
T_UAV_winnight2, Q_UAV_win2 = EqTemp(eps_UAV, alpha_UAV, Q_int_UAV_standby2, np.min(q_vik_win), A_UAV/2, A_UAV/2, np.min(q_ir))
T_UAV_sumday_cruise2, Q_UAV_sumday_cruise2 = EqTemp(eps_UAV, alpha_UAV, Q_int_UAV_cruise2, np.max(q_vik_sum), A_UAV/2, A_UAV/2, np.max(q_ir))
T_base_winnight2, Q_base_win2 = EqTemp(eps_base, alpha_base, Q_int_base_nom2, np.min(q_vik_win), A_base_top, A_base_bot, np.min(q_ir))
T_base_sumday2, Q_base_sum2 = EqTemp(eps_base, alpha_base, Q_int_base_peak2, np.max(q_vik_sum), A_base_top, A_base_bot, np.max(q_ir))
q_rad_base_winnight2 = Q_base_win2[0]/A_base #radiated flux, base, winter [W/m^2]
q_rad_base_sumday2 = Q_base_sum2[0]/A_base #Radiated flux, base, summer [W/m^2]
q_rad_UAV_winnight2 = Q_UAV_win2[0]/A_UAV
q_rad_UAV_sumday_cruise2 = Q_UAV_sumday_cruise2[0]/A_UAV
print('Outside temperatures [Abs, %], UAVwin, UAVsum, Basewin, Basesum', Diff(T_UAV_winnight,T_UAV_winnight2),Diff(T_UAV_sumday_cruise,T_UAV_sumday_cruise2), Diff(T_base_winnight,T_base_winnight2), Diff(T_base_sumday,T_base_sumday2))
print('IR radiated flux [Abs, %], UAVwin, UAVsum, Basewin, Basesum', Diff(q_rad_UAV_winnight,q_rad_UAV_winnight2), Diff(q_rad_UAV_sumday_cruise,q_rad_UAV_sumday_cruise2), Diff(q_rad_base_winnight,q_rad_base_winnight2), Diff(q_rad_base_sumday,q_rad_base_sumday2))
T_box_UAV_tempW2 = TempBox(Q_box_cold, Q_int_UAVbox_nom,q_rad_UAV_winnight2, A_boxUAV, A_expUAV)
T_box_UAV_tempD2 = TempBox(minheat(Q_box_UAV_hot)[0], Q_int_UAVbox_peak,q_rad_UAV_sumday_cruise2, A_boxUAV, A_expUAV)
T_box_base_tempD2 = TempBox(minheat(Q_box_base_hot)[0], Q_int_Basebox_peak, q_rad_base_sumday2, A_boxBASE, A_expBASE)
T_box_base_tempW2 = TempBox(minheat(Q_box_base_cold)[0], Q_int_Basebox_nom, q_rad_base_winnight2, A_boxBASE, A_expBASE)
print('Box temperatures [Abs, %], UAVwin, UAVsum, Basewin, Basesum', Diff(T_box_UAV_tempW,T_box_UAV_tempW2), Diff(T_box_UAV_tempD,T_box_UAV_tempD2), Diff(T_box_base_tempW,T_box_base_tempW2), Diff(T_box_base_tempD,T_box_base_tempD2))

Q_int_UAVbox_nom2 = 7*0.8 #W, based on power dissipated
Q_int_UAVbox_peak2 = 20*0.8  #W, based on power dissipated
Q_int_Basebox_nom2 = 61.6*0.8 #W, based on nominal power dissipated
Q_int_Basebox_peak2 = 100*0.8 #W, peak, based on nominal dissipated +40W from transmission



T_box_UAV_tempW3 = TempBox(Q_box_cold, Q_int_UAVbox_nom2,q_rad_UAV_winnight, A_boxUAV, A_expUAV)
T_box_UAV_tempD3 = TempBox(minheat(Q_box_UAV_hot)[0], Q_int_UAVbox_peak2,q_rad_UAV_sumday_cruise, A_boxUAV, A_expUAV)
T_box_base_tempD3 = TempBox(minheat(Q_box_base_hot)[0], Q_int_Basebox_peak2, q_rad_base_sumday, A_boxBASE, A_expBASE)
T_box_base_tempW3 = TempBox(minheat(Q_box_base_cold)[0], Q_int_Basebox_nom2, q_rad_base_winnight, A_boxBASE, A_expBASE)

print('Int inside diff [Abs, %], UAVwin, UAVsum, Basewin, Basesum', Diff(Q_int_UAVbox_nom,Q_int_UAVbox_nom2), Diff(Q_int_UAVbox_peak,Q_int_UAVbox_peak2), Diff(Q_int_Basebox_nom,Q_int_Basebox_nom2), Diff(Q_int_Basebox_peak,Q_int_Basebox_peak2))

print('Box temperatures [Abs, %], UAVwin, UAVsum, Basewin, Basesum', Diff(T_box_UAV_tempW,T_box_UAV_tempW3),Diff(T_box_UAV_tempD,T_box_UAV_tempD3), Diff(T_box_base_tempW,T_box_base_tempW3), Diff(T_box_base_tempD,T_box_base_tempD3))

