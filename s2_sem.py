import xarray as xr
import semopy as sm
from pcv.process import select_data
import matplotlib.pylab as plt
import pandas as pd
import numpy as np

t2m_path = "/Users/anand/Documents/data/project_3_data/data/detrended_t2m.nc"
tp_path = "/Users/anand/Documents/data/project_3_data/data/detrended_tp.nc"
rad_path = "/Users/anand/Documents/data/project_3_data/data/detrended_ssrd.nc"
lai_path = "/Users/anand/Documents/data/project_3_data/data/detrended_lai.nc"
swvlall_path = "/Users/anand/Documents/data/project_3_data/data/detrended_swvlall.nc"
vpd_path = "/Users/anand/Documents/data/project_3_data/data/detrended_vpd.nc"
sd_path = "/Users/anand/Documents/data/project_3_data/data/detrended_sd.nc"

t2m_data = xr.open_dataset(t2m_path)
tp_data = xr.open_dataset(tp_path)
ssrd_data = xr.open_dataset(rad_path)
swvlall_data = xr.open_dataset(swvlall_path)
vpd_data = xr.open_dataset(vpd_path)
lai_data = xr.open_dataset(lai_path)
sd_data = xr.open_dataset(sd_path)

t2m_winter = select_data(t2m_data,  "winter")
t2m_spring = select_data(t2m_data,  "spring")
t2m_summer = select_data(t2m_data,  "summer")

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

sd_winter = select_data(sd_data,  "winter")
sd_spring = select_data(sd_data,  "spring")
sd_summer = select_data(sd_data,  "summer")

mod_0 = """
# measurement model

lai_spring ~ tp_spring + ssrd_spring + t2m_spring
swvlall_summer ~ lai_spring + ssrd_summer + t2m_summer+ tp_summer
lai_summer ~ swvlall_summer
lai_summer ~ lai_spring

"""

mod_1 = """
# measurement model

lai_spring ~ tp_spring + ssrd_spring + t2m_spring
swvlall_summer ~ lai_spring + ssrd_summer + t2m_summer+ tp_summer
lai_summer ~ swvlall_summer + ssrd_summer + t2m_summer+ tp_summer
lai_summer ~ lai_spring

"""

mod_2 = """
# measurement model

lai_spring ~ tp_spring + ssrd_spring + t2m_spring + swvlall_spring
swvlall_summer ~ lai_spring + ssrd_summer + t2m_summer+ tp_summer
swvlall_spring ~ lai_winter + ssrd_spring + t2m_spring+ tp_spring
lai_summer ~ swvlall_summer + ssrd_summer + t2m_summer+ tp_summer
lai_summer ~ lai_spring
lai_spring ~ lai_winter

"""
mod_3 = """
# measurement model

lai_spring ~  ssrd_spring + t2m_spring + swvlall_spring
swvlall_summer ~ lai_spring + ssrd_summer + t2m_summer+ tp_summer +swvlall_spring
swvlall_spring ~  ssrd_spring + t2m_spring+ tp_spring + swvlall_winter
lai_summer ~ swvlall_summer + ssrd_summer + t2m_summer
lai_summer ~ lai_spring
swvlall_winter ~ ssrd_winter + t2m_winter+ tp_winter

"""

mod_4 = """
# measurement model

lai_summer ~ swvlall_summer 
lai_summer ~ lai_spring
swvlall_winter ~  tp_winter
swvlall_spring ~ swvlall_winter
lai_spring ~ swvlall_spring + sd_winter
lai_spring ~ t2m_winter + swvlall_winter + sd_winter
swvlall_summer ~ swvlall_spring + lai_spring
"""

