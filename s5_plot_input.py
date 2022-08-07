#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# Created by : Mohit Anand
# Created on : Sat Aug 06 2022 at 4:54:25 PM
# ==========================================================
# Created on Sat Aug 06 2022
# __copyright__ = Copyright (c) 2022, PCV Project
# __credits__ = [Mohit Anand,]
# __license__ = Private
# __version__ = 0.0.0
# __maintainer__ = Mohit Anand
# __email__ = itsmohitanand@gmail.com
# __status__ = Development
# ==========================================================

# Script to plot the input data 
import xarray as xr
import matplotlib.pyplot as plt


data_path = "/data/compoundx/anand/PCV/data/"
image_path = "/data/compoundx/anand/PCV/images/" 

t2m_path = data_path+"detrended_seasonal_t2m.nc"
swvlall_path = data_path+"detrended_seasonal_swvlall.nc"
lai_path = data_path+"detrended_seasonal_lai.nc"

t2m = xr.open_dataset(t2m_path)
swvlall = xr.open_dataset(swvlall_path)
lai = xr.open_dataset(lai_path)

# for i in range(5):

#     swvlall.swvlall[4*i, :, :].plot(figsize=(14,4))
#     plt.savefig(image_path+f"swvlall_example_{i}.png")
#     plt.close()

# lai.GLOBMAP_LAI[4*i, :, :].plot(figsize=(14,4))
# plt.savefig(image_path+f"lai_example_{i}.png")


sem_data = xr.open_dataset(data_path+"sem_data_2.nc")
print(sem_data.keys())
sem_data["chi2p"].plot(figsize=(14,4))
plt.savefig(image_path+"sem_example.png")