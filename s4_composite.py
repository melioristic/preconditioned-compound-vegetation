import xarray as xr
import semopy as sm
from pcv.process import select_data
import matplotlib.pylab as plt
import pandas as pd
import numpy as np

t2m_path = "/Users/anand/Documents/data/project_3_data/data/detrended_t2m.nc"
tp_path = "/Users/anand/Documents/data/project_3_data/data/detrended_tp.nc"
rad_path = "/Users/anand/Documents/data/project_3_data/data/detrended_ssrd.nc"
lai_path = "/Users/anand/Documents/data/project_3_data/data/detrended_lai.nc"
swvlall_path = "/Users/anand/Documents/data/project_3_data/data/detrended_swvlall.nc"
vpd_path = "/Users/anand/Documents/data/project_3_data/data/detrended_vpd.nc"
sd_path = "/Users/anand/Documents/data/project_3_data/data/detrended_sd.nc"

t2m_data = xr.open_dataset(t2m_path)
tp_data = xr.open_dataset(tp_path)
ssrd_data = xr.open_dataset(rad_path)
swvlall_data = xr.open_dataset(swvlall_path)
vpd_data = xr.open_dataset(vpd_path)
lai_data = xr.open_dataset(lai_path)
sd_data = xr.open_dataset(sd_path)

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

lai_summer_arr = lai_summer.to_numpy() 