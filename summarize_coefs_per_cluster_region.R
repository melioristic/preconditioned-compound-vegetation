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
#======================================================================
st_crs(stars_LU_tree) <- st_crs(clim_EU)
#======================================================================
stars_LU_tree =  list.files(dir_data,
                            "sem_data_1",
                            full.names = TRUE,
                            recursive = TRUE) %>% 
  read_stars() %>% 
  st_redimension() 

clim_EU_coef <-stars_LU_tree%>% 
  st_crop(clim_EU[3,]) %>% 
  as.data.frame() %>% 
  drop_na() %>% 
  rename(value = 4)


clim_EU_coef %>% 
  dplyr::select(-x,-y) %>% 
  filter(new_dim != "chi2p") %>% 
  ggplot()+
  geom_density(aes(x=value))+
  geom_vline(xintercept = 0)+
  facet_grid(~new_dim)+
  ggtitle(label = "Med")+
  theme_classic(base_size = 15)
