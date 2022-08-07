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
import cartopy as cp
import matplotlib.pyplot as plt


class SEMMap(object):
    def __init__(self, sem_data) -> None:
        self.sem_data = sem_data
        self.lai_summer_map("scratch.png")
    
    def lai_summer_map(self, fpath):
        
        lon = self.sem_data.lon.values
        lat = self.sem_data.lat.values

        
        
        
        key_list = list(self.sem_data.keys())
        name_list = [key_list[i] for i in range(len(key_list)) if ("lai_summer" in key_list[i].split("~")[0]) and ("Estimate" in key_list[i]) and (len(key_list[i].split("~"))==2)]
        n_plots = len(name_list)
        
        
        fig, ax = plt.subplots(n_plots+1, 1, figsize = (14, 3*n_plots), 
                subplot_kw={'projection': ccrs.PlateCarree()})

        for i, name in enumerate(name_list):
            val = self.sem_data[name][:,:].to_numpy()
            cs1 = ax[i].contourf(lon, lat, val, cmap='coolwarm',  transform=ccrs.PlateCarree())
            ax[i].coastlines()
            ax[i].set_title(name)

        val = self.sem_data["chi2p"][:,:].to_numpy()
        cs2= ax[-1].contourf(lon, lat, val, cmap='magma_r',  transform=ccrs.PlateCarree())
        ax[-1].coastlines()
        ax[-1].set_title("chi2 p-value")

        cbar1_ax = fig.add_axes([0.93, 0.12, 0.02, 0.75])
        cbar2_ax = fig.add_axes([0.17, 0.05, 0.70, 0.02])

        cbar=fig.colorbar(cs1, cax=cbar1_ax,orientation='vertical')
        cbar=fig.colorbar(cs2, cax=cbar2_ax,orientation='horizontal')

        plt.subplots_adjust(hspace=0.5)
        plt.suptitle("Summmer LAI relationships")
        plt.savefig(fpath)