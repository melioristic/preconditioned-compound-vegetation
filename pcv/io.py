#
# Created on Wed Jul 20 2022
#
# Copyright (c) 2022 Your Company
#

## The script for all the input and output files
from pcv.process import comp_area_lat_lon
import xarray as xr
import numpy as np

from sklearn.model_selection import train_test_split

def read_ipcc_region_csv(path="/data/compoundx/anand/PCV/data/gat_data/low/crop_Tibetan-Plateau_n_1539.csv") -> None:
    
    data = np.loadtxt(path)
    data = data[~np.isnan(data).any(axis=1), :][:,:,np.newaxis]
    train_data, test_data = train_test_split(data, test_size=0.1, train_size=0.9, shuffle=True)

    train_data, val_data = train_test_split(train_data, test_size=0.1, train_size=0.9, shuffle=True)
        
    return train_data, val_data, test_data