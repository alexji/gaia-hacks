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

def load_tgas_df():
    start = time.time()
    tgas_cat = gload.tgas()
    tgas = Table(tgas_cat).to_pandas()
    tgas.index = make_id_tgas_cat(tgas_cat)
    print "Load tgas and make ID {:.2f}".format(time.time()-start)
    return tgas

def load_rave_df():
    start = time.time()
    rave_cat = gload.rave()
    return rave_cat.to_pandas()

