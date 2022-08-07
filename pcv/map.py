#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# Created by : Mohit Anand
# Created on : Sun Aug 07 2022 at 1:52:51 PM
# ==========================================================
# Created on Sun Aug 07 2022
# __copyright__ = Copyright (c) 2022, PCV Project
# __credits__ = [Mohit Anand,]
# __license__ = Private
# __version__ = 0.0.0
# __maintainer__ = Mohit Anand
# __email__ = itsmohitanand@gmail.com
# __status__ = Development
# ==========================================================

# Script for all the plots
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.feature import ShapelyFeature
import matplotlib.pyplot as plt
import numpy as np
import cartopy.io.shapereader as shpreader
from pcv.cfg import IPCC_REGION_SHPFILE 


class SEMMap(object):
    def __init__(self, sem_data) -> None:
        self.sem_data = sem_data
        self.ipcc_regions = shpreader.Reader(IPCC_REGION_SHPFILE)

    def lai_summer_map(self, fpath):
        
        lon = self.sem_data.lon.values
        lat = self.sem_data.lat.values
        
        key_list = list(self.sem_data.keys())
        name_list = [key_list[i] for i in range(len(key_list)) if ("lai_summer" in key_list[i].split("~")[0]) and ("Estimate" in key_list[i]) and (len(key_list[i].split("~"))==2)]
        n_plots = len(name_list)
        
        fig, ax = plt.subplots(n_plots+1, 1, figsize = (14, 3*n_plots), 
                subplot_kw={'projection': ccrs.PlateCarree()})

        shape_feature_list = self._generate_shape_feature()
            
        for i, name in enumerate(name_list):
            valE = self.sem_data[name][:,:].to_numpy()
            valP = self.sem_data[name.replace("Estimate", "p-value")].to_numpy()

            cs1 = ax[i].contourf(lon, lat, valE, cmap='coolwarm',  transform=ccrs.PlateCarree())
            ax[i].contourf(lon, lat, valP, levels=[0, 0.05, 1.0],  hatches = ["...", ""], alpha=0)
            self._add_features(ax[i], shape_feature_list)

            ax[i].coastlines()
            ax[i].set_title(name)

        val = self.sem_data["chi2p"][:,:].to_numpy()
        cs2= ax[-1].contourf(lon, lat, val, cmap='magma_r',  transform=ccrs.PlateCarree())
        ax[-1].coastlines()
        ax[-1].set_title("chi2 p-value of the model")

        cbar1_ax = fig.add_axes([0.93, 0.12, 0.02, 0.75])
        cbar2_ax = fig.add_axes([0.17, 0.05, 0.70, 0.02])

        cbar1=fig.colorbar(cs1, cax=cbar1_ax,orientation='vertical')
        cbar2=fig.colorbar(cs2, cax=cbar2_ax,orientation='horizontal')

        plt.subplots_adjust(hspace=0.3)
        plt.suptitle("Summmer LAI relationships")
        plt.savefig(fpath)

    def _add_features(self, ax, shape_feature_list):
        for shape_feature in shape_feature_list:
            ax.add_feature(shape_feature)

    def _generate_shape_feature(self):
        shape_feature_list = []
        for i, records in enumerate(self.ipcc_regions.records()):
            shape_feature = ShapelyFeature([records.geometry], ccrs.PlateCarree(), facecolor = "None", edgecolor='black', lw=1)
            shape_feature_list.append(shape_feature)
        
        return shape_feature_list
