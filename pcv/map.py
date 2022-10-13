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
from pcv.mapaux import chi_cmap, make_colorbar, p1, p3_1
from shapely.geometry import Point, Polygon
import os
import seaborn.apionly as sns
import xarray as xr
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import copy

class SEMMap(object):
    def __init__(self, sem_data) -> None:
        self.sem_data = sem_data
        self.ipcc_regions = shpreader.Reader(IPCC_REGION_SHPFILE)
        self.lat = self.sem_data.lat
        self.lon = self.sem_data.lon


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
        for name, shape_feature, centroid in shape_feature_list:

            ax.add_feature(shape_feature, linestyle = ":")
            if 75>centroid[1]>25 and name!="N.Pacific-Ocean":
                ax.text(centroid[0], centroid[1], name, color='k', size=11, ha='center', va='center', wrap = True,  transform=ccrs.PlateCarree())

    def _generate_shape_feature(self):
        shape_feature_list = []
        for i, records in enumerate(self.ipcc_regions.records()):
            shape_feature = ShapelyFeature([records.geometry], ccrs.PlateCarree(), facecolor = "None", edgecolor='black', lw=1)
            shape_feature_list.append((records.attributes["Name"], shape_feature, (records.geometry.centroid.x, records.geometry.centroid.y) ))

        return shape_feature_list

    def _write_clim_mask(self,  path = "/data/compoundx/anand/PCV/data/clim_mask/"):
        
        print("writing climate mask, to be used later. This function should not be called again and again")
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

    def group_clim(self, name, img_path):

        valE = self.sem_data[name][:,:].to_numpy()
        
        valP = self.sem_data[name.replace("Estimate", "p-value")].to_numpy()

        fig, fax1 = self.plot_clim_lu_group(valE)

        fax1.contourf(self.sem_data.lon, self.sem_data.lat, valP, levels=[0, 0.05, 1.0],  hatches = ["...", ""], alpha=0) # p-val 0.05

        plt.savefig(img_path)
        plt.close()

    def lu_mask(self):

        lu_mc_1 = self._majority_class_1_landuse()

        last_year_lu = lu_mc_1[-1,:,:]
        
        mask_forest = ((last_year_lu>=40) & ((last_year_lu<110)))
        mask_crop = ((last_year_lu>=10) & ((last_year_lu<40)))

        # Just to check 
        # plt.imshow(mask_crop)
        # plt.savefig("crop.png")

        return mask_forest, mask_crop

    def _read_land_use(self, year):
        if year < 2016:
            version = "2.0.7cds"
        else:
            version = "2.1.1"

        file_name = f"/data/compoundx/anand/PCV/data/CCI-LC/ESACCI-LC-L4-LCCS-Map-300m-P1Y-aggregated-0.500000Deg-{year}-v{version}.nc"
        return xr.open_dataset(file_name)

    
    def _majority_class_1_landuse(self):
        val = []
        for i in range(1992, 2019):
            data = self._read_land_use(i)
            val.append(data.interp(lat = self.lat, lon = self.lon, method = "nearest").majority_class_1.data)

        majority_class_1 = np.stack(val)

        lu_mc_1 = xr.DataArray(
            majority_class_1, dims = ["time", "lat", "lon"], coords = {
                "time" : np.arange(1992, 2019),
                "lat" : self.lat.data,
                "lon" : self.lon.data,
            }
        )
        return lu_mc_1


    def path_map(self, piping, img_path):
        
        max_min = 1
        if isinstance(piping, list):
            valE = self._get_piping_val(piping[0])
            for each_piping in piping[1:]:
                valE += self._get_piping_val(each_piping)
            max_min = 0.2
        else:
            valE = self._get_piping_val(piping)

        

        fig, ax_head = self.plot_clim_lu_group(valE, max_min=max_min)
        plt.savefig(img_path)
        plt.close()

    def _get_piping_val(self, piping):
        graph_list = piping.split("|>")

        valE = np.ones_like(self.sem_data["chi2p"].data)
        for i in range(len(graph_list)-1):
            name = graph_list[i+1].replace(" ", "") + "~" + graph_list[i].replace(" ", "") + "_Estimate"
            valE = valE* self.sem_data[name].data

        # max_min = (1/10)**((len(graph_list)-1)//2)

        return valE

    def plot_clim_lu_group(self, valE, max_min = 1.0, n=1):

        clim_mask_path = "/data/compoundx/anand/PCV/data/clim_mask/"
        clim_files = [clim_mask_path + file for file in os.listdir(clim_mask_path) if ".npy" in file ]
        # clim_list = ["N.W.North-America", "N.Central-America", "N.Europe", "E.Europe", "Russian-Far-East" ]
        # clim_files = [clim_mask_path + file + ".npy" for file in clim_list ]

        lon = self.sem_data.lon.values
        lat = self.sem_data.lat.values
        
        shape_feature_list = self._generate_shape_feature()

        fig = plt.figure(constrained_layout=True, figsize=(20,20))
        gs = fig.add_gridspec(6, 5)
        fax1 = fig.add_subplot(gs[0, :], projection=ccrs.PlateCarree())

        valE_cut = copy.deepcopy(valE) 
        valE_cut[valE_cut>1]=1.0
        valE_cut[valE_cut<-1]=-1.0

        cs1 = fax1.contourf(lon, lat, valE_cut, cmap='coolwarm', levels = np.linspace(-max_min, max_min, 9))
        fax1.coastlines(color = "gray", linewidth = 0.4)
        self._add_features(fax1, shape_feature_list)

        cbaxes = inset_axes(fax1, width="1%", height="50%", loc=3) 

        cbar1=fig.colorbar(cs1, cax=cbaxes,orientation='vertical')

        mask_forest, mask_crop = self.lu_mask()

        i = 0
        for _, files in enumerate(clim_files):
            mask_clim = np.load(files)
            
            if sum(sum(mask_clim)) > 10 :
                
                all_data = valE[mask_clim==True]
                forest_data = valE[(mask_clim==True) & (mask_forest==True)]
                crop_data = valE[(mask_clim==True) & (mask_crop==True)]
                
                # SHOULD GIVE THE SAME RESULT
                # #forest_data = self.sem_data[name].where(mask_clim==True).where(mask_forest==True).values
                # crop_data = self.sem_data[name].where(mask_clim==True).where(mask_crop==True).values
                # forest_data = forest_data[~np.isnan(forest_data)].reshape(-1)
                # crop_data = crop_data[~np.isnan(crop_data)].reshape(-1)
                # all_data = all_data[~np.isnan(all_data)].reshape(-1)
                
                r = i//5 + 1 
                c = i%5
                i+=1            
                ax = fig.add_subplot(gs[r, c])
                # sns.histplot(forest_data, ax = ax, kde = True, color = p3_1["blue"], alpha = 0.5)
                # sns.histplot(crop_data, ax = ax, kde = True, color = p3_1["green"], alpha = 0.5)
                # sns.histplot(all_data, ax = ax, kde = True, color = p3_1["orange"], alpha = 0.5)
                sns.kdeplot(all_data, ax = ax, color = "k", label = "Total")
                sns.kdeplot(crop_data, ax = ax, color = p3_1["orange"], alpha = 0.5, fill = True, label = "Crop")
                sns.kdeplot(forest_data, ax = ax, color = p3_1["green"], alpha = 0.5, fill = True, label = "Forest")
                
                
                ax.legend()
                # ax.axvline(np.mean(data), color = "r", linestyle = "--")
                # ax.hist(data[~np.isnan(data)].reshape(-1))
                ax.set_xlim(-max_min, max_min)
                ax.set_xlabel(files.split("/")[-1][:-3])

        return fig, fax1