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
from pcv.mapaux import chi_cmap, make_colorbar, p1
from shapely.geometry import Point, Polygon
import os
import seaborn.apionly as sns


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
            max_min = 1.0

            valE[valE>1.0] = 1.0
            valE[valE<-1.0] = -1.0

            cs1 = ax[i].contourf(lon, lat, valE, cmap='coolwarm',  transform=ccrs.PlateCarree(), levels = np.linspace(-max_min, max_min, 9))
            ax[i].contourf(lon, lat, valP, levels=[0, 0.05, 1.0],  hatches = ["...", ""], alpha=0)
            self._add_features(ax[i], shape_feature_list)

            ax[i].coastlines()
            ax[i].set_title(name)

        val = self.sem_data["chi2p"][:,:].to_numpy()


        cs2= ax[-1].contourf(lon, lat, val,cmap = chi_cmap[0], transform=ccrs.PlateCarree())
        self._add_features(ax[-1], shape_feature_list)

        ax[-1].coastlines()
        ax[-1].set_title("chi2 p-value of the model")

        cbar1_ax = fig.add_axes([0.93, 0.12, 0.02, 0.75])
        cbar2_ax = fig.add_axes([0.17, 0.05, 0.70, 0.02])

        cbar1=fig.colorbar(cs1, cax=cbar1_ax,orientation='vertical')
        cbar2= make_colorbar(fig, cbar2_ax, chi_cmap, label= "p-val of the SEM") 

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

    def _write_clim_mask(self,  path = "/data/compoundx/anand/PCV/data/clim_mask/"):

        long, latg =  np.meshgrid(self.sem_data.lon, self.sem_data.lat)
        lat1d = latg.reshape(-1)
        lon1d = long.reshape(-1)

        print(long.shape)
        print(latg.shape)
        for i, records in enumerate(self.ipcc_regions.records()):
            print(i)
            a = np.array([Point(x, y) for x, y in zip(lon1d, lat1d)], dtype=object)
            mask = np.array([records.geometry.contains(point) for point in a])
            mask = mask.reshape(long.shape)
            print(mask.shape)
            print(sum(sum(mask)))
            print(records.attributes["Name"])
            np.save(path+records.attributes["Name"].replace("/", "|")+".npy", mask)

    def group_clim(self):
        clim_mask_path = "/data/compoundx/anand/PCV/data/clim_mask/"
        clim_files = [clim_mask_path + file for file in os.listdir(clim_mask_path) if ".npy" in file ]
        
        lon = self.sem_data.lon.values
        lat = self.sem_data.lat.values

        fig = plt.figure(constrained_layout=True, figsize=(15,15))
        gs = fig.add_gridspec(6, 5)
        fax1 = fig.add_subplot(gs[0, :])
        
        name = "lai_summer~swvlall_summer_Estimate"
        valE = self.sem_data[name][:,:].to_numpy()

        max_min = 1.0
        fax1.contourf(lon, lat, valE, cmap='coolwarm', levels = np.linspace(-max_min, max_min, 9))

        i = 0
        for _, files in enumerate(clim_files):
            mask = np.load(files)
            
            if sum(sum(mask)) :
                print(i)
                data = self.sem_data[name].where(mask==True).values
                data = data[~np.isnan(data)].reshape(-1)
                r = i//5 + 1 
                c = i%5
                i+=1            

                ax = fig.add_subplot(gs[r, c])
                sns.histplot(data, ax = ax, kde = True, color = p1["blue"], element = "step", bins = 20)
                ax.axvline(np.mean(data), color = "r", linestyle = "--")
                # ax.hist(data[~np.isnan(data)].reshape(-1))
                ax.set_xlim(-1, 1)
                ax.set_xlabel(files.split("/")[-1][:-3])

        plt.savefig(f"{name}_clim.png")
        plt.close()

