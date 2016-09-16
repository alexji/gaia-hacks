import time

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

def make_id_df(df):
    assert len(df) == np.sum(pd.isnull(df["hip"])) + np.sum(pd.isnull(df["tycho2_id"]))
    id = df["tycho2_id"].copy()
    id.name = "id"
    id[pd.isnull(df["tycho2_id"])] = df["hip"][~pd.isnull(df["hip"])].astype(int).astype(str) #pandas matches indices
    return id

def merge_in_dfs(tgas,dfs, datanames):
    # Manually counted things: 65 columns
    # 59 tgas columns
    # 6 extra columns from vizier download
    # u'angDist', u'ra_ep2000', u'dec_ep2000', u'errHalfMaj', u'errHalfMin', u'errPosAng'
    merged = tgas
    for df,dataname in zip(dfs,datanames):
        start = time.time()
        col_indices = []
        for i,col in enumerate(df.columns):
            if col[:-2]==".1" or col in tgas: continue
            col_indices.append(i)
        cols = df.columns[col_indices]
        merged = pd.merge(merged, df[cols], left_index=True, right_index=True, 
                          how="left", suffixes=('_tgas','_'+dataname), sort=False)
        print "  Time to merge {}: {:.2f}".format(dataname, time.time()-start)
    return merged

def test_id_match(tgas,df):
    start = time.time()
    merged = pd.merge(tgas,df,left_index=True,right_index=True)
    print "Merge time {:.2f}".format(time.time()-start)
    assert len(merged)==len(df)

if __name__=="__main__":
    datanames = ["2mass","apass","sdssdr8","wise"]
    fnames = ["data/tgas_"+x+".csv" for x in datanames]
    start = time.time()
    
    dfs = [pd.read_csv(fname) for fname in fnames]
    print "Reading all dfs {:.2f}".format(time.time()-start)
    
    start = time.time()
    tgas_cat = gload.tgas()
    tgas = Table(tgas_cat).to_pandas()
    tgas.index = make_id_tgas_cat(tgas_cat)
    print "Load tgas and make ID {:.2f}".format(time.time()-start)
    
    start = time.time()
    merged = merge_in_dfs(tgas, dfs, datanames)
    print "Load tgas and make ID {:.2f}".format(time.time()-start)

#    # TEST
#    start = time.time()
#    df = pd.read_csv(fnames[2])
#    df.index = make_id_df(df)
#    print "Load sdss and make ID {:.2f}".format(time.time()-start)
    
    
    #Index([u'hip', u'tycho2_id', u'solution_id', u'source_id', u'random_index',
    #u'ref_epoch', u'ra', u'ra_error', u'dec', u'dec_error', u'parallax',
    #u'parallax_error', u'pmra', u'pmra_error', u'pmdec', u'pmdec_error',
    #u'ra_dec_corr', u'ra_parallax_corr', u'ra_pmra_corr', u'ra_pmdec_corr',
    #u'dec_parallax_corr', u'dec_pmra_corr', u'dec_pmdec_corr',
    #u'parallax_pmra_corr', u'parallax_pmdec_corr', u'pmra_pmdec_corr',
    #u'astrometric_n_obs_al', u'astrometric_n_obs_ac',
    #u'astrometric_n_good_obs_al', u'astrometric_n_good_obs_ac',
    #u'astrometric_n_bad_obs_al', u'astrometric_n_bad_obs_ac',
    #u'astrometric_delta_q', u'astrometric_excess_noise',
    #u'astrometric_excess_noise_sig', u'astrometric_primary_flag',
    #u'astrometric_relegation_factor', u'astrometric_weight_al',
    #u'astrometric_weight_ac', u'astrometric_priors_used',
    #u'matched_observations', u'duplicated_source',
    #u'scan_direction_strength_k1', u'scan_direction_strength_k2',
    #u'scan_direction_strength_k3', u'scan_direction_strength_k4',
    #u'scan_direction_mean_k1', u'scan_direction_mean_k2',
    #u'scan_direction_mean_k3', u'scan_direction_mean_k4', u'phot_g_n_obs',
    #u'phot_g_mean_flux', u'phot_g_mean_flux_error', u'phot_g_mean_mag',
    #u'phot_variable_flag', u'l', u'b', u'ecl_lon', u'ecl_lat'],
    #dtype='object')
