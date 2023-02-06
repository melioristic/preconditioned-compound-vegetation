#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# Created by : Mohit Anand
# Created on : Wed Sep 28 2022 at 9:44:27 AM
# ==========================================================
# Created on Wed Sep 28 2022
# __copyright__ = Copyright (c) 2022, PCV Project
# __credits__ = [Mohit Anand,]
# __license__ = Private
# __version__ = 0.0.0
# __maintainer__ = Mohit Anand
# __email__ = itsmohitanand@gmail.com
# __status__ = Development
# ==========================================================


import xarray as xr
from pcv.map import SEMMap

model_num = 2
sem_data = xr.open_dataset(f"/data/compoundx/anand/PCV/data/sem_data_{model_num}.nc")

sem_map = SEMMap(sem_data)

sem_map.lai_summer_map(f"/data/compoundx/anand/PCV/images/lai_summer_{model_num}.png")

name_1 = "lai_summer~swvlall_summer_Estimate"
name_2 = "swvlall_summer~lai_spring_Estimate"

for name in [name_1, name_2 ] : 
    img_name = "/data/compoundx/anand/PCV/images/" + name+f"_{model_num}.png"
    sem_map.group_clim(name, img_path = img_name)

# piping_1 = "t2m_winter |> lai_spring |> lai_summer"

# piping_2 = "t2m_winter |> swvlall_winter |> swvlall_spring |> lai_spring |>  lai_summer"
# piping_3 = "t2m_winter |> swvlall_winter |> swvlall_spring |> lai_spring |> swvlall_summer |> lai_summer"
# piping_4 = "t2m_winter |> swvlall_winter |> swvlall_spring |> swvlall_summer |>  lai_summer"

piping_5 = "tp_winter |> swvlall_winter |> swvlall_spring |> lai_spring |>  lai_summer"
piping_6 = "tp_winter |> swvlall_winter |> swvlall_spring |> lai_spring |> swvlall_summer |> lai_summer"
piping_7 = "tp_winter |> swvlall_winter |> swvlall_spring |> swvlall_summer |>  lai_summer"

sem_map.path_map(piping=5, scratch_1.png)

# piping_list_1 = [piping_1, piping_2, piping_3, piping_4]
# piping_list_1 = [piping_2, piping_3, piping_4]

# piping_list_2 = [piping_5, piping_6, piping_7]

# # for piping in piping_list_1:
# #     sem_map.path_map(piping, "/data/compoundx/anand/PCV/images/"+ piping.replace(" ", "") + f"_{model_num}.png")

# for piping in piping_list_2:
#     sem_map.path_map(piping, "/data/compoundx/anand/PCV/images/"+ piping.replace(" ", "") + f"_{model_num}.png")

# # sem_map.path_map(piping_list_1, f"/data/compoundx/anand/PCV/images/t2m_winter_{model_num}.png")
# sem_map.path_map(piping_list_2, f"/data/compoundx/anand/PCV/images/tp_winter_{model_num}.png")
