import numpy as np

def mprop(tb, Ft, Isp):
    #Input Ft in kN, Isp in s, burn time in s
    #Outputs tonnes of prop used
    return tb * Ft / float(Isp) / 9.80665
#Falcon 9 FT
def F9FTpars():
            ###Stages
    NE1 = 9 #Number of engines
    Ft1 = 8277 #kN, vacuum
    Isp1 = 311 #s, vac
    tb1 = 162 #s, vac
    Mp1 = mprop(tb1, Ft1, Isp1)
    
    NE2 = 1
    Ft2 = 934 #kN, vac
    Isp2 = 348 #s
    tb2 = 397 #s
    Mp2 = mprop(tb2, Ft2, Isp2)
    
    Mgto = 5500 #kg to GTO capability, recoverable
    Mp = Mp1+Mp2 #total prop mass
    cost = 62.
    print 'Mass to GTO', Mgto, '[kg], payload/fuel = ', (Mgto /1000./ (float(Mp)))
    print 'Cost $k per kilo to GTO', cost/float(Mgto)*1000
    print 'Prop used', Mp

    return '----'
    
def F9Hpars():
            ###Stages
    #Boosters
    Nb = 2 #Number of boosters
    NEb = 9 #engines per booster
    Ftb = 16400 #kN, vac
    Ispb = 311 #s, vac
    tbb = 154 #s
    Mpb = mprop(tbb, Ftb, Ispb)
    #1st stage
    NE1 = 9 #Number of engines
    Ft1 = 8277 #kN, vacuum
    Isp1 = 311 #s, vac
    tb1 = 187 #s, vac
    Mp1 = mprop(tb1, Ft1, Isp1)
    #2nd stage
    NE2 = 1
    Ft2 = 934 #kN, vac
    Isp2 = 348 #s
    tb2 = 397 #s
    Mp2 = mprop(tb2, Ft2, Isp2)
    Mgto = 26700 #kg to GTO capability, recoverable
    Mp = Mp1+Mp2+Mpb #total prop mass
    cost = 90.
    print 'Mass to GTO', Mgto, '[kg], payload/fuel = ', (Mgto /1000./ (float(Mp)))
    print 'Cost $k per kilo to GTO', cost/float(Mgto)*1000
    print 'Prop used', Mp

    return '----'
def AtlasVpars():
      ###Stages
    #Boosters
    Nb = range(6) #Number of boosters
    Ftb = 1688.4 #kN
    Ispb = 279.3 #s, vac
    tbb = 94 #s
    Mpb = mprop(tbb, Ftb, Ispb)*max(Nb) #Assuming 5 boosters
    #1st stage
    NE1 = 1 #Number of engines
    Ft1 = 4152 #kN, vacuum
    Isp1 = 337.8 #s, vac
    tb1 = 253 #s, vac
    Mp1 = mprop(tb1, Ft1, Isp1)
    #2nd stage
    NE2 = 1
    Ft2 = 99.2 #kN, vac
    Isp2 = 450.5 #s
    tb2 = 842 #s
    Mp2 = mprop(tb2, Ft2, Isp2)
    Mgto = 8900. #kg to GTO capability, recoverable
    Mp = Mp1+Mp2+Mpb #total prop mass
    cost = 132.4
    print 'Mass to GTO', Mgto, '[kg], payload/fuel = ', (Mgto /1000./ (float(Mp)))
    print 'Cost $k per kilo to GTO', cost/float(Mgto)*1000
    print 'Prop used', Mp

    return '----'
def Ariane5pars(): #ECA variation
       ###Stages
    #Boosters
    Nb = 2 #Number of boosters
    Ftb = 7080 #kN
    Ispb = 275. #s, vac
    tbb = 140 #s
    Mpb = mprop(tbb, Ftb, Ispb)*Nb #Assuming 5 boosters
    #1st stage
    NE1 = 1 #Number of engines
    Ft1 = 1390 #kN, vacuum
    Isp1 = 432 #s, vac
    tb1 = 540 #s, vac
    Mp1 = mprop(tb1, Ft1, Isp1)
    #2nd stage
    NE2 = 1
    Ft2 = 67 #kN, vac
    Isp2 = 446 #s
    tb2 = 945 #s
    Mp2 = mprop(tb2, Ft2, Isp2)
    Mgto = 11115. #kg to GTO capability, recoverable
    Mp = Mp1+Mp2+Mpb #total prop mass
    cost = 170.
    print 'Mass to GTO', Mgto, '[kg], payload/fuel = ', (Mgto /1000./ (float(Mp)))
    print 'Cost $k per kilo to GTO', cost/float(Mgto)*1000
    print 'Prop used', Mp
    return '----'
    
def Soyuz2Pars(): #ECA variation
       ###Stages
    #Boosters
    Nb = 4 #Number of boosters
    Ftb = 1019.93 #kN
    Ispb = 320.2 #s, vac
    tbb = 118 #s
    Mpb = mprop(tbb, Ftb, Ispb)*Nb #Assuming 5 boosters
    #1st stage
    NE1 = 1 #Number of engines
    Ft1 = 923.86 #kN, vacuum
    Isp1 = 320.6 #s, vac
    tb1 = 286 #s, vac
    Mp1 = mprop(tb1, Ft1, Isp1)
    #2nd stage
    NE2 = 1
    Ft2 = 298 #kN, vac
    Isp2 = 326 #s
    tb2 = 270 #s
    Mp2 = mprop(tb2, Ft2, Isp2)
    Mgto = 3250. #kg to GTO capability, recoverable
    Mp = Mp1+Mp2+Mpb #total prop mass
    cost = 80.
    print 'Mass to GTO', Mgto, '[kg], payload/fuel = ', (Mgto /1000./ (float(Mp)))
    print 'Cost $k per kilo to GTO', cost/float(Mgto)*1000
    print 'Prop used', Mp

    return '----'
print 'F9 FT', F9FTpars()
print 'F9 HEAVY', F9Hpars()
print 'Atlas V', AtlasVpars()
print 'Ariane 5', Ariane5pars()
print 'Soyuz2', Soyuz2Pars()