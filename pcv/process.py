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

@timeit
def detrend(data:xr.Dataset, deg:int, var:str)->xr.Dataset:
    p = data.polyfit(dim="time", deg=deg)
    fit = xr.polyval(data["time"], p["polyfit_coefficients"])
    return data - fit

def detrend_seasons(data:xr.Dataset, deg:int, var:str)->xr.Dataset:

    data_list = []
    for month in range(3,13,3):
        seasonal_data = data[var].where(data["time.month"]==month, drop=True)
        detrended_season = detrend(seasonal_data, deg, var)
        data_list.append(detrended_season)


    if var=="vpd_cf":
        print(f"var_name changed from {var} to vpd")
        var = "vpd"
    
    return xr.concat(data_list, dim="time").sortby("time").to_dataset(name=var)

def aggregate_seasons(data:xr.Dataset, var="t2m")->xr.Dataset:
    aggregate = data.resample({"time":"QS-DEC"}).mean()
    return aggregate

def select_data(data:xr.Dataset, season:str)->xr.Dataset:
    
    season_list = ["winter", "spring", "summer", "autumn"]
    
    assert season in season_list, "Seasons can only be : winter, spring, summer or autumn"
    month = -1
    if season == "winter":
        month=12
    elif season=="spring":
        month=3
    elif season=="summer":
        month=6
    elif season=="autumn":
        month=9
    return data.where(data["time.month"]==month, drop=True).sortby("time")

def create_xr_dataset(model, lat, lon):
    model_data_dict = {}
    
    var_list = _create_xr_variable_list(model)
    metric_list = model.inspect().columns[3:]

    xr_dict_list = _permute_list(var_list, metric_list)

    for each in xr_dict_list:
        model_data_dict[each] = (
                ("latitude", "longitude"), np.full((200, 220), np.nan))
    
    model_data_dict["chi2p"] = (
                ("latitude", "longitude"), np.full((200, 220), np.nan))

    coords= {"latitude":lat, "longitude":lon}

    return xr.Dataset(model_data_dict, coords = coords)

def _create_xr_variable_list(model):
    var_list = []
    for index in model.inspect().index:
        var_list.append("".join(model.inspect().iloc[index,:3].values))

    return var_list

def _permute_list(a, b):
    permuted_list = []
    for each_1 in a:
        for each_2 in b:
            permuted_list.append(each_1+"_"+each_2)
    return permuted_list

def fill_xr_dataset(xr_dataset, model_inspect, chi2p, lat, lon):

    xr_dataset["chi2p"][lat, lon] = chi2p
    xr_dataset = _fill_inspect_data(xr_dataset, model_inspect, lat, lon)

    return xr_dataset

def _fill_inspect_data(xr_dataset, model_inspect, lat, lon):
    for index in model_inspect.index:
        var_name = "".join(model_inspect.iloc[index, :3].values)

        for metric, val in model_inspect.iloc[index,3:].iteritems():
            xr_dataset[var_name+"_"+metric][lat, lon] = val

    return xr_dataset

