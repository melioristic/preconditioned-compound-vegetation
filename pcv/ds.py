#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# Created by : Mohit Anand
# Created on : Sat Aug 06 2022 at 12:38:54 PM
# ==========================================================
# Created on Sat Aug 06 2022
# __copyright__ = Copyright (c) 2022, PCV Project
# __credits__ = [Mohit Anand,]
# __license__ = Private
# __version__ = 0.0.0
# __maintainer__ = Mohit Anand
# __email__ = itsmohitanand@gmail.com
# __status__ = Development
# ==========================================================

# Script for datastructures 

import xarray as xr
import numpy as np
import cartopy.io.shapereader as shpreader


def create_xr_dataset(model, lat, lon):
    model_data_dict = {}
    
    var_list = _create_xr_variable_list(model)
    metric_list = model.inspect().columns[3:]

    xr_dict_list = _permute_list(var_list, metric_list)
    lat =  lat.values
    lon = lon.values
    for each in xr_dict_list:
        model_data_dict[each] = (
                ("lat", "lon"), np.full((lat.shape[0], lon.shape[0]), np.nan))
    
    model_data_dict["chi2p"] = (
                ("lat", "lon"), np.full((lat.shape[0], lon.shape[0]), np.nan))

    coords= {"lat":lat, "lon":lon}

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
