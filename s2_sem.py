import xarray as xr
import semopy as sm
from pcv.process import select_data
import matplotlib.pylab as plt
import pandas as pd
import numpy as np

temp_path = "/Users/anand/Documents/data/project_3_data/data/detrended_temp.nc"
tp_path = "/Users/anand/Documents/data/project_3_data/data/detrended_tp.nc"
rad_path = "/Users/anand/Documents/data/project_3_data/data/detrended_ssrd.nc"
lai_path = "/Users/anand/Documents/data/project_3_data/data/detrended_lai.nc"
swvlall_path = "/Users/anand/Documents/data/project_3_data/data/detrended_swvlall.nc"
vpd_path = "/Users/anand/Documents/data/project_3_data/data/detrended_vpd.nc"


temp_data = xr.open_dataset(temp_path)
tp_data = xr.open_dataset(tp_path)
ssrd_data = xr.open_dataset(rad_path)
swvlall_data = xr.open_dataset(swvlall_path)
vpd_data = xr.open_dataset(vpd_path)
lai_data = xr.open_dataset(lai_path)

temp_winter = select_data(temp_data,  "winter")
temp_spring = select_data(temp_data,  "spring")
temp_summer = select_data(temp_data,  "summer")

tp_winter = select_data(tp_data,  "winter")
tp_spring = select_data(tp_data,  "spring")
tp_summer = select_data(tp_data,  "summer")

ssrd_winter = select_data(ssrd_data,  "winter")
ssrd_spring = select_data(ssrd_data,  "spring")
ssrd_summer = select_data(ssrd_data,  "summer")

lai_winter = select_data(lai_data,  "winter")
lai_spring = select_data(lai_data,  "spring")
lai_summer = select_data(lai_data,  "summer")

swvlall_winter = select_data(swvlall_data,  "winter")
swvlall_spring = select_data(swvlall_data,  "spring")
swvlall_summer = select_data(swvlall_data,  "summer")

vpd_winter = select_data(vpd_data,  "winter")
vpd_spring = select_data(vpd_data,  "spring")
vpd_summer = select_data(vpd_data,  "summer")

mod_0 = """
# measurement model

lai_spring ~ tp_spring + ssrd_spring + temp_spring
swvlall_summer ~ lai_spring + ssrd_summer + temp_summer+ tp_summer
lai_summer ~ swvlall_summer
lai_summer ~ lai_spring

"""

mod_1 = """
# measurement model

lai_spring ~ tp_spring + ssrd_spring + temp_spring
swvlall_summer ~ lai_spring + ssrd_summer + temp_summer+ tp_summer
lai_summer ~ swvlall_summer + ssrd_summer + temp_summer+ tp_summer
lai_summer ~ lai_spring

"""

mod_2 = """
# measurement model

lai_spring ~ tp_spring + ssrd_spring + temp_spring + swvlall_spring
swvlall_summer ~ lai_spring + ssrd_summer + temp_summer+ tp_summer
swvlall_spring ~ lai_winter + ssrd_spring + temp_spring+ tp_spring
lai_summer ~ swvlall_summer + ssrd_summer + temp_summer+ tp_summer
lai_summer ~ lai_spring
lai_spring ~ lai_winter

"""

model_data_0 = xr.Dataset(
    {
        "chi2p": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),         
        "lai_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_summer_to_swvlall_summer_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "swvlall_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan))        
    },
    coords= {"latitude":lai_data.latitude, "longitude":lai_data.longitude}
)

model_data_1 = xr.Dataset(
    {
        "chi2p": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),         
        "lai_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_summer_to_swvlall_summer_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "swvlall_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan))        
    },
    coords= {"latitude":lai_data.latitude, "longitude":lai_data.longitude}
)

model_data_2 = xr.Dataset(
    {
        "chi2p": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),         
        "lai_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_summer_to_swvlall_summer_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "swvlall_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_spring_to_lai_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "swvlall_spring_to_lai_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_spring_to_swvlall_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
    },
    coords= {"latitude":lai_data.latitude, "longitude":lai_data.longitude}
)

