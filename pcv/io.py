#
# Created on Wed Jul 20 2022
#
# Copyright (c) 2022 Your Company
#

## The script for all the input and output files

import xarray as xr

def regrid_data(data_path:str, regrid_like_path:str)->xr.Dataset:
    
    """The function regrids the data at `data_path` to the same latitude and longitude as `regrid_like_path`. The regrid_like_path data should have latitude and longitude fields. The data path should have lat and lon fields. The function is only tested with nc files The function is based on linear interpolation.

    Args:
        data_path (str): The path of the data to be regridded
        regrid_like_path (str): The path of data to be regridded like

    Returns:
        xr.Dataset: _description_
    """

    with xr.open_dataset(data_path) as data:
        with xr.open_dataset(regrid_like_path) as interp_like_data:
            coords = {
                "lat" : interp_like_data.latitude.values,
                "lon" : interp_like_data.longitude.values
            }
    return data.interp(coords, method="zero")
