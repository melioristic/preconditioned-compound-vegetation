#======================================================================
#clean workspace
rm(list = ls())
graphics.off()
gc()
#======================================================================
#load directory
dir_root <- "C:/Users/rhd630/Desktop/PhD/damocles_summer_school"
dir_data <- file.path(dir_root, "data")
dir_climate <-file.path(dir_data, "climate")
#======================================================================
#load libraries
library(tidyverse)
library(raster)
library(sf)
library(lubridate)
library(colorspace)
#======================================================================
#setup the loop
#======================================================================
#vector of variable names
var_names <- c("t2m")
#----------------------------------------------------------------------
#list to store variables
var_list <- vector('list', length(var_names))
#add names for each variable
names(var_list) <- var_names
#list to store all detrended climate variables
climate_list_dtr<- var_list
#======================================================================
#loop over various climate variables
#======================================================================
#loop over various variables
for (var_name in var_names) {
  climate_list_dtr[[match(var_name, var_names)]] <-
    list.files(dir_climate, var_name, full.names = TRUE) %>%
    brick() %>%
    rasterToPoints() %>%
    as_tibble() %>%
    rename_all( ~ (str_replace(., "X", ""))) %>%
    pivot_longer(cols = -c(x, y)) %>%
    mutate(
      date = lubridate::ymd(as.character(name)),
      year = lubridate::year(date),
      month = lubridate::month(date)
    ) %>%
    #main processing steps
    group_by(x, y) %>%
    nest() %>%
    mutate(model_trend = map(data,  ~ lm(value ~ year, data = .))) %>%
    mutate(augment_trend  = map(model_trend,  ~ broom::augment(.))) %>%
    mutate(date  = map(data,  ~ .$date)) %>%
    unnest(cols = c(augment_trend, date)) %>%
    ungroup() %>%
    dplyr::select(x, y,.resid,data) %>%
    unnest(cols = c(data)) %>%
    group_by(x, y, month) %>%
    mutate_at(vars(.resid),
              ~ scale(., center = TRUE, scale = TRUE)) %>%
    ungroup()
}

#==============================
#==============================
#==============================
#==============================
#FOR EXPLAINING
#vector of variable names
var_name <- c("t2m")
#example list
example_test <- var_list
#give subsample coordinates
x_min <-25
x_max <-30
y_min <-35
y_max <-40
#create example test
example_test[[match(var_name,var_names)]] <-
  list.files(dir_climate, var_name, full.names = TRUE) %>%
  brick() %>%
  rasterToPoints() %>%
  as_tibble() %>%
  rename_all(~ (str_replace(., "X", ""))) %>%
  pivot_longer(cols = -c(x, y)) %>% 
  filter(x > x_min & x < x_max & y > y_min & y < y_max)

#run code over subsample
example_subset <-example_test$t2m %>% 
  mutate(
    date = lubridate::ymd(as.character(name)),
    year = lubridate::year(date),
    month = lubridate::month(date)
  ) %>%
  group_by(x, y) %>%
  nest() %>%
  mutate(model_trend = map(data,  ~ lm(value ~ year, data = .))) %>%
  mutate(augment_trend  = map(model_trend,  ~ broom::augment(.))) %>%
  mutate(date  = map(data,  ~ .$date)) %>%
  unnest(cols = c(augment_trend, date)) %>%
  ungroup() %>%
  dplyr::select(x, y,.resid,data) %>%
  unnest(cols = c(data)) %>%
  group_by(x, y, month) %>%
  mutate_at(vars(.resid),
            ~ scale(., center = TRUE, scale = TRUE)) %>%
  ungroup()

#quick plot
example_subset %>%  
  ggplot(aes(x=x,y=y,fill =.resid))+
  geom_raster()+
  facet_grid(~month)+
  scale_fill_continuous_diverging("Blue-Red 2")
