import time, os, sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import healpy as hp

import read_data as rd

from astropy import units as u

NSIDE=32

def lb_to_thetaphi(l,b):
    #b = -90 to 90, also dec
    #l = 0 to 360, also ra
    theta = (b+90.)*np.pi/180.
    phi = (l-180.)*np.pi/180.
    return theta,phi

if __name__=="__main__":
    hpbins = np.arange(hp.nside2npix(NSIDE)+1)
    tgas = rd.load_tgas_df()

    # Digitize into healpix based on coordinates
    theta,phi = lb_to_thetaphi(tgas["l"],tgas["b"])
    tgas_hp_galactic = hp.ang2pix(NSIDE, theta, phi)

    # Star density map
    h,x = np.histogram(tgas_hp_galactic,bins=hpbins)
    fig1 = hp.mollview(h,title="TGAS Density Galactic")
    
    # Velocity map
    tgas_good = rd.load_tgas_goodastrometry()
    #pm_quality_cut = np.logical_and(tgas[""]

    #indices = np.digitize(tgas_hp_galactic, hpbins)

    #theta,phi = lb_to_thetaphi(tgas["ra"],tgas["dec"])
    #tgas_hp_radec = hp.ang2pix(NSIDE, theta, phi)
    #h,x = np.histogram(tgas_hp_radec,bins=hpbins)
    #fig2 = hp.mollview(h,title="TGAS Density RA DEC")

    plt.show()
