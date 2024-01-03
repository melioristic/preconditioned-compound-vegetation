#
# Created on Wed Jul 20 2022
#
# Copyright (c) 2022 Your Company
#

## The script for all the input and output files
from pcv.process import comp_area_lat_lon
import xarray as xr
import numpy as np
import os
from sklearn.model_selection import train_test_split
from typing import Tuple, List
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shpreader
from pcv.cfg import IPCC_REGION_SHPFILE

def read_ipcc_region_csv(path) -> None:
    
    data = np.loadtxt(path)
    data =data[:,:,np.newaxis]
    train_data, test_data = train_test_split(data, test_size=0.1, train_size=0.9, shuffle=True)
        
    return train_data, test_data

def read_clim_mask(mask_path = "/data/compoundx/anand/PCV/data/clim_mask/" )-> Tuple[List, List]:
    clim_files = [mask_path + file for file in os.listdir(mask_path) if ".npy" in file ]
    return [np.load(files) for files in clim_files], [files.split("/")[-1] for files in clim_files]

def read_land_use(year)->xr.Dataset:
    if year < 2016:
        version = "2.0.7cds"
    else:
        version = "2.1.1"

    file_name = f"/data/compoundx/anand/PCV/data/CCI-LC/ESACCI-LC-L4-LCCS-Map-300m-P1Y-aggregated-0.250000Deg-{year}-v{version}.nc"
    return xr.open_dataset(file_name)

def majority_class_1_landuse(lon:List, lat:List)->xr.DataArray:
    """Gest the majority class data of land use

    Args:
        lon (List): List of longitudes to select
        lat (List): List of latitudes to select

    Returns:
        xr.DataArray: Majority class of data for the given 27 years
    """
    val = []
    for i in range(1992, 2019):
        if i!=2014:
            data = read_land_use(i)
            val.append(data.sel(lat = lat, lon = lon).majority_class_1.data)

    majority_class_1 = np.stack(val)

    lu_mc_1 = xr.DataArray(
        majority_class_1, dims = ["time", "latitude", "longitude"], coords = {
            "time" : np.concatenate([np.arange(1992, 2014), np.arange(2015, 2019)]),
            "latitude" : lat,
            "longitude" : lon,
        }
    )
    return lu_mc_1


def get_climate_shape_feature(shpfile = IPCC_REGION_SHPFILE):
    ipcc_regions = shpreader.Reader(shpfile)
    shape_feature_list = []
    for i, records in enumerate(ipcc_regions.records()):
        shape_feature = ShapelyFeature([records.geometry], ccrs.PlateCarree(), facecolor = "None", edgecolor='black', lw=1)
        shape_feature_list.append((records.attributes["Name"], shape_feature, (records.geometry.centroid.x, records.geometry.centroid.y) ))

    return shape_feature_list