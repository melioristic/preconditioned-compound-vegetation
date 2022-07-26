import numpy as np
import xarray

""" functions to get a xarray of the good structure and attributes. """


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
