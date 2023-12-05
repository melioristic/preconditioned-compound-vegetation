#
# Created on Thu Jul 21 2022
#
# Copyright (c) 2022 Your Company
#

# Script for function to process the data

import numpy as np
import xarray as xr
from pcv.misc import timeit
from typing import List, Tuple


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


def standardise_monthly(data:xr.Dataset)->xr.Dataset:
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

def detrend(data:xr.Dataset, deg:int)->xr.Dataset:
    """Detrends the dataset along time dimension by fitting a polynomila of degree `deg` 

    Args:
        data (xr.Dataset): Dataset to be detrended
        deg (int): degree of the polynomial to detrend

    Returns:
        xr.Dataset: Detrended dataset
    """

    p = data.polyfit(dim="time", deg=deg)

    var_name = list(p.keys())[0] # This can be a source of error.
    fit = xr.polyval(data["time"], p[var_name])
    return data - fit

@timeit
def detrend_seasons(data:xr.Dataset, deg:int)->xr.Dataset:
    """Detrend dataset seasonaly, relies on `detrend`
    #LIMITATION
        Will only workd for xarray dataset with 1 variables

    Args:
        data (xr.Dataset): dataset to be detrended
        deg (int): degree of the polynomial to detrend

    Returns:
        xr.Dataset: Detrended dataset
    """

    assert len(list(data.keys())) ==  1, "Detrend seasons only works with datasets with 1 variable"

    data_list = []

    # Depends on the way in which data is aggregated. Here there are 4 seasons
    # DJF, MAM, JJA, SON and the time associated is the first day of the season
    # Thus season months are 3, 6, 9, 12

    for month in range(3,13,3):
        seasonal_data = data.where(data["time.month"]==month, drop=True) #select month
        detrended_season = detrend(seasonal_data, deg) # detrend data
        data_list.append(detrended_season)
    
    return xr.concat(data_list, dim="time").sortby("time")


def aggregate_seasons(data:xr.Dataset)->xr.Dataset:
    """Aggregate data based on seasons. There is a resampling function which can do this. Resampling is done quarterly starting from december. The time assigned is the first day of the sampling period

    Args:
        data (xr.Dataset): data to be resampled

    Returns:
        xr.Dataset: Resampled dataset
    """
    aggregate = data.resample({"time":"QS-DEC"}).mean()
    return aggregate

def select_data(data:xr.Dataset, season:str)->xr.Dataset:
    
    season_list = ["winter", "spring", "summer", "autumn"]
    
    assert season in season_list, "Seasons can only be : winter, spring, summer or autumn"
    month = -1
    if season == "winter":
        time_window = slice("1982", "2019")
        month=12
    elif season=="spring":
        time_window = slice("1983", "2020")
        month=3
    elif season=="summer":
        time_window = slice("1983", "2020")
        month=6
    elif season=="autumn":
        time_window = slice("1983", "2020")
        month=9
    
    data = data.where(data["time.month"]==month, drop=True).sortby("time")

    return data[[i for i in data.keys()][0]].sel(time=time_window) .sortby("latitude", ascending=False) 


def regrid_data(data, interp_like_data):

    interp_like_data = interp_like_data.reindex(latitude=interp_like_data.latitude[::-1])
    coords = {
        "lat" : np.arange(interp_like_data.latitude.values[0], interp_like_data.latitude.values[-1]+0.5, 0.25 ),  
        "lon" : np.arange(interp_like_data.longitude.values[0], interp_like_data.longitude.values[-1]+0.5, 0.25 ) 
    }

    # data.drop_vars(["majority_class_1", "majority_class_2", "majority_class_3"])

    
    area_0_05 = comp_area_lat_lon(data.lat.values, data.lon.values)

    area_0_25 = comp_area_lat_lon(interp_like_data.latitude.values, interp_like_data.longitude.values)

    area_0_25 = np.reshape(area_0_25,(area_0_25.shape[0],area_0_25.shape[1],1))

    regridded_data = (data*area_0_05).groupby_bins("lon", coords["lon"], right = False).sum(skipna=False).groupby_bins("lat", coords["lat"], right = False).sum(skipna=False)/area_0_25

    regridded_data["lat_bins"] = coords["lat"][:-1]
    regridded_data["lon_bins"] = coords["lon"][:-1]

    regridded_data =  regridded_data.rename({"lat_bins":"lat", "lon_bins":"lon"})
        
    return regridded_data


def mask_crop_forest(lu_mc_1:xr.DataArray) -> Tuple[np.array, np.array]:
    """Masks crops and forest regions based on the land use map for multiple years.
    Only the years which have been crops or forest for all the years are considered.

    Args:
        lu_mc_1 (xr.DataArray): The datarray with land use class on lon lat and time dimension

    Returns:
        Tuple[np.array, np.array]: Array of crops and forests masks
    """


    last_year_lu = lu_mc_1
    
    n_year = last_year_lu.shape[0]
    mask_forest = (((last_year_lu>=40).sum("time") == n_year) & (((last_year_lu<110).sum("time") == n_year)))
    mask_crop = (((last_year_lu>=10).sum("time") == n_year) & (((last_year_lu<40).sum("time") == n_year)))

    # return mask_crop.values, mask_forest.values
    return mask_crop.values, mask_forest.values

## NEED TO IMPROVE regridding to make it a more generic function 

# def regrid_data(data_path:str, regrid_like_path:str)->xr.Dataset:
    
#     """The function regrids the data at `data_path` to the same latitude and longitude as `regrid_like_path`. The regrid_like_path data should have latitude and longitude fields. The data path should have lat and lon fields. The function is only tested with nc files The function is based on linear interpolation. This messes up the majority class and hence are deleted. 

#     Args:
#         data_path (str): The path of the data to be regridded
#         regrid_like_path (str): The path of data to be regridded like

#     Returns:
#         xr.Dataset: _description_
#     """

#     with xr.open_dataset(data_path) as data:
#         with xr.open_dataset(regrid_like_path) as interp_like_data:
            
#             interp_like_data = interp_like_data.reindex(latitude=interp_like_data.latitude[::-1])
#             coords = {
#                 "lat" : np.arange(interp_like_data.latitude.values[0], interp_like_data.latitude.values[-1]+0.5, 0.25 ),  
#                 "lon" : np.arange(interp_like_data.longitude.values[0], interp_like_data.longitude.values[-1]+0.5, 0.25 ) 
#             }

#             data.drop_vars(["majority_class_1", "majority_class_2", "majority_class_3"])

#             area_0_05 = comp_area_lat_lon(data.lat.values, data.lon.values)
#             area_0_25 = comp_area_lat_lon(interp_like_data.latitude.values, interp_like_data.longitude.values)

#             regridded_data = (data*area_0_05).groupby_bins("lon", coords["lon"], right = False).sum().groupby_bins("lat", coords["lat"], right = False).sum()/area_0_25

#             regridded_data["lat_bins"] = coords["lat"][:-1]
#             regridded_data["lon_bins"] = coords["lon"][:-1]

#             regridded_data =  regridded_data.rename({"lat_bins":"lat", "lon_bins":"lon"})
        
#     return regridded_data

