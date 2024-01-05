#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# Created by : Mohit Anand
# Created on : Sun Aug 07 2022 at 8:57:26 AM
# ==========================================================
# Created on Sun Aug 07 2022
# __copyright__ = Copyright (c) 2022, PCV Project
# __credits__ = [Mohit Anand,]
# __license__ = Private
# __version__ = 0.0.0
# __maintainer__ = Mohit Anand
# __email__ = itsmohitanand@gmail.com
# __status__ = Development
# ==========================================================

# Script for running sem model


import xarray as xr
import cartopy.crs as ccrs
import geopandas as gpd

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from pcv.io import majority_class_1_landuse, read_clim_mask, get_climate_shape_feature
from pcv.process import select_data
from pcv.process import mask_crop_forest
from pcv.cfg import IPCC_REGION_SHPFILE, IPCC_ACRONYM
import time
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.metrics import roc_auc_score
from scipy.stats.distributions import chi2

parser = argparse.ArgumentParser(description='Args for model')
parser.add_argument('-v', '--vegetation_type', type=str,
                    help='For choosing the models from models.py')

parser.add_argument('-x','--xtreme', type=str,
                    help='For choosing the models from models.py')

args = parser.parse_args()

vegetation_type = args.vegetation_type
xtreme = args.xtreme

t2m_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_t2m_v3.nc"
tp_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_tp_v3.nc"
ssrd_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_ssrd_v3.nc"
lai_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_lai_v3.nc"
swvlall_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_swvlall_v3.nc"
vpd_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_vpd_v3.nc"
sd_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_sd_v3.nc"

t2m_data = xr.open_dataset(t2m_path)
tp_data = xr.open_dataset(tp_path)
ssrd_data = xr.open_dataset(ssrd_path)
swvlall_data = xr.open_dataset(swvlall_path)
vpd_data = xr.open_dataset(vpd_path)
sd_data = xr.open_dataset(sd_path)
lai_data = xr.open_dataset(lai_path).rename({"lat":"latitude", "lon":"longitude"})
lai_data = lai_data.reindex(lat = list(reversed(lai_data.latitude)))

t2m_winter = select_data(t2m_data,  "winter")
t2m_spring = select_data(t2m_data,  "spring")
t2m_summer = select_data(t2m_data,  "summer")

tp_winter = select_data(tp_data,  "winter")
tp_spring = select_data(tp_data,  "spring")
tp_summer = select_data(tp_data,  "summer")

lai_winter = select_data(lai_data,  "winter")
lai_spring = select_data(lai_data,  "spring")
lai_summer = select_data(lai_data,  "summer")

if xtreme=="low":
    t = lai_summer.quantile(0.1, dim="time")
    lai_summer = xr.where(lai_summer<t, 1, 0)
elif xtreme == "high":
    t = lai_summer.quantile(0.9, dim="time")
    lai_summer = xr.where(lai_summer>t, 1, 0)

##### Create xr dataset to store values

def init_xr_dataset(lat, lon, with_winter = False):

    if with_winter:
        var_list = ["c_t2m_w", "c_t2m_sp", "c_t2m_su", "c_tp_w", "c_tp_sp", "c_tp_su" , "b", "p", "auc", "Y_pred", "Y", "ll", "lr"]
    else:        
        var_list = ["c_t2m_sp", "c_t2m_su", "c_tp_sp", "c_tp_su" , "b", "p","auc", "Y_pred", "Y", "ll"]

    lat = lat.values
    lon = lon.values
    model_data_dict = {}

    for each in var_list:
        model_data_dict[each] = (
                ("latitude", "longitude"), np.full((lat.shape[0], lon.shape[0]), np.nan))
    
    model_data_dict["chi2p"] = (
                ("latitude", "longitude"), np.full((lat.shape[0], lon.shape[0]), np.nan))

    coords= {"latitude":lat, "longitude":lon}

    return xr.Dataset(model_data_dict, coords = coords)


##### Section for everything about the model

