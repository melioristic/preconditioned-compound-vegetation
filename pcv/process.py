#
# Created on Thu Jul 21 2022
#
# Copyright (c) 2022 Your Company
#

# Script for function to process the data

import numpy as np
import xarray as xr
from pcv.misc import timeit

def comp_area_lat_lon(lat:np.array,lon:np.array)->np.array:
    """Calculate the area between an array of lat lons

    Args:
        lat (np.array): Array of latitudes
        lon (np.array): Array of longitudes

    Returns:
        np.array: Area 
    """


    radius = 6.37122e6 # in meters

    lat=np.squeeze(lat); lon=np.squeeze(lon)
    nlat=len(lat)
    nlon=len(lon)

    # LATITUDE
    lat_edge=np.zeros((nlat+1))
    lat_edge[0] = max(-90, lat[0]-0.5*(lat[1]-lat[0])); #ana
    lat_edge[1:nlat] = 0.5*(lat[0:nlat-1] + lat[1:nlat])
    lat_edge[nlat] = min(90, lat[nlat-1]-0.5*(lat[nlat-2]-lat[nlat-1]))
    dlat=np.diff(lat_edge)

    #LONGITUDE
    lon_edge=np.zeros((nlon+1))
    lon_edge[0] = lon[0]-0.5*(lon[1]-lon[0])
    lon_edge[1:nlon] = 0.5*(lon[0:nlon-1] + lon[1:nlon])
    lon_edge[nlon] = lon[nlon-1]-0.5*(lon[nlon-2]-lon[nlon-1])
    dlon=np.diff(lon_edge)

    dlon_2d, dlat_2d = np.meshgrid(dlon,dlat) # create mesh with cell size in deg
    lon_2d, lat_2d = np.meshgrid(lon, lat)

    dy = radius * (dlat_2d * (np.pi/180.0))
    dx = radius * np.multiply(dlon_2d * (np.pi/180.0),np.cos(lat_2d * (np.pi/180.0)))

    area = np.multiply(dx , dy)
    if np.sum(area)<0:
        area=-1*area

    return area


@timeit
def standardise_monthly(data:xr.Dataset, var:str)->xr.Dataset:
    """Function standardises the `var` in the xarray `data`. This typically means subtracting the mean and dividing it by standard deviation of the data. The function does it at a monthly scale

    Args:
        data (xr.Dataset): The xarray dataset to be standardised
        var (str): The name of the variable to be standarised in the data.

    Returns:
        xr.Dataset: Monthly standardised data
    """
    month_mean=data.groupby('time.month').mean("time")
    month_std=data.groupby('time.month').std("time")
    
    standardised_data = (data.groupby('time.month') - month_mean).groupby('time.month') / month_std 
    
    return standardised_data

def detrend(data:xr.Dataset, deg:int, var:str)->xr.Dataset:
    p = data.polyfit(dim="time", deg=deg)
    fit = xr.polyval(data["time"], p[var+"_polyfit_coefficients"])
    return data - fit

def aggregate_seasons(data:xr.Dataset, var="t2m")->xr.Dataset:
    aggregate = data.resample({"time":"QS-DEC"}).sum()
    return aggregate


