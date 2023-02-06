#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==========================================================
# Created by : Mohit Anand
# Created on : Sun Aug 07 2022 at 1:11:09 PM
# ==========================================================
# Created on Sun Aug 07 2022
# __copyright__ = Copyright (c) 2022, Mohit Anand's Project
# __credits__ = [Mohit Anand,]
# __license__ = Private
# __version__ = 0.0.0
# __maintainer__ = Mohit Anand
# __email__ = itsmohitanand@gmail.com
# __status__ = Development
# ==========================================================

import xarray as xr
from pcv.map import SEMMap

model_num = 5
sem_data = xr.open_dataset(f"/data/compoundx/anand/PCV/data/sem_data_{model_num}.nc")

sem_map = SEMMap(sem_data)
sem_map.lai_summer_map("scratch.png")

# name_1 = "lai_summer~swvlall_summer_Estimate"
# name_2 = "lai_summer~vpd_summer_Estimate"
# name_3 = "vpd_summer~swvlall_summer_Estimate"
# name_4 = "swvlall_summer~lai_spring_Estimate"
# name_5 = "swvlall_spring~lai_winter_Estimate"

# for name in [name_1, name_2, name_3, name_4, name_5 ]: #, name_2, name_3]:

#     img_name = "/data/compoundx/anand/PCV/images/" + name+f"_{model_num}.png"
#     sem_map.group_clim(name, img_path = img_name)

# piping_1 = "t2m_winter |> swvlall_winter |> lai_winter |> lai_spring |>  lai_summer"
# piping_2 = "t2m_winter |> swvlall_winter |> vpd_winter |> lai_winter |> lai_spring |>  lai_summer"

# piping_3 = "tp_winter |> swvlall_winter |> lai_winter |> lai_spring |>  lai_summer"
# piping_4 = "tp_winter |> swvlall_winter |> vpd_winter |> lai_winter |> lai_spring |>  lai_summer"

# piping_list = [piping_1, piping_2, piping_3, piping_4]

# for piping in piping_list:
#     sem_map.path_map(piping, "/data/compoundx/anand/PCV/images/"+ piping.replace(" ", "") + f"_{model_num}.png")
