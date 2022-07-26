#include script to load custom functions
#======================================================================
#clean workspace
rm(list = ls())
graphics.off()
gc()
#======================================================================
#load libraries
library(lavaan)
library(piecewiseSEM)
library(tidyverse)
library(ggraph)
library(ggpubr)
library(raster)
#======================================================================
#Load directories
dir_root <-"C:/Users/rhd630/Desktop/PhD/damocles_summer_school/"
dir_in <- file.path(dir_root, "data")
#======================================================================
#Plot a fitted lavaan object
ggsem <- function(fit, layout = "sugiyama") {
  
  # Extract standardized parameters
  params <- lavaan::standardizedSolution(fit)
  
  # Edge properties
  
  #ADJUST PVALUE TO SEE WHEN TO INCL. NODES
  param_edges <- params %>% 
    filter(op %in% c("=~", "~", "~~"), lhs != rhs, pvalue <= 1) %>%
    transmute(to = lhs,
              from = rhs,
              val = est.std,
              type = dplyr::case_when(
                op == "=~" ~ "loading",
                op == "~"  ~ "regression",
                op == "~~" ~ "correlation",
                TRUE ~ NA_character_))
  
  # Identify latent variables for nodes
  latent_nodes <- param_edges %>% 
    filter(type == "loading") %>% 
    distinct(to) %>% 
    transmute(metric = to, latent = TRUE)
  
  # Node properties
  param_nodes <- params %>% 
    filter(lhs == rhs) %>% 
    transmute(metric = lhs, e = est.std) %>% 
    left_join(latent_nodes) %>% 
    mutate(latent = if_else(is.na(latent), FALSE, latent))
  
  # Complete Graph Object
  param_graph <- tidygraph::tbl_graph(param_nodes, param_edges)
  
  # Plot
  ggraph(param_graph, layout = layout) +
    # Latent factor Nodes
    geom_node_point(aes(alpha = as.numeric(latent)),
                    shape = 16, size = 5) +
    geom_node_point(aes(alpha = as.numeric(latent)),
                    shape = 16, size = 4, color = "white") +
    # Observed Nodes
    # CHANGE NODE SHAPE
    
    geom_node_point(aes(alpha = as.numeric(!latent)),
                    shape = 16, size = 5,color = "darkgray") +
    # geom_node_point(aes(alpha = as.numeric(!latent)),
    #                 shape = 15, size = 4, color = "white") +
    
    # Regression Paths (and text)
    geom_edge_link(aes(color = val, label = round(val, 2),
                       alpha = as.numeric(type == "regression")),
                   linetype = 1, angle_calc = "along", vjust = -.5,
                   arrow = arrow(20, unit(.3, "cm"), type = "closed")) +
    # Factor Loadings (no text)
    geom_edge_link(aes(color = val, alpha = as.numeric(type == "loading")),
                   linetype = 3, angle_calc = "along",
                   arrow = arrow(20, unit(.3, "cm"), ends = "first", type = "closed")) +
    # Correlation Paths (no text)
    geom_edge_link(aes(color = val,alpha = as.numeric(type == "correlation")),
                   linetype = 2, angle_calc = "along",
                   arrow = arrow(20, unit(.3, "cm"), type = "closed", ends = "both")) +
    # Node names
    
    #HERE CHANGE NUDE_Y FOR WHERE TO PLOT NAME IN FIGURE
    geom_node_text(aes(label = metric),
                   nudge_y = .15, hjust = "inward", size =3) +
    
    # Node residual 
    # geom_node_text(aes(label = sprintf("%.2f", e)),
    #                nudge_y = -.1, size = 3) +
    
    # Scales and themes
    scale_alpha(guide = FALSE, range = c(0, 1)) +
    scale_edge_alpha(guide = FALSE, range = c(0, 1)) +
    scale_edge_colour_gradient2(guide = FALSE, low = "blue", mid = "gray", high = "red") +
    scale_edge_linetype(guide = FALSE) +
    scale_size(guide = FALSE) +
    theme_graph()
}
#------------------------------------------------------------------------------------
predicty.lavaan = function(object, newdata, xnames, ynames){
  # predict function for computing predicted values for set of response variables
  # given a set of predictor variables
  # based on the joint distribution estimated by a SEM model
  # INPUT
  # object: lavaan output object obtained from sem()
  # newdata: data frame with new values for the predictors
  # xnames: variables designated as predictors
  # ynames: variables designated as response variables
  
  #
  Sxx = fitted(object)$cov[xnames , xnames]
  Sxy = fitted(object)$cov[xnames , ynames]
  mx = fitted(object)$mean[xnames]
  my = fitted(object)$mean[ynames]
  
  #
  Xtest = as.matrix(newdata[, xnames])
  Xtest = scale(Xtest, center = mx, scale = FALSE)
  yhat = matrix(my, nrow = nrow(Xtest), ncol = length(ynames), byrow = TRUE) + Xtest %*% solve(Sxx) %*% Sxy
  
  # return
  return(yhat)
}
#------------------------------------------------------------------------------------
#leave-one-out function
fun_loo_per_grid <- function(x,model_structure){
  
  predictions <-rep(NA, length(x$yield_anomaly))
  List_year <-unique(x$year)
  
  for (i in 1:length(List_year)){
    
    x_names <-c("SMroot_summer","edd35_summer") 
    y_names <-"yield_anomaly"
    
    Training_i <- x[x$year!=List_year[i],]
    Test_i <- x[x$year==List_year[i],]
    Mod_i <- sem(model_structure,data =Training_i,estimator = "MLM",std.lv = TRUE, meanstructure = TRUE)
    Y_lm_i <- predicty.lavaan(Mod_i, newdata = Test_i,xnames =x_names , ynames = y_names)
    predictions[x$year==List_year[i]] <-Y_lm_i
    
    
  }
  return(predictions) 
}
#------------------------------------------------------------------------------------
#get data
get_data <- function(var, x_min, x_max, y_min,y_max) {
  list.files(dir_in, var, full.names = TRUE, recursive = TRUE) %>%
    brick() %>%
    rasterToPoints() %>%
    as_tibble() %>%
    filter(x > x_min & x < x_max ) %>%
    filter(y > y_min & y < y_max ) %>% 
    rename_all( ~ (str_replace(., "X", ""))) %>%
    pivot_longer(cols = -c(x, y)) %>%
    mutate(
      date = lubridate::ymd(as.character(name)),
      year = lubridate::year(date),
      month = lubridate::month(date)
    ) %>% 
    dplyr::select(-name,-date) %>% 
    mutate(variable := !!var)
  
  
}
#======================================================================
#load nc data
# data_frame <-c("lai","ssrd","swvlall","temp","tp") %>% 
#   map_dfr(~get_data(var = .,x_min = 25,x_max =26,
#                     y_min = 67, y_max = 68)) %>% 
#   unite("var", variable:month, sep= "_", 
#         remove = TRUE) %>% 
#   pivot_wider(values_from = value,names_from = var)
 
 list.files(dir_in,".csv",full.names = TRUE, recursive = TRUE)[1] %>% 
  read.csv() %>% 
  colnames()

