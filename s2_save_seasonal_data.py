#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# Created by : Mohit Anand
# Created on : Sat Aug 06 2022 at 11:14:26 AM
# ==========================================================
# Created on Sat Aug 06 2022
# __copyright__ = Copyright (c) 2022, PCV Project
# __credits__ = [Mohit Anand,]
# __license__ = Pversion__ = 0.0.0
# __maintainer__ = Mohit Anand
# __email__ = itsmohitanand@gmail.com
# __status__ = Development
# ==========================================================

# To create seasonal aggregates and detrend them and save them

import xarray as xr
from pcv.process import aggregate_seasons, detrend_seasons
import matplotlib.pyplot as plt

temp_path = "/data/compoundx/ERA5/MohitBudapestProject/t2m.monthly.era5.nhemisphere.1981-2020.nc"
tp_path = "/data/compoundx/ERA5/MohitBudapestProject/tp.monthly.era5.nhemisphere.1981-2020.nc"
ssrd_path = "/data/compoundx/ERA5/MohitBudapestProject/ssrd.monthly.era5.nhemisphere.1981-2020.nc"
swvlall_path = "/data/compoundx/ERA5/MohitBudapestProject/swvlall.monthly.era5.nhemisphere.1981-2020.nc"
vpd_path = "/data/compoundx/ERA5/MohitBudapestProject/vpd_cf.monthly.era5.nhemisphere.1981-2020.nc"
sd_path = "/data/compoundx/ERA5/MohitBudapestProject/sd.monthly.era5.nhemisphere.1981-2020.nc"
lai_path = "/data/compoundx/lai_global/GLOBMAP_LAI.monthly.nhemisphere.1982-2020.nc"
# smroot_path = "/data/compoundx/anand/PCV/data/SMroot_1980-2021_MO.nc"


t2m_data = xr.open_dataset(temp_path)
tp_data = xr.open_dataset(tp_path)
ssrd_data = xr.open_dataset(ssrd_path)
swvlall_data = xr.open_dataset(swvlall_path)
# sm_data = xr.open_dataset(smroot_path)
# sm_north = sm_data.where(sm_data["lat"]>25, drop=True).where(sm_data["lat"]<75, drop=True).where(sm_data["time.year"]< 2021, drop=True).where(sm_data["time.year"]> 1980, drop=True)
vpd_data = xr.open_dataset(vpd_path)
sd_data = xr.open_dataset(sd_path)

lai_data = xr.open_dataset(lai_path)

aggregated_t2m = aggregate_seasons(t2m_data)
aggregated_tp = aggregate_seasons(tp_data)
aggregated_ssrd = aggregate_seasons(ssrd_data)
aggregated_swvlall = aggregate_seasons(swvlall_data)
# aggregated_sm = aggregate_seasons(sm_north)
aggregated_lai = aggregate_seasons(lai_data)
aggregated_vpd = aggregate_seasons(vpd_data)
aggregated_sd = aggregate_seasons(sd_data)

detrended_t2m = detrend_seasons(aggregated_t2m, deg=1)
detrended_tp = detrend_seasons(aggregated_tp, deg=1)
detrended_ssrd = detrend_seasons(aggregated_ssrd, deg=1)
detrended_swvlall = detrend_seasons(aggregated_swvlall, deg=1)
# detrended_sm = detrend_seasons(aggregated_sm, deg=1)
detrended_vpd = detrend_seasons(aggregated_vpd, deg=1)
detrended_sd = detrend_seasons(aggregated_sd, deg=1)
detrended_lai = detrend_seasons(aggregated_lai, deg=1)

detrended_t2m.to_netcdf("/data/compoundx/anand/PCV/data/detrended_seasonal_t2m.nc")
detrended_tp.to_netcdf("/data/compoundx/anand/PCV/data/detrended_seasonal_tp.nc")
detrended_ssrd.to_netcdf("/data/compoundx/anand/PCV/data/detrended_seasonal_ssrd.nc")
detrended_swvlall.to_netcdf("/data/compoundx/anand/PCV/data/detrended_seasonal_swvlall.nc")
# detrended_sm.to_netcdf("/data/compoundx/anand/PCV/data/detrended_seasonal_smroot.nc")
detrended_lai.to_netcdf("/data/compoundx/anand/PCV/data/detrended_seasonal_lai.nc")
detrended_vpd.to_netcdf("/data/compoundx/anand/PCV/data/detrended_seasonal_vpd.nc")
detrended_sd.to_netcdf("/data/compoundx/anand/PCV/data/detrended_seasonal_sd.nc")

# aggregated_t2m.to_netcdf("/data/compoundx/anand/PCV/data/aggregated_seasonal_t2m.nc")
# aggregated_tp.to_netcdf("/data/compoundx/anand/PCV/data/aggregated_seasonal_tp.nc")
# aggregated_ssrd.to_netcdf("/data/compoundx/anand/PCV/data/aggregated_seasonal_ssrd.nc")
# aggregated_swvlall.to_netcdf("/data/compoundx/anand/PCV/data/aggregated_seasonal_swvlall.nc")
# aggregated_sm.to_netcdf("/data/compoundx/anand/PCV/data/aggregated_seasonal_smroot.nc")
# aggregated_lai.to_netcdf("/data/compoundx/anand/PCV/data/aggregated_seasonal_lai.nc")
# aggregated_vpd.to_netcdf("/data/compoundx/anand/PCV/data/aggregated_seasonal_vpd.nc")
# aggregated_sd.to_netcdf("/data/compoundx/anand/PCV/data/aggregated_seasonal_sd.nc")