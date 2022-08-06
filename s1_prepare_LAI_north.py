#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# Created by : Mohit Anand
# Created on : Sat Aug 06 2022 at 12:47:52 AM
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

import xarray as xr
from pcv.process import regrid_data

era5_data_path = "/data/compoundx/ERA5/MohitBudapestProject/"

t2m_path = era5_data_path + "t2m.monthly.era5.nhemisphere.1981-2020.nc"

lai_data_path = "/data/compoundx/lai_global/GLOBMAP_LAI.monthly.1982.nc"

t2m_dataset = xr.open_dataset(t2m_path)

### First select the dataset in the northern hemisphere

latitude = t2m_dataset.latitude.values
longitude = t2m_dataset.longitude.values

min_lat = min(latitude)
max_lat = max(latitude)
min_lon = min(longitude)
max_lon = max(longitude)

lai_list = []
for year in range(1982, 2021):
    print(f"Writing files for year : {year}")
    with xr.open_dataset(f"/data/compoundx/lai_global/GLOBMAP_LAI.monthly.{year}.nc") as lai_data:
        # Select northern hemisphere
        lai_n_data = lai_data.sel(lat=slice(max_lat,min_lat), lon=slice(min_lon,max_lon))
        # Regrid the data        
        lai_n_regridded = regrid_data(lai_n_data, t2m_dataset)
        # Save in a list to concatenate the data
        lai_list.append(lai_n_regridded)


lai_concatenated = xr.concat(lai_list, dim="time")

lai_concatenated.to_netcdf(f"/data/compoundx/lai_global/GLOBMAP_LAI.monthly.nhemisphere.1982-2020.nc")