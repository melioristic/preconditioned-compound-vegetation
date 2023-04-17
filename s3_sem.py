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
import semopy as sm
from pcv.process import select_data
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from pcv.ds import create_xr_dataset, fill_xr_dataset
import pcv.models as models
import time

import argparse

parser = argparse.ArgumentParser(description='Args for model')
parser.add_argument('model_num', metavar='mn', type=int,
                    help='For choosing the models from models.py')

args = parser.parse_args()
model_num = args.model_num

t2m_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_t2m.nc"
tp_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_tp.nc"
ssrd_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_ssrd.nc"
lai_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_lai.nc"
swvlall_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_smroot.nc"
vpd_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_vpd.nc"
sd_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_sd.nc"

t2m_data = xr.open_dataset(t2m_path)
tp_data = xr.open_dataset(tp_path)
ssrd_data = xr.open_dataset(ssrd_path)
swvlall_data = xr.open_dataset(swvlall_path)
vpd_data = xr.open_dataset(vpd_path)
sd_data = xr.open_dataset(sd_path)
lai_data = xr.open_dataset(lai_path)

t2m_winter = select_data(t2m_data,  "winter")
t2m_spring = select_data(t2m_data,  "spring")
t2m_summer = select_data(t2m_data,  "summer")

tp_winter = select_data(tp_data,  "winter")
tp_spring = select_data(tp_data,  "spring")
tp_summer = select_data(tp_data,  "summer")

ssrd_winter = select_data(ssrd_data,  "winter")
ssrd_spring = select_data(ssrd_data,  "spring")
ssrd_summer = select_data(ssrd_data,  "summer")

lai_winter = select_data(lai_data,  "winter")
lai_spring = select_data(lai_data,  "spring")
lai_summer = select_data(lai_data,  "summer")

swvlall_winter = select_data(swvlall_data,  "winter")
swvlall_spring = select_data(swvlall_data,  "spring")
swvlall_summer = select_data(swvlall_data,  "summer")

vpd_winter = select_data(vpd_data,  "winter")
vpd_spring = select_data(vpd_data,  "spring")
vpd_summer = select_data(vpd_data,  "summer")


sd_winter = select_data(sd_data,  "winter")
sd_spring = select_data(sd_data,  "spring")
sd_summer = select_data(sd_data,  "summer")

##### Section for everything about the model

mod = getattr(models, f"mod_{model_num}")

model = sm.Model(mod)

xr_dataset = create_xr_dataset(model, lai_data.lat, lai_data.lon)

init_time = time.time()
for lat_i, lat in enumerate(lai_data.lat.values):
    strt_time = time.time()
    for lon_i , lon in enumerate(lai_data.lon.values):

        model = sm.Model(mod)
        lai_w = lai_winter.sel(lon=lon, lat=lat).to_numpy()
        swvlall_w = swvlall_winter.sel(lon=lon, lat=lat).to_numpy()
        swvlall_su = swvlall_summer.sel(lon=lon, lat=lat).to_numpy()
        swvlall_sp = swvlall_spring.sel(lon=lon, lat=lat).to_numpy()
        
        sd_sp = sd_spring.sel(longitude=lon, latitude=lat).to_numpy()

        if np.isnan(lai_w).any() == True:
            pass
        elif np.isnan(swvlall_w).all() == True:
            pass
        elif np.isnan(swvlall_su).all() == True:
            pass
        elif np.isnan(swvlall_sp).all() == True:
            pass
        elif np.nansum(sd_sp) == 0:
            pass
        # elif np.nansum(swvlall_w) < 1e-10:
        #     pass
        # elif np.nansum(swvlall_su) < 1e-10:
        #     pass
        # elif np.nansum(swvlall_sp) < 1e-10:
        #     pass
        else:
            
            try:

                lai_w = lai_winter.sel(lon=lon, lat=lat).to_numpy()
                lai_sp = lai_spring.sel(lon=lon, lat=lat).to_numpy()                
                lai_su = lai_summer.sel(lon=lon, lat=lat).to_numpy()
                # FOR CLIMATE
                # We have an extra year for climate data, thus need to shift with a +1
                t2m_w = t2m_winter.sel(longitude=lon, latitude=lat).to_numpy()
                t2m_sp = t2m_spring.sel(longitude=lon, latitude=lat).to_numpy()
                t2m_su = t2m_summer.sel(longitude=lon, latitude=lat).to_numpy()

                tp_w = tp_winter.sel(longitude=lon, latitude=lat).to_numpy()
                tp_sp = tp_spring.sel(longitude=lon, latitude=lat).to_numpy()
                tp_su = tp_summer.sel(longitude=lon, latitude=lat).to_numpy()
                
                ssrd_w = ssrd_winter.sel(longitude=lon, latitude=lat).to_numpy()
                ssrd_sp = ssrd_spring.sel(longitude=lon, latitude=lat).to_numpy()
                ssrd_su = ssrd_summer.sel(longitude=lon, latitude=lat).to_numpy()

                vpd_w = vpd_winter.sel(longitude=lon, latitude=lat).to_numpy()
                vpd_sp = vpd_spring.sel(longitude=lon, latitude=lat).to_numpy()
                vpd_su = vpd_summer.sel(longitude=lon, latitude=lat).to_numpy()

                sd_w = sd_winter.sel(longitude=lon, latitude=lat).to_numpy()
                sd_sp = sd_spring.sel(longitude=lon, latitude=lat).to_numpy()
                sd_su = sd_summer.sel(longitude=lon, latitude=lat).to_numpy()

                swvlall_w = swvlall_winter.sel(lon=lon, lat=lat).to_numpy()
                swvlall_sp = swvlall_spring.sel(lon=lon, lat=lat).to_numpy()
                swvlall_su = swvlall_summer.sel(lon=lon, lat=lat).to_numpy()


                assert t2m_w.shape == t2m_sp.shape == t2m_su.shape
                
                list_val = [t2m_w, t2m_sp, t2m_su,
                        tp_w, tp_sp, tp_su, 
                        ssrd_w, ssrd_sp, ssrd_su, 
                        lai_w, lai_sp, lai_su,
                        vpd_w, vpd_sp, vpd_su,
                        sd_w, sd_sp, sd_su,
                        swvlall_w, swvlall_sp, swvlall_su,
                        ]

                col_names = ["t2m_winter", "t2m_spring", "t2m_summer",
                                "tp_winter", "tp_spring", "tp_summer",
                                "ssrd_winter", "ssrd_spring", "ssrd_summer",
                                "lai_winter", "lai_spring", "lai_summer", 
                                "vpd_winter", "vpd_spring", "vpd_summer",
                                "sd_winter", "sd_spring", "sd_summer",
                                "swvlall_winter", "swvlall_spring", "swvlall_summer",
                                ]    
                
                data = np.vstack(list_val).T

                df = pd.DataFrame(data, columns=col_names)
                df=(df-df.mean())/df.std()
                model.fit(df)
                chi2p = sm.calc_stats(model)["chi2 p-value"][0]
                xr_dataset = fill_xr_dataset(xr_dataset, model.inspect(), chi2p, lat_i, lon_i)
            
            except:
                pass

    print(f"Time taken for lat {lat_i} is {(time.time()-strt_time):.2f} seconds.")

xr_dataset.to_netcdf(f"/data/compoundx/anand/PCV/data/sem_data_{model_num}_gleam.nc")
print(f"Total time {(time.time()-init_time):.2f} seconds.")

