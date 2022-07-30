""" This script aims at computing, saving and plotting winter or spring maps
of composites years where summer LAI was especially low or high. """
from typing import Union

import numpy as np
import xarray as xr
from matplotlib import pyplot as plt

from lib_ploting import plotMap_withBorders, savefigure
from lib_xarray import createXarrayAsExample
from pcv.process import standardise_seasonly
from time_passed import tic, tac


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
    and select the N timesteps of dates with lowest or highest data_1D values.
    NB : the indices correspond to the N dates with extreme values, but not in order ! """
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
    if only_nans_in(time_steps_indices_1D):
        return np.nan

    values_list = []
    for index in time_steps_indices_1D:
        if not np.isnan(index):
            values_list.append(climate_data_1D[int(index)])

    mean_for_extreme = np.mean(values_list)
    return mean_for_extreme


def compute_composite(climate_data: xr.DataArray, time_steps_indices: xr.DataArray) -> xr.DataArray:
    """ For each lat lon, computes the mean on the N time steps listed in time_steps_indices at those lat lon,
    of the values taken in the climate_data. Watch out, the time steps must be consitent with the time or climate_data."""
    latitude = climate_data.latitude.values
    longitude = climate_data.longitude.values
    print("did you check the consistency between climate data time steps and the original time steps? ")

    composite = createXarrayAsExample(climate_data[0], np.zeros(np.shape(climate_data[0])))
    time_steps_indices_xr = createXarrayAsExample(climate_data[:len(time_steps_indices)], time_steps_indices)

    for lat in latitude:
        for lon in longitude:
            # todo : complete
            climate_data_1D = climate_data.sel(latitude=lat, longitude=lon)
            time_steps_indices_1D = time_steps_indices_xr.sel(latitude=lat, longitude=lon)
            mean_value = mean_climate_for_extreme_LAI(climate_data_1D.values, time_steps_indices_1D.values)
            composite.loc[lat, lon] = mean_value
    return composite


def example_on_France_pixel(lai_summer: xr.DataArray, climate_data: xr.DataArray):
    """ computes the composites values for one pixel in France"""
    lon, lat = 0, 45
    lai_1D = lai_summer.sel(latitude=lat, longitude=lon, method="nearest")
    lai_1D.plot(), plt.title("LAI anomaly, for France pixel"), plt.show()
    climate_data_1D = climate_data.sel(latitude=lat, longitude=lon, method="nearest")

    time_steps_indices_1D = select_time_steps_extreme_values(lai_1D, N)
    print(N, "lowest steps,", time_steps_indices_1D.values)
    years_extreme = lai_summer.time[time_steps_indices_1D.values].dt.year.values  # list of int
    print(N, "lowest years, ", years_extreme)
    print(f"LAI mean on this lai is {lai_1D.mean(dim='time').values}, "
          f"and the lowest value is {lai_1D.sel(time=str(years_extreme[0])).values}")
    mean_winter_T_ext_lai = mean_climate_for_extreme_LAI(climate_data_1D, time_steps_indices_1D).values
    print(f"the mean winter T anomaly on these {N} extreme {extreme_type} LAI years, is : {mean_winter_T_ext_lai}")


# depending on your computer
dir_root = "/home/julie_andre/PycharmProjects/Damocles_Project3/data/data_preprocessed/"
dir_save_nc = "/home/julie_andre/PycharmProjects/Damocles_Project3/generated_data/composites_map/"
saving_figure = True
dir_save_fig = "/home/julie_andre/PycharmProjects/Damocles_Project3/plots/"

# load the LAI detrended data
var_name_path = "lai"
var_name = "GLOBMAP_LAI"
nc_path = f"{dir_root}detrended_{var_name_path}.nc"
lai = xr.open_dataset(nc_path)[var_name]

# select summer data only
lai_summer = lai.groupby("time.season")["JJA"]
axis_time = lai_summer.get_axis_num(dim='time')

# we need to take first year of LAI
first_year_LAI = lai_summer.time.dt.year[0].values
last_year_LAI = lai_summer.time.dt.year[-1].values
print("lai data first summer", first_year_LAI)

# parameters for selection of extreme LAI years

for season in ["DJF"]:  # ["DJF", "MAM"]:  # season on which to look at the anomalies.
    print(f"working on {season} effects --------------------------")
    for N in [10]:  # number of extreme years, 1, 3
        for extreme_type in ["low", "high"]:
            print(f"working on the {N} extreme {extreme_type} summer LAI.")

            # years of the extreme LAI values
            time_steps_indices = np.apply_along_axis(func1d=select_time_steps_extreme_values, arr=lai_summer,
                                                     axis=axis_time, N=N,
                                                     extreme_type=extreme_type)
            tic()
            for var_name in ["swvlall"]:  # , "tp", "sd", "ssrd", "swvlall", "vpd"]:  # "t2m"
                print("working on", var_name)

                ## Mean winter climate variable for this 5 years, pointwise

                nc_path = f"{dir_root}detrended_{var_name}.nc"
                climate_data_abs = xr.open_dataset(nc_path)[var_name]

                # standardise the data
                climate_data_season_all = standardise_seasonly(climate_data_abs)
                climate_data_season_all.to_netcdf(dir_root + f"detrended_and_season_standardized_{var_name}" + ".nc")

                # make sure the time steps are consistent
                offset = 0
                if season == "DJF":
                    offset = -1 # winter starts one calendar year before
                climate_data_season_all = climate_data_season_all.sel(time=slice(str(first_year_LAI + offset), str(last_year_LAI)))

                # select the season on the climate data
                climate_data_season = climate_data_season_all.groupby("time.season")[season]

                print(f"climate data, on season {season} only, going from", climate_data_season.time[0].values)


                # compute the composite - takes about 40s by variable on Julie's laptop.
                composite = compute_composite(climate_data_season, time_steps_indices)

                # plot the map
                if saving_figure:
                    plt.figure(figsize=(8, 6))
                    plotMap_withBorders(composite, cmap="bwr",
                                        title=f"{season} {var_name} anomalies - for the {N} {extreme_type}est summer LAI")

                    name_data = f"composite_map_{season}_{var_name}_for_{N}_{extreme_type}_summer_LAI"
                    savefigure(dir_save_fig + "composites_map/" + name_data + ".png")
                    plt.close()

                # save the array as a netcdf
                composite.to_netcdf(dir_save_nc + f"for_{extreme_type}est_LAI/" + name_data + ".nc")
            tac()

print("done!")
