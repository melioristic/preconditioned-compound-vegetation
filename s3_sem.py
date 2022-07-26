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
from pcv.models import *
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
swvlall_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_swvlall.nc"
vpd_path = "/data/compoundx/anand/PCV/data/detrended_seasonal_vpd.nc"

t2m_data = xr.open_dataset(t2m_path)
tp_data = xr.open_dataset(tp_path)
ssrd_data = xr.open_dataset(ssrd_path)
swvlall_data = xr.open_dataset(swvlall_path)
vpd_data = xr.open_dataset(vpd_path)
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

##### Section for everything about the model

if model_num==1:
    mod = mod_1
elif model_num==2:
    mod = mod_2
elif model_num==20:
    mod = mod_2_extended
elif model_num==3:
    mod = mod_3
elif model_num==4:
    mod = mod_4

model = sm.Model(mod)

xr_dataset = create_xr_dataset(model, lai_data.lat, lai_data.lon)

init_time = time.time()
for lat_i, lat in enumerate(lai_data.lat.values):
    strt_time = time.time()
    for lon_i , lon in enumerate(lai_data.lon.values):

        model = sm.Model(mod)
        lai_w = lai_winter.GLOBMAP_LAI.sel(lon=lon, lat=lat).to_numpy()[1:-1]
        swvlall_w = swvlall_winter.swvlall.sel(longitude=lon, latitude=lat).to_numpy()[2:-1]
        if np.isnan(lai_w).any() == True:
            pass
        elif np.isnan(swvlall_w).all() == True:
            pass
        else:
           
            
            # FOR LAI
            # taking winter of 1982 and not 1981 which is partial
            # subsequently we leave the last year
            # Account for 1 more year because of the DJA problem 

            # From 1982 winter to 
            lai_w = lai_winter.GLOBMAP_LAI.sel(lon=lon, lat=lat).to_numpy()[1:-1]
            # now take spring and summer from 1983 (following year)
            lai_sp = lai_spring.GLOBMAP_LAI.sel(lon=lon, lat=lat).to_numpy()[:-1]
            lai_su = lai_summer.GLOBMAP_LAI.sel(lon=lon, lat=lat).to_numpy()[:-1]

            # FOR CLIMATE
            # We have an extra year for climate data, thus need to shift with a +1
            t2m_w = t2m_winter.t2m.sel(longitude=lon, latitude=lat).to_numpy()[2:-1]
            t2m_sp = t2m_spring.t2m.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]
            t2m_su = t2m_summer.t2m.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]

            tp_w = tp_winter.tp.sel(longitude=lon, latitude=lat).to_numpy()[2:-1]
            tp_sp = tp_spring.tp.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]
            tp_su = tp_summer.tp.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]
            
            ssrd_w = ssrd_winter.ssrd.sel(longitude=lon, latitude=lat).to_numpy()[2:-1]
            ssrd_sp = ssrd_spring.ssrd.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]
            ssrd_su = ssrd_summer.ssrd.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]

            vpd_w = vpd_winter.vpd_cf.sel(longitude=lon, latitude=lat).to_numpy()[2:-1]
            vpd_sp = vpd_spring.vpd_cf.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]
            vpd_su = vpd_summer.vpd_cf.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]

            swvlall_w = swvlall_winter.swvlall.sel(longitude=lon, latitude=lat).to_numpy()[2:-1]
            swvlall_sp = swvlall_spring.swvlall.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]
            swvlall_su = swvlall_summer.swvlall.sel(longitude=lon, latitude=lat).to_numpy()[1:-1]


            assert t2m_w.shape == t2m_sp.shape == t2m_su.shape
            
            list_val = [t2m_w, t2m_sp, t2m_su,
                    tp_w, tp_sp, tp_su, 
                    ssrd_w, ssrd_sp, ssrd_su, 
                    lai_w, lai_sp, lai_su,
                    vpd_w, vpd_sp, vpd_su,
                    swvlall_w, swvlall_sp, swvlall_su,
                    ]

            col_names = ["t2m_winter", "t2m_spring", "t2m_summer",
                            "tp_winter", "tp_spring", "tp_summer",
                            "ssrd_winter", "ssrd_spring", "ssrd_summer",
                            "lai_winter", "lai_spring", "lai_summer", 
                            "vpd_winter", "vpd_spring", "vpd_summer",
                            "swvlall_winter", "swvlall_spring", "swvlall_summer",
                            ]    
            
            data = np.vstack(list_val).T

            df = pd.DataFrame(data, columns=col_names)
            df=(df-df.mean())/df.std()
            model.fit(df)
            chi2p = sm.calc_stats(model)["chi2 p-value"][0]
            xr_dataset = fill_xr_dataset(xr_dataset, model.inspect(), chi2p, lat_i, lon_i)


    print(f"Time taken for lat {lat_i} is {(time.time()-strt_time):.2f} seconds.")

xr_dataset.to_netcdf(f"/data/compoundx/anand/PCV/data/sem_data_{model_num}.nc")
print(f"Total time {(time.time()-init_time):.2f} seconds.")