mod_5 = """
# measurement model

lai_summer ~ lai_spring + t2m_winter +tp_winter
lai_spring ~ t2m_winter +tp_winter
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

model_data_3 = xr.Dataset(
    {
        "chi2p": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),         
        "lai_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_summer_to_swvlall_summer_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "swvlall_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_spring_to_swvlall_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "swvlall_spring_to_swvlall_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
    },
    coords= {"latitude":lai_data.latitude, "longitude":lai_data.longitude}
)

model_data_4 = xr.Dataset(
    {
        "chi2p": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),         
        "swvlall_winter_to_tp_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "swvlall_spring_to_swvlall_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_spring_to_swvlall_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_spring_to_t2m_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_spring_to_swvlall_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "swvlall_summer_to_swvlall_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "swvlall_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_summer_to_swvlall_summer_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
    },
    coords= {"latitude":lai_data.latitude, "longitude":lai_data.longitude}
)

model_data_5 = xr.Dataset(
    {
        "chi2p": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),         
        "lai_spring_to_temp_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_spring_to_tp_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_summer_to_lai_spring_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_summer_to_temp_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
        "lai_summer_to_tp_winter_E": (
            ("latitude", "longitude"), np.full((200, 220), np.nan)),
    },
    coords= {"latitude":lai_data.latitude, "longitude":lai_data.longitude}
)

mod_list = [mod_0, mod_1, mod_2, mod_3, mod_4, mod_5]

for lat in range(200):
    print(lat)
    for lon in range(220):
        lai_w = lai_winter.GLOBMAP_LAI[:, lat, lon].to_numpy()[-39:]
        if np.isnan(lai_w).any() == True:
            pass
        else:

            lai_w = lai_summer.GLOBMAP_LAI[:, lat, lon].to_numpy()[-39:]
            lai_sp = lai_spring.GLOBMAP_LAI[:, lat, lon].to_numpy()[-39:]
            lai_su = lai_summer.GLOBMAP_LAI[:, lat, lon].to_numpy()[-39:]
            
            t2m_w = t2m_winter.t2m[:, lat, lon].to_numpy()[-39:]
            t2m_sp = t2m_spring.t2m[:, lat, lon].to_numpy()[-39:]
            t2m_su = t2m_summer.t2m[:, lat, lon].to_numpy()[-39:]

            tp_w = tp_winter.tp[:, lat, lon].to_numpy()[-39:]
            tp_sp = tp_spring.tp[:, lat, lon].to_numpy()[-39:]
            tp_su = tp_summer.tp[:, lat, lon].to_numpy()[-39:]
            
            ssrd_w = ssrd_winter.ssrd[:, lat, lon].to_numpy()[-39:]
            ssrd_sp = ssrd_spring.ssrd[:, lat, lon].to_numpy()[-39:]
            ssrd_su = ssrd_summer.ssrd[:, lat, lon].to_numpy()[-39:]

            vpd_w = vpd_winter.vpd[:, lat, lon].to_numpy()[-39:]
            vpd_sp = vpd_spring.vpd[:, lat, lon].to_numpy()[-39:]
            vpd_su = vpd_summer.vpd[:, lat, lon].to_numpy()[-39:]

            swvlall_w = swvlall_winter.swvlall[:, lat, lon].to_numpy()[-39:]
            swvlall_sp = swvlall_spring.swvlall[:, lat, lon].to_numpy()[-39:]
            swvlall_su = swvlall_summer.swvlall[:, lat, lon].to_numpy()[-39:]

            # sd_w = sd_winter.sd[:, lat, lon].to_numpy()[-39:]
            # sd_sp = sd_spring.sd[:, lat, lon].to_numpy()[-39:]
            # sd_su = sd_summer.sd[:, lat, lon].to_numpy()[-39:]
            
            assert t2m_w.shape == t2m_sp.shape == t2m_su.shape
            
            list_val = [t2m_w[:-1], t2m_sp[1:], t2m_su[1:],
                    tp_w[:-1], tp_sp[1:], tp_su[1:], 
                    ssrd_w[:-1], ssrd_sp[1:], ssrd_su[1:], 
                    lai_w[:-1], lai_sp[1:], lai_su[1:],
                    vpd_w[:-1], vpd_sp[1:], vpd_su[1:],
                    swvlall_w[:-1], swvlall_sp[1:], swvlall_su[1:],
                    # sd_w[:-1], sd_sp[1:], sd_su[1:],
                    ]

            col_names = ["t2m_winter", "t2m_spring", "t2m_summer",
                            "tp_winter", "tp_spring", "tp_summer",
                            "ssrd_winter", "ssrd_spring", "ssrd_summer",
                            "lai_winter", "lai_spring", "lai_summer", 
                            "vpd_winter", "vpd_spring", "vpd_summer",
                            "swvlall_winter", "swvlall_spring", "swvlall_summer",
                            # "sd_winter", "sd_spring", "sd_summer",
                            ]    
            
            data = np.vstack(list_val).T

            df = pd.DataFrame(data, columns=col_names)
            df=(df-df.mean())/df.std()
            
            for i, mod in enumerate(mod_list[-1:]):
                i=5
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
                elif i==3:
                    model_data_3.chi2p[lat, lon] = chi2p
                    model_data_3.lai_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[18, :].Estimate
                    model_data_3.lai_summer_to_swvlall_summer_E[lat, lon] = model.inspect().iloc[15, :].Estimate
                    model_data_3.swvlall_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[3, :].Estimate
                    model_data_3.lai_spring_to_swvlall_spring_E[lat, lon] = model.inspect().iloc[2, :].Estimate
                    model_data_3.swvlall_spring_to_swvlall_winter_E[lat, lon] = model.inspect().iloc[11, :].Estimate
                elif i==4:
                    model_data_4.chi2p[lat, lon] = chi2p
                    model_data_4.swvlall_winter_to_tp_winter_E[lat, lon] = model.inspect().iloc[0, :].Estimate
                    model_data_4.swvlall_spring_to_swvlall_winter_E[lat, lon] = model.inspect().iloc[1, :].Estimate
                    model_data_4.lai_spring_to_swvlall_spring_E[lat, lon] = model.inspect().iloc[2, :].Estimate
                    model_data_4.lai_spring_to_t2m_winter_E[lat, lon] = model.inspect().iloc[3, :].Estimate
                    model_data_4.lai_spring_to_swvlall_winter_E[lat, lon] = model.inspect().iloc[4, :].Estimate
                    model_data_4.swvlall_summer_to_swvlall_spring_E[lat, lon] = model.inspect().iloc[5, :].Estimate
                    model_data_4.swvlall_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[6, :].Estimate
                    model_data_4.lai_summer_to_swvlall_summer_E[lat, lon] = model.inspect().iloc[7, :].Estimate
                    model_data_4.lai_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[8, :].Estimate
                elif i==5:
                    model_data_5.chi2p[lat, lon] = chi2p
                    model_data_5.lai_spring_to_temp_winter_E[lat, lon] = model.inspect().iloc[0, :].Estimate
                    model_data_5.lai_spring_to_tp_winter_E[lat, lon] = model.inspect().iloc[1, :].Estimate
                    model_data_5.lai_summer_to_lai_spring_E[lat, lon] = model.inspect().iloc[2, :].Estimate
                    model_data_5.lai_summer_to_temp_winter_E[lat, lon] = model.inspect().iloc[3, :].Estimate
                    model_data_5.lai_summer_to_tp_winter_E[lat, lon] = model.inspect().iloc[4, :].Estimate

# model_data_0.to_netcdf("/Users/anand/Documents/data/project_3_data/data/sem_data_0.nc")
# model_data_1.to_netcdf("/Users/anand/Documents/data/project_3_data/data/sem_data_1.nc")
# model_data_2.to_netcdf("/Users/anand/Documents/data/project_3_data/data/sem_data_2.nc")
model_data_5.to_netcdf("/Users/anand/Documents/data/project_3_data/data/sem_data_5.nc")
