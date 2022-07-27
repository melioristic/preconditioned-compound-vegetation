""" This script aims at computing and plotting winter maps of composites years
where summer LAI was especially low or high. """
from typing import Union

import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

from lib_ploting import plotMap_withBorders, savefigure
from lib_xarray import createXarrayAsExample

# load lai data
dir_root = "/home/julie_andre/PycharmProjects/Damocles_Project3/data/data_preprocessed/"  # depending on your computer

var_name_path = "lai"
var_name = "GLOBMAP_LAI"
nc_path = f"{dir_root}detrended_{var_name_path}.nc"
lai = xr.open_dataset(nc_path)[var_name]

# select summer data only
lai_summer = lai.groupby("time.season")["JJA"]

# parameters for selection of extreme LAI years
N = 5
extreme_type = "low"


## Select pixelwise the N years with lowest LAI in summer
def only_nans_in(data_1D: Union[np.array, xr.DataArray]) -> bool:
    """ return True if there are only nans in the 1D data"""
    values_nan = np.unique(np.isnan(data_1D))  # True, or False or False and True
    if (len(values_nan) == 1) and (True in values_nan):
        return True
    else:
        return False


def select_time_steps_extreme_values(data_1D: Union[np.array, xr.DataArray], N: int, extreme_type: str = "low") \
        -> Union[np.array, xr.DataArray]:
    """ takes a 1D time serie of an impact variable (LAI here),
    and select the dates of the N timesteps of lowest or highest values.
    NB : the indices correspond to the N minimum values, not ordered ! """
    if only_nans_in(data_1D):
        return np.array([np.nan] * N)  # could transform it as xarray for consistency.
    if extreme_type == "low":
        indices = np.argpartition(data_1D, N)
        indices_N_lowest = indices[:N]
        return indices_N_lowest

    elif extreme_type == "high":
        # we just chnage the sign of the lai
        data_1D_inversed = - data_1D
        indices_N_highest = np.argpartition(data_1D_inversed, N)[:N]
        return indices_N_highest

    else:
        raise ValueError(" extreme_type must be in ['low', 'high']")


def time_indice_to_year(indices_array: np.ndarray, time_serie: np.array) -> np.ndarray:
    """ returns an array with years instead of indices"""

    def time_indice_to_year_pixel(index: int, time_serie: np.array) -> int:
        """return the year of this time step
        @param time_serie: array of the years
        """
        if np.isnan(index):
            return np.nan
        return time_serie[int(index)]

    year_array = np.apply_along_axis(func1d=time_indice_to_year_pixel, axis=0, arr=indices_array, time_serie=time_serie)

    return year_array

def plot_year_extreme_summer_LAI(lai_summer: xr.DataArray, extreme_type="low"):
    # extracting the time steps for all lat lon.
    axis_time = 0
    time_steps_indices = np.apply_along_axis(func1d=select_time_steps_extreme_values, arr=lai_summer, axis=axis_time,
                                             N=1, extreme_type=extreme_type)
    # converting to years
    years_series = lai_summer.time.dt.year.values
    years_extreme = time_indice_to_year(time_steps_indices, years_series)

    # ploting part
    years_extreme_xr = createXarrayAsExample(lai_summer[0], years_extreme)  # same xarray structure as the initial data
    plotMap_withBorders(years_extreme_xr, title=f"Years with {extreme_type}est summer LAI")

    # saving
    dir_save_fig = "/home/julie_andre/PycharmProjects/Damocles_Project3/plots/"
    path_save_fig = dir_save_fig + f"years_{extreme_type}est_lai.png"
    savefigure(path_save_fig)
    plt.show()

def mean_climate_for_extreme_LAI(climate_data_1D: np.array, time_steps_indices_1D: np.array) -> float:
    """ computes the mean on the N time steps listed in time_steps_indices_1D, of the values taken in the climate_data_1D"""
    if only_nans_in(climate_data_1D):
        return np.nan

    values_list = []
    for index in time_steps_indices_1D:
        print(index)
        if not np.isnan(index):
            values_list.append(climate_data_1D[index])

    mean_for_extreme = np.mean(values_list)
    return mean_for_extreme

def compute_composite(climate_data:xr.DataArray, time_steps_indices: xr.DataArray):
    """ For each lat lon, computes the mean on the N time steps listed in time_steps_indices at those lat lon,
    of the values taken in the climate_data"""
    latitude = climate_data.latitude.values
    longitude= climate_data.longitude.values
    composite = createXarrayAsExample(climate_data[0], np.zeros(np.shape(climate_data[0])))
    for lat in latitude:
        for lon in latitude:
            print(lat, lon)
            # todo : complete
            # composite at lat lon mean of these values


# # try on the French pixel
# lon, lat = 0, 45
# lai_1D = lai_summer.sel(latitude=lat, longitude=lon, method="nearest")
# lai_1D.plot(), plt.title("LAI anomaly, for France pixel"), plt.show()
#
# time_steps_indices_1D = select_time_steps_extreme_values(lai_1D, N)
# print(N, "lowest steps,", time_steps_indices_1D.values)
# years_extreme = lai_summer.time[time_steps_indices_1D.values].dt.year.values  # list of int
# print(N, "lowest years, ", years_extreme)
# print(f"LAI mean on this lai is {lai_1D.mean(dim='time').values}, "
#       f"and the lowest value is {lai_1D.sel(time=str(years_extreme[0])).values}")
# mean_winter_T_ext_lai = mean_climate_for_extreme_LAI(lai_1D, time_steps_indices_1D).values
# print(f"the mean winter T anomaly on these {N} extreme {extreme_type} LAI years, is : {mean_winter_T_ext_lai}")


# plot_year_extreme_summer_LAI(lai_summer, extreme_type="low")

axis_time = 0
time_steps_indices = np.apply_along_axis(func1d=select_time_steps_extreme_values, arr=lai_summer, axis=axis_time, N=N,
                                         extreme_type=extreme_type)
# plt.imshow(time_steps_indices_1D[0]), plt.title("indexes of years with first low LAI"), plt.colorbar(), plt.show()


## Mean winter temperature for this 5 years, pointwise
var_name = "t2m"
nc_path = f"{dir_root}detrended_{var_name}.nc"
climate_data = xr.open_dataset(nc_path)[var_name]

season = "DJF"
climate_data_season = climate_data.groupby("time.season")[season]


# on 3D LAI
# TODO : bug here to correct. size issue.
mean_winter_T_ext_lai  = compute_composite(climate_data_season, time_steps_indices)

# createXarrayAsExample()
# plotMap_withBorders()

## Composite map of winter climate variable on those years
