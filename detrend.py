""" preprocessing climate variable"""

import numpy as np
import xarray
from matplotlib import pyplot as plt
from scipy import signal

from time_passed import tic, tac


def createXarrayAsExample(other: xarray.DataArray, new_values: np.ndarray) -> xarray:
    """ takes a xarray with a given size (for example time, lat, lon)
        and a numpy other with the new values.
        It creates a xarray of same dims, coords and metadata (dates etc) than "other".
        We avoid to use .copy and .values since it is useless and would be much longer.
        :param other: the other xarray from which we take the structure
        :param new_values : the new values to save. Must be the same shape as other.shape"""

    if new_values.shape != other.shape:
        raise ValueError('The new_values must have the same shape as the other xarray')

    values_xr = xarray.DataArray(data=new_values, dims=other.dims,
                                 coords=other.coords, attrs=other.attrs,
                                 name=other.name)
    return values_xr


def detrend_pixelwise(data: xarray.DataArray) -> xarray.DataArray:
    """ detrends a lat lon time xarray from its linear variation with time,
    on every gridpoints independantly. returns the detrended lai. """

    axis_time = data.get_axis_num(dim='time')
    data_detrended = np.apply_along_axis(func1d=signal.detrend, axis=axis_time, arr=data)

    # create a xarray from this numpy array, with the originalk structure
    data_detrended_xr = createXarrayAsExample(data, data_detrended)
    return data_detrended_xr


def visualise_detrending(data: xarray.DataArray, data_detrended: xarray.DataArray):
    """ visualising the detrending effect on a lai and its detrending"""
    data_detrended = xarray.open_dataset(path_detrend)[var_name]

    data_france = data.sel(latitude=slice(55, 42), longitude=slice(0, 10))
    data_france_time_serie = data_france.mean(dim='latitude').mean(dim='longitude')

    data_france_d = data_detrended.sel(latitude=slice(55, 42), longitude=slice(0, 10))
    data_france_d_time_serie = data_france_d.mean(dim='latitude').mean(dim='longitude')

    data_france[0].plot(), plt.title(f"original {var_name} for january 1982 - France"), plt.show()
    data_france_d[0].plot(), plt.title(f"detrended {var_name} for january 1982 - France"), plt.show()

    data_france_time_serie.plot(), plt.title(f"original {var_name} for january 1982 - France"), plt.show()
    data_france_d_time_serie.plot(), plt.title(f"detrended {var_name} for january 1982 - France"), plt.show()


# load the lai
dir_root = "/home/julie_andre/PycharmProjects/Damocles_Project3/data/"  # depending on your computer
var_name = "t2m"
nc_name = var_name + ".monthly.era5.europe.1981-2020.nc"
nc_path = dir_root + nc_name

data = xarray.open_dataset(nc_path)[var_name]

# detrending

print(f"beginning the detrending for variable {var_name}")
tic()
data_detrended = detrend_pixelwise(data)
tac()

# saving the lai as a ncdf
save = True
if save:
    path_detrend = dir_root + var_name + ".monthly.era5.europe.1981-2020_detrended.nc" # path to save the detrend lai
    data_detrended.to_netcdf(path_detrend)



