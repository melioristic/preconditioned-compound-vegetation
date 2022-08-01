#fix regex
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
library(rnaturalearth)
#======================================================================
#Load directories
dir_root <-"C:/Users/rhd630/Desktop/PhD/damocles_summer_school/"
dir_data <- file.path(dir_root, "data")
ipcc_data <-file.path(dir_data, "IPCC-WGI-reference-regions-v4_shapefile")
#======================================================================
#load world map
world <- ne_countries(scale = 'small', returnclass = 'sf') %>% 
  dplyr::select(geometry)

#load climate zones
climate_zones <-list.files(dir_data, "climate_zone_masks.nc", full.names = TRUE) %>% 
  st_read()

#load LU types
mask_forest <-list.files(dir_data, "mask_tree_shrubs_sum", full.names = TRUE) %>% 
  read_stars() %>% 
  setNames("mask_nc")

mask_crop <-list.files(dir_data, "mask_crops", full.names = TRUE) %>% 
  read_stars()%>% 
  setNames("mask_nc")

#Load model output as df
model_out_estimate <-list.files(dir_data, "sem_data_2", full.names = TRUE) %>% 
  read_stars() %>% 
  as.data.frame() %>% 
  drop_na() %>% 
  tibble() %>% 
  pivot_longer(-c(x,y)) %>% 
  filter_at(.vars= vars(name), all_vars(grepl('Estimate',.))) %>% 
  mutate(name = sub("(.*?_.*?_.*?)_.*", "\\1", name)) 
  


model_out_pval <-list.files(dir_data, "sem_data_2", full.names = TRUE) %>% 
  read_stars() %>% 
  as.data.frame() %>% 
  drop_na() %>% 
  tibble() %>% 
  pivot_longer(-c(x,y)) %>% 
  filter_at(.vars= vars(name), all_vars(grepl('_p.value',.))) %>% 
  mutate(name = sub("(.*?_.*?_.*?)_.*", "\\1", name)) %>% 
  filter(value <= 0.05)

#Load model output as nc
model_out_nc <-list.files(dir_data, "sem_data_2", full.names = TRUE) %>% 
  read_stars() 
#======================================================================
st_crs(mask_crop) <- st_crs(world)
st_crs(mask_forest) <- st_crs(world)
st_crs(model_out_nc) <- st_crs(world)
#======================================================================
get_mask <- function(mask, thrs, climate_zone){
  
  (mask > thrs)%>% 
    st_join(climate_zones %>% 
              filter(Acronym == climate_zone)) %>% 
    st_as_sf() %>% 
    filter(mask_nc == TRUE) %>% 
    dplyr::select(geometry)
  
}
#-----------------------------------------------------
mask_nc <-function(nc_file,mask){
  
  name <- as.character(ensym(mask))
  
 split_string <- str_split(name, fixed("_"))
  

  return_file <-nc_file %>% 
    st_crop(mask) %>% 
    as.data.frame() %>% 
    drop_na() %>% 
    tibble() %>% 
    mutate(Climate_zone := !!split_string[[1]][1],
           Land_cover := !!split_string[[1]][3])
  

    return(return_file)
}

#======================================================================

NEU_mask_crop <-get_mask(mask_crop,0.5,"NEU")
WCE_mask_crop <-get_mask(mask_crop,0.5,"WCE")
MED_mask_crop <-get_mask(mask_crop,0.5,"MED")

NEU_mask_forest <-get_mask(mask_forest,0.5,"NEU")
WCE_mask_forest <-get_mask(mask_forest,0.5,"WCE")
MED_mask_forest <-get_mask(mask_forest,0.5,"MED")

#======================================================================
#post-processing and maps
map_plot <-function (variable){

    p1 <-model_out_estimate %>% 
    filter(name == variable) %>% 
    ggplot()+
    geom_tile(aes(x=x,y=y, fill = value))+
    geom_point(data =model_out_pval %>% 
                 filter(name == variable) ,aes(x=x,y=y),
               color = "black",
               size = 0.0001,
               alpha = 0.3)+
    geom_sf(data = world, fill = "transparent", colour = "black")+
    geom_sf(data = climate_zones, fill = "transparent", colour = "black", size = 1)+
    coord_sf(xlim = c(-10, 45), ylim = c(30, 73), expand = FALSE)+
    theme_bw()+
    ggtitle(label = variable)+
    ylab("")+
    xlab("")+
    scale_fill_continuous_diverging("Blue-Red 3")+
    theme(element_blank(),
          legend.title=element_blank())
  
}
#======================================================================
NEU_crop_df <-mask_nc(model_out_nc,NEU_mask_crop) %>% 
  mutate(Climate_zone = "NEU",
         Land_cover  = "Crop")

WCE_crop_df <-mask_nc(model_out_nc,WCE_mask_crop) %>% 
  mutate(Climate_zone = "WCE",
         Land_cover  = "Crop")

MED_crop_df <-mask_nc(model_out_nc,MED_mask_crop) %>% 
  mutate(Climate_zone = "MED",
         Land_cover  = "Crop")

NEU_forest_df <-mask_nc(model_out_nc,NEU_mask_forest) %>% 
  mutate(Climate_zone = "NEU",
         Land_cover  = "Forest")

WCE_forest_df <-mask_nc(model_out_nc,WCE_mask_forest) %>% 
  mutate(Climate_zone = "WCE",
         Land_cover  = "Forest")

MED_forest_df <-mask_nc(model_out_nc,MED_mask_forest) %>% 
  mutate(Climate_zone = "MED",
         Land_cover  = "Forest")

coef_summary_df <-bind_rows(NEU_crop_df,WCE_crop_df,MED_crop_df,
          NEU_forest_df,WCE_forest_df,MED_forest_df) %>% 
    tibble() %>% 
   pivot_longer(-c(x,y,Climate_zone, Land_cover))  %>% 
  filter_at(.vars= vars(name), all_vars(grepl('Estimate',.))) %>% 
  mutate(name = sub("(.*?_.*?_.*?)_.*", "\\1", name)) %>% 
  mutate(Climate_zone = recode_factor(Climate_zone,
                                      NEU = "NEU",
                                      WCE = "WCE",
                                      MED = "MED"))

mean_coef <-coef_summary_df %>% 
 # filter_at(.vars= vars(name), all_vars(grepl('Estimate',.))) %>% 
  group_by(Climate_zone,Land_cover,name) %>% 
  summarise_at(vars(value),mean) %>% 
  rename(mean = value) 
  
#======================================================================
coef_plot <- function(variable){
  
  p1 <-coef_summary_df %>% 
    inner_join(mean_coef) %>% 
   # mutate(name = sub("(.*?_.*?)_.*", "\\1", name)) %>% 
    filter(name == variable) %>% 
    ggplot() +
    geom_density(aes(value, fill = mean))+
    facet_grid(Climate_zone~Land_cover)+
    theme_bw(base_size = 15)+
    ylab("")+
    xlab("")+
    geom_vline(xintercept = 0, linetype = "dashed", size = 1)+
    scale_fill_continuous_diverging("Blue-Red 3")
  

}
#======================================================================
var_name <-model_out_estimate$name %>%  unique()
var_name
a<-map_plot(var_name[[1]])
b<-coef_plot(var_name[[1]])

library(patchwork)

a + b
