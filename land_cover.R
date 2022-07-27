#include script to load custom functions
#======================================================================
#clean workspace
rm(list = ls())
graphics.off()
gc()
#======================================================================
#load libraries
library(tidyverse)
library(raster)
library(sf)
library(stars)
library(colorspace)
#======================================================================
#Load directories
dir_root <-"C:/Users/rhd630/Desktop/PhD/damocles_summer_school/"
dir_data <- file.path(dir_root, "data")
ipcc_data <-file.path(dir_data, "IPCC-WGI-reference-regions-v4_shapefile")
#======================================================================
climate_zones <-list.files(ipcc_data,"shp",full.names = TRUE, recursive = TRUE) %>%
  st_read()

clim_EU <-climate_zones %>% 
  filter(Continent %in% c("EUROPE","EUROPE-AFRICA")) %>% 
  filter(Acronym != "EEU")
#======================================================================
stars_LU_tree =  list.files(dir_data,
                       "LU_2018",
                       full.names = TRUE,
                       recursive = TRUE) %>% 
  read_stars() %>% 
  dplyr::select(starts_with("Tree"),starts_with("Shrub")) %>% 
  st_redimension(along = list(land_type = names(.))) %>% 
  set_names("Tree Type") 
#======================================================================
stars_LU_crop =  list.files(dir_data,
                            "LU_2018",
                            full.names = TRUE,
                            recursive = TRUE) %>% 
  read_stars() %>% 
  dplyr::select(starts_with("Crops")) %>% 
  st_redimension(along = list(land_type = names(.))) %>% 
  set_names("Crop")
#======================================================================
stars_LU_full =  list.files(dir_data,
                            "LU_2018",
                            full.names = TRUE,
                            recursive = TRUE) %>% 
  read_stars() %>% 
  dplyr::select(-c(starts_with("majority_class"),"NoData","change_count")) %>% 
  st_redimension(along = list(land_type = names(.))) %>% 
  set_names("Land Type")
#======================================================================
#sum over variables
stars_LU_full_sum <-stars_LU_full %>% 
  st_apply(c("x","y"),sum) 

stars_LU_tree_sum <-stars_LU_tree %>% 
  st_apply(c("x","y"),sum)

ratio_tree_to_crop <- stars_LU_tree_sum-stars_LU_crop
#======================================================================
#create crop and tree mask
stars_tree_crop_mask <-
  stars_LU_tree_sum %>%
  set_names("Tree") %>%
  st_join(stars_LU_crop) %>%
  st_redimension(along = list(land_type = names(.))) 
#======================================================================
#adjust crs
st_crs(stars_tree_crop_mask) <- st_crs(clim_EU)

#filter based on fraction LU
stars_tree_crop_mask_filtered <-stars_tree_crop_mask > 0.5

#masks per climate zone
NEU_mask <-stars_tree_crop_mask_filtered %>% 
  st_join(clim_EU[1,]) 

WCE_mask <-stars_tree_crop_mask_filtered %>% 
  st_join(clim_EU[2,]) 

MED_mask <-stars_tree_crop_mask_filtered %>% 
  st_join(clim_EU[3,]) 
#======================================================================
ggplot()+
  geom_stars(data=stars_tree_crop_mask)+
  geom_sf(data=clim_EU, fill = "transparent", color = "black", size  = 2)+
  facet_grid(~land_type)+
  xlab("")+
  ylab("")+
  theme_classic(base_size = 15)+
  scale_fill_continuous_sequential("Reds 3")+
  labs(fill="Fraction [%]")
#======================================================================
write_stars(stars_tree_crop_mask, "mask_crop_vs_tree_and_shrubs.nc")
write_sf(clim_EU, "climate_zone_masks.nc")
write_stars(stars_LU_crop, "mask_crops.nc")


