#
# Created on Wed Jul 20 2022
#
# Copyright (c) 2022 Your Company
#

## The script for all the input and output files
from pcv.process import comp_area_lat_lon
import xarray as xr
import numpy as np

def regrid_data(data_path:str, regrid_like_path:str)->xr.Dataset:
    
    """The function regrids the data at `data_path` to the same latitude and longitude as `regrid_like_path`. The regrid_like_path data should have latitude and longitude fields. The data path should have lat and lon fields. The function is only tested with nc files The function is based on linear interpolation. This messes up the majority class and hence are deleted. 

    Args:
        data_path (str): The path of the data to be regridded
        regrid_like_path (str): The path of data to be regridded like

    Returns:
        xr.Dataset: _description_
    """

    with xr.open_dataset(data_path) as data:
        with xr.open_dataset(regrid_like_path) as interp_like_data:
            
            interp_like_data = interp_like_data.reindex(latitude=interp_like_data.latitude[::-1])
            coords = {
                "lat" : np.arange(interp_like_data.latitude.values[0], interp_like_data.latitude.values[-1]+0.5, 0.25 ),  
                "lon" : np.arange(interp_like_data.longitude.values[0], interp_like_data.longitude.values[-1]+0.5, 0.25 ) 
            }

            data.drop_vars(["majority_class_1", "majority_class_2", "majority_class_3"])

            area_0_05 = comp_area_lat_lon(data.lat.values, data.lon.values)
            area_0_25 = comp_area_lat_lon(interp_like_data.latitude.values, interp_like_data.longitude.values)

            regridded_data = (data*area_0_05).groupby_bins("lon", coords["lon"], right = False).sum().groupby_bins("lat", coords["lat"], right = False).sum()/area_0_25

            regridded_data["lat_bins"] = coords["lat"][:-1]
            regridded_data["lon_bins"] = coords["lon"][:-1]

            regridded_data =  regridded_data.rename({"lat_bins":"lat", "lon_bins":"lon"})
            regridded_data.Tree_Broadleaf_Evergreen.plot()
        
    return regridded_data