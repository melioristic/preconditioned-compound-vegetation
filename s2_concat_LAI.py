#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# Created by : Mohit Anand
# Created on : Sat Aug 06 2022 at 10:39:25 AM
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

# Script to concatenate monthly netCDF files of LAI

import xarray as xr


lai_list = []
for year in range(1982, 2021):
    lai_list.append(xr.open_dataset(f"/data/compoundx/lai_global/GLOBMAP_LAI.monthly.{year}.nhemisphere.regridded.nc"))

lai_concatenated = xr.concat(lai_list, dim="time")

lai_concatenated.to_netcdf(f"/data/compoundx/lai_global/GLOBMAP_LAI.monthly.nhemisphere.1982-2020.nc")