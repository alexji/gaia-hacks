import time, os, sys
import numpy as np
import pandas as pd
import gaia_tools.load as gload
from astropy.table import Table

def make_id_tgas_cat(tgas_cat):
    ii_hip = tgas_cat["hip"]>= 0
    ii_tycho = np.logical_and(tgas_cat["tycho2_id"]!=(" "*12), tgas_cat["tycho2_id"]!=(" "*11))
    assert len(tgas_cat) == np.sum(ii_hip) + np.sum(ii_tycho)
    id = tgas_cat["tycho2_id"]
    id[ii_hip] = tgas_cat["hip"][ii_hip]
    id = map(lambda x: x.strip(), id)
    return id

def load_tgas_goodastrometry(cut=0.5):
    return load_tgas_df(parallax_cut=cut, pm_cut=cut)
def load_tgas_df(parallax_cut=None,pm_cut=None):
    start = time.time()
    tgas_cat = gload.tgas()
    tgas = Table(tgas_cat).to_pandas()
    tgas.index = make_id_tgas_cat(tgas_cat)
    print "Load tgas and make ID {:.2f}".format(time.time()-start)
    if parallax_cut is None and pm_cut is None:
        return tgas

    if parallax_cut is not None:
        parallax_quality = tgas["parallax_error"]/tgas["parallax"]
        parallax_quality_cut = np.logical_and(parallax_quality >=0, parallax_quality < parallax_cut)
    else:
        parallax_quality_cut = np.ones(len(tgas),dtype=bool)
    if pm_cut is not None:
        pmra_quality = np.abs(tgas["pmra_error"]/tgas["pmra"])
        pmdec_quality= np.abs(tgas["pmdec_error"]/tgas["pmdec"])
        pmra_quality_cut = np.logical_and(pmra_quality >=0, pmra_quality < pm_cut)
        pmdec_quality_cut = np.logical_and(pmdec_quality >=0, pmdec_quality < pm_cut)
    else:
        pmra_quality_cut = np.ones(len(tgas),dtype=bool)
        pmdec_quality_cut = np.ones(len(tgas),dtype=bool)

    goodii = np.logical_and(np.logical_and(pmra_quality_cut,pmdec_quality_cut),parallax_quality_cut)
    print "Kept {}% ({} par {} pm)".format(float(np.sum(goodii))/len(tgas), parallax_cut, pm_cut)
    tgas = tgas[goodii]
    return tgas

def load_rave_df():
    start = time.time()
    rave_cat = gload.rave()
    return rave_cat.to_pandas()

