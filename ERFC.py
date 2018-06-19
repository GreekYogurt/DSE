from scipy import special
import scipy as sp
a = special.erfc(10)
ebn0lst = sp.arange(0,10,1)
for ebn0 in ebn0lst:
    BER = 1./2 * special.erfc(sp.sqrt(ebn0))
    print 'for', ebn0, BER