xr_dataset = init_xr_dataset(lai_data.latitude, lai_data.longitude)
xr_dataset_w = init_xr_dataset(lai_data.latitude, lai_data.longitude, with_winter = True)

init_time = time.time()
for lat_i, lat in enumerate(lai_data.latitude.values):
    strt_time = time.time()
    for lon_i , lon in enumerate(lai_data.longitude.values):
        lai_su = lai_summer.sel(longitude=lon, latitude=lat).to_numpy()
        

        if (np.sum(lai_su)) <1 or (np.isnan(lai_su).any() == True):
            pass
        else:
            
            # FOR CLIMATE
            # We have an extra year for climate data, thus need to shift with a +1
            t2m_w = t2m_winter.sel(longitude=lon, latitude=lat).to_numpy()
            t2m_sp = t2m_spring.sel(longitude=lon, latitude=lat).to_numpy()
            t2m_su = t2m_summer.sel(longitude=lon, latitude=lat).to_numpy()

            tp_w = tp_winter.sel(longitude=lon, latitude=lat).to_numpy()
            tp_sp = tp_spring.sel(longitude=lon, latitude=lat).to_numpy()
            tp_su = tp_summer.sel(longitude=lon, latitude=lat).to_numpy()
            
            assert t2m_w.shape == t2m_sp.shape == t2m_su.shape == tp_w.shape == tp_sp.shape == tp_su.shape == lai_su.shape
                
            X = np.stack([t2m_sp, t2m_su, tp_sp, tp_su]).T
            X_w = np.stack([t2m_w, t2m_sp, t2m_su, tp_w, tp_sp, tp_su]).T
            
            Y = lai_su


            clf = LogisticRegression(max_iter=5000, class_weight="balanced").fit(X,Y)
            c = clf.coef_[0]

            data_dict = {} 
            Y_score = clf.predict_proba(X)[:,1] 
            Y_pred = clf.predict(X)
            data_dict["ll"] = -log_loss(Y, Y_pred)*len(Y)
            data_dict["c_t2m_sp"] = c[0]
            data_dict["c_t2m_su"] = c[1]
            data_dict["c_tp_sp"] = c[2]
            data_dict["c_tp_su"] = c[3]
            data_dict["b"] = clf.intercept_[0]
            data_dict["auc"] = roc_auc_score(Y, Y_score)
           
            data_dict_w = {}
            clf_w = LogisticRegression(max_iter=5000, class_weight="balanced").fit(X_w,Y)
            c_w = clf_w.coef_[0]

            Y_score_w = clf_w.predict_proba(X_w)[:,1] 
            Y_pred_w = clf_w.predict(X_w)

            data_dict_w["ll"] = -log_loss(Y, Y_pred_w)*len(Y)
            data_dict_w["c_t2m_w"] = c_w[0]   
            data_dict_w["c_t2m_sp"] = c_w[1]
            data_dict_w["c_t2m_su"] = c_w[2]
            data_dict_w["c_tp_w"] = c_w[3]
            data_dict_w["c_tp_sp"] = c_w[4]
            data_dict_w["c_tp_su"] = c_w[5]
            data_dict_w["b"] = clf_w.intercept_[0]
            data_dict_w["auc"] = roc_auc_score(Y, Y_score_w)

            data_dict_w["lr"] = 2*(data_dict_w["ll"] - data_dict["ll"]) 
            data_dict_w["p"] = chi2.sf(data_dict_w["lr"],2) 
            
            for k, v in data_dict.items():
                xr_dataset[k][lat_i, lon_i] = v

            for k, v in data_dict_w.items():
                xr_dataset_w[k][lat_i, lon_i] = v

xr_dataset.to_netcdf(f"/data/compoundx/anand/PCV/data/logreg_{vegetation_type}_{xtreme}.nc")
xr_dataset_w.to_netcdf(f"/data/compoundx/anand/PCV/data/logreg_{vegetation_type}_{xtreme}_w.nc")

print(f"Total time {(time.time()-init_time):.2f} seconds.")