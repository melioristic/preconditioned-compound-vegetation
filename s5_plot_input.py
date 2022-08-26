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

era5_data_path = "/data/compoundx/ERA5/MohitBudapestProject/"


data_path = "/data/compoundx/anand/PCV/data/"
image_path = "/data/compoundx/anand/PCV/images/" 

t2m_path = data_path+"detrended_seasonal_t2m.nc"
swvlall_path = era5_data_path + "swvlall.monthly.era5.nhemisphere.1981-2020.nc"
lai_path = data_path+"detrended_seasonal_lai.nc"

t2m = xr.open_dataset(t2m_path)
swvlall = xr.open_dataset(swvlall_path)
lai = xr.open_dataset(lai_path)


swvlall.swvlall[4*1, :, :].plot(figsize=(14,4))
print(swvlall.swvlall[4*1, :, :].min())

plt.savefig(image_path+f"swvlall_example_{1}.png")
plt.close()