mod_list = [mod_0, mod_1, mod_2]

for lat in range(200):
    print(lat)
    for lon in range(220):
        lai_w = lai_winter.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
        if np.isnan(lai_w).any() == True:
            pass
        else:

            lai_sp = lai_spring.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            lai_su = lai_summer.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            
            temp_w = temp_winter.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            temp_sp = temp_spring.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            temp_su = temp_summer.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]

            tp_w = tp_winter.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            tp_sp = tp_spring.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            tp_su = tp_summer.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            
            ssrd_w = ssrd_winter.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            ssrd_sp = ssrd_spring.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            ssrd_su = ssrd_summer.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]

            vpd_w = vpd_winter.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            vpd_sp = vpd_spring.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            vpd_su = vpd_summer.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]

            swvlall_w = swvlall_winter.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            swvlall_sp = swvlall_spring.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            swvlall_su = swvlall_summer.__xarray_dataarray_variable__[:, lat, lon].to_numpy()[-39:]
            assert temp_w.shape == temp_sp.shape == temp_su.shape
            
            list_val = [temp_w[:-1], temp_sp[1:], temp_su[1:],
                    tp_w[:-1], tp_sp[1:], tp_su[1:], 
                    ssrd_w[:-1], ssrd_sp[1:], ssrd_su[1:], 
                    lai_w[:-1], lai_sp[1:], lai_su[1:],
                    vpd_w[:-1], vpd_sp[1:], vpd_su[1:],
                    swvlall_w[:-1], swvlall_sp[1:], swvlall_su[1:]
                    ]

            col_names = ["temp_winter", "temp_spring", "temp_summer",
                            "tp_winter", "tp_spring", "tp_summer",
                            "ssrd_winter", "ssrd_spring", "ssrd_summer",
                            "lai_winter", "lai_spring", "lai_summer", 
                            "vpd_winter", "vpd_spring", "vpd_summer",
                            "swvlall_winter", "swvlall_spring", "swvlall_summer",
                            ]    
            
            data = np.vstack(list_val).T

            df = pd.DataFrame(data, columns=col_names)
            df=(df-df.mean())/df.std()
            
            for i, mod in enumerate(mod_list):
                model = sm.Model(mod)
                model.fit(df)
                chi2p = sm.calc_stats(model)["chi2 p-value"][0]
                if i ==0:
                    model_data_0.chi2p[lat, lon] = chi2p
                    model_data_0.lai_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[8, :].Estimate
                    model_data_0.lai_summer_to_swvlall_summer_E[lat, lon] = model.inspect().iloc[7, :].Estimate
                    model_data_0.swvlall_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[3, :].Estimate
                elif i==1:
                    model_data_1.chi2p[lat, lon] = chi2p
                    model_data_1.lai_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[11, :].Estimate
                    model_data_1.lai_summer_to_swvlall_summer_E[lat, lon] = model.inspect().iloc[7, :].Estimate
                    model_data_1.swvlall_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[3, :].Estimate
                elif i==2:
                    model_data_2.chi2p[lat, lon] = chi2p
                    model_data_2.lai_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[17, :].Estimate
                    model_data_2.swvlall_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[5, :].Estimate
                    model_data_2.lai_spring_to_lai_winter_E[lat, lon] = model.inspect().iloc[4, :].Estimate
                    model_data_2.swvlall_spring_to_lai_winter_E[lat, lon] = model.inspect().iloc[9, :].Estimate
                    model_data_2.lai_spring_to_swvlall_spring_E[lat, lon] = model.inspect().iloc[3, :].Estimate


model_data_0.to_netcdf("/Users/anand/Documents/data/project_3_data/data/sem_data_0.nc")
model_data_1.to_netcdf("/Users/anand/Documents/data/project_3_data/data/sem_data_1.nc")
model_data_2.to_netcdf("/Users/anand/Documents/data/project_3_data/data/sem_data_2.nc")