list.files(dir_in,".csv",full.names = FALSE, recursive = TRUE)

list.files(dir_in,".csv",full.names = TRUE, recursive = TRUE) %>% 
  map_dfr(~read.csv(.), .id = "filename") %>% 
  pivot_longer(temp_winter:swvlall_summer) %>% 
  ggplot(aes(x=X,y=value,group=name))+
  facet_grid(filename~name)+
  geom_line()+
  theme_bw()
#======================================================================
model_structure_local <-
  "lai_summer ~ ssrd_summer + temp_summer + lai_spring + swvlall_summer
                swvlall_summer~ lai_spring + tp_summer + swvlall_spring+ temp_summer
                lai_spring ~ ssrd_spring + tp_spring + temp_spring + swvlall_spring
                "
#======================================================================
#model fitting local
model_pipe_local <- 
  list.files(dir_in,".csv",full.names = TRUE, recursive = TRUE) %>% 
  map_dfr(~read.csv(.), .id = "filename") %>%
  group_by(filename) %>%
  nest() %>%
  mutate(
    #tibble as data frame
    data_psem_format = map(data, ~ as.data.frame(.)),
    #fit local sem and get goodness of fit
    sem_model = map(data, ~ sem(
      model_structure_local,
      data = .,
      estimator = "MLM",
      std.lv = TRUE,
      meanstructure = TRUE
    )),
    #predictions from sem model
    sem_pred = map2(sem_model,
                    data,
                    ~ predicty.lavaan(
                      .x,
                      newdata = .y,
                      xnames = c("ssrd_summer","temp_summer","lai_spring","swvlall_summer"),
                      ynames = "lai_summer"
                    )
                    %>%
                      tibble(.)),
    #loo predictions from sem model
    # sem_pred_loo = map(data,
    #                    ~ fun_loo_per_grid(
    #                      .x,
    #                      model_structure_local
    #                    )
    #                    %>%
    #                      tibble(.)),
    
    #calculate r-square local
    rsq = map(sem_model, ~ inspect(., "rsquare")),
    
    #calculate goodness of fit local
    chisq = map(sem_model, ~ fitMeasures(., c(
      "chisq", "df", "pvalue"
    ))),
    
    #plot dag local
    dag = map(sem_model, ~ ggsem(.)),
    
    #coef sem local
    model_parameters = map(
      sem_model,
      ~ parameterEstimates(.) %>% 
        tibble(.)
    ),
    #piecewise model fit
    psem = map(data_psem_format, ~ psem(
      lm(lai_summer  ~ ssrd_summer + temp_summer + lai_spring + tp_summer, data = .),
      lm(lai_spring ~ ssrd_spring + tp_spring + temp_spring, data = .),
      data = .
    )),
    #basis set
    basis_set = map(psem, ~ basisSet(.)),
    #dsep test
    d_sep = map(psem, ~ dSep(., .progressBar = FALSE)),
    #fisher c statistic
    fisher_c = map(psem, ~ fisherC(.)))
#======================================================================
#quick plot (observed vs predicted)
model_pipe_local %>%  
  dplyr::select(data,sem_pred) %>% 
  unnest(cols = c(data, sem_pred)) %>% 
  dplyr::select("lai_summer",".") %>% 
  rename(observed = "lai_summer",
         predicted = ".") %>% 
  group_by(filename) %>% 
  mutate(year = 1982:2018) %>% 
  ungroup() %>% 
  pivot_longer(observed:predicted) %>% 
  ggplot(aes(x=year,y=value,group = name, color = name))+
  geom_line()+
  facet_wrap(~filename)


