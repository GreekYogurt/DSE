import numpy as np

#MastCam
#Res
DegToRad = np.pi/180.
#==============================================================================
#             ###Functions
#==============================================================================
def resol(FOV, picsie, h):
    #Input FOV of pic in the form [N, M] in degrees, pic size in pixels [N, M] pixels and altitude in m
    #Output possible resolution, Area of image, [length and width of image]
    res_high = np.max(res)
    res_low = np.min(res)
    FOV_high = np.max(FOV) * DegToRad
    FOV_low = np.min(FOV) * DegToRad
    l = 2 * h * np.tan(FOV_high/2.)    
    w = 2 * h * np.tan(FOV_low/2.)    
    res_long = 2 * h * np.tan(FOV_high/2.)/res_high
    res_short = 2 * h * np.tan(FOV_low/2.)/res_low
    A_captured = l * w
    return res_long, res_short, A_captured, [l, w]
def area(d):
    #Outputs are based on diameter
    A = np.pi * d**2/4.
    return A
    
#==============================================================================
#             ##Mission parameters
#==============================================================================
v = 5 #m/s
d_fine = 2000 #m
d_coarse = 100000 #m
h = 2000 #m, altitude
A_fine = area(d_fine) #Area to cover during fine mapping
A_coarse = area(d_coarse) #Area to cover during coarse mapping


#==============================================================================
#             ##MastCam-Z
#==============================================================================
res = [1600, 1200] #[N x M] pixels, according to https://mars.nasa.gov/mars2020/mission/instruments/mastcam-z/
FOV_W = [23, 18] #[N x M] deg, wide, https://mars.nasa.gov/mars2020/mission/instruments/mastcam-z/for-scientists/
FOV_N = [6, 5] #[N x M] deg, narrow, https://mars.nasa.gov/mars2020/mission/instruments/mastcam-z/for-scientists/
m_mastcam = 4.5 #kg
fps = 4 #frames per second
P_used1 = 11.8 #Watts, picturing
P_used2 = 11.8 #Watts, standby
r_l_w, r_s_w, A_w, lxw_w = resol(FOV_W, res, h)
r_l_n, r_s_n, A_n, lxw_n = resol(FOV_N, res, h)
print 'Resolution, narrow', r_l_n, r_s_n, 'm per pixel, Pic size = ', A_w, '[L, W]', lxw_w
print 'Resolution, wide', r_l_w, r_s_w, 'm per pixel, Pic size = ', A_n, '[L, W]', lxw_n
N_fine = A_fine/A_n #Number of pics for fine mapping with narrow angled cam
sec_perpic = np.max(lxw_n)/float(v) #time per picture
T_fine = N_fine * sec_perpic/3600./24. #Time for fine mapping
