import xarray as xr
import semopy as sm
from pcv.process import select_data
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from pcv.process import create_xr_dataset, fill_xr_dataset
from pcv.models import mod_1, mod_2

t2m_path = "/Users/anand/Documents/data/project_3_data/data/detrended_t2m.nc"
tp_path = "/Users/anand/Documents/data/project_3_data/data/detrended_tp.nc"
ssrd_path = "/Users/anand/Documents/data/project_3_data/data/detrended_ssrd.nc"
lai_path = "/Users/anand/Documents/data/project_3_data/data/detrended_lai.nc"
swvlall_path = "/Users/anand/Documents/data/project_3_data/data/detrended_swvlall.nc"
vpd_path = "/Users/anand/Documents/data/project_3_data/data/detrended_vpd.nc"

t2m_data = xr.open_dataset(t2m_path)
tp_data = xr.open_dataset(tp_path)
ssrd_data = xr.open_dataset(ssrd_path)
swvlall_data = xr.open_dataset(swvlall_path)
vpd_data = xr.open_dataset(vpd_path)
lai_data = xr.open_dataset(lai_path)

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

##### Section for everything about the model
model_num = 2

if model_num==1:
    mod = mod_1
elif model_num==2:
    mod = mod_2

model = sm.Model(mod)

graph_img_path = f"images/sem_{model_num}.png"
sm.semplot(model, graph_img_path)
print("The model graph is saved at {graph_img_path}")

xr_dataset = create_xr_dataset(model, lai_data.latitude, lai_data.longitude)

for lat in range(200):
    print(lat)
    for lon in range(220):
        lai_w = lai_winter.GLOBMAP_LAI[:, lat, lon].to_numpy()[-39:]
        if np.isnan(lai_w).any() == True:
            pass
        else:
            lai_w = lai_winter.GLOBMAP_LAI[:, lat, lon].to_numpy()[-39:]
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
            
            assert t2m_w.shape == t2m_sp.shape == t2m_su.shape
            
            list_val = [t2m_w[:-1], t2m_sp[1:], t2m_su[1:],
                    tp_w[:-1], tp_sp[1:], tp_su[1:], 
                    ssrd_w[:-1], ssrd_sp[1:], ssrd_su[1:], 
                    lai_w[:-1], lai_sp[1:], lai_su[1:],
                    vpd_w[:-1], vpd_sp[1:], vpd_su[1:],
                    swvlall_w[:-1], swvlall_sp[1:], swvlall_su[1:],
                    ]

            col_names = ["t2m_winter", "t2m_spring", "t2m_summer",
                            "tp_winter", "tp_spring", "tp_summer",
                            "ssrd_winter", "ssrd_spring", "ssrd_summer",
                            "lai_winter", "lai_spring", "lai_summer", 
                            "vpd_winter", "vpd_spring", "vpd_summer",
                            "swvlall_winter", "swvlall_spring", "swvlall_summer",
                            ]    
            
            data = np.vstack(list_val).T

            df = pd.DataFrame(data, columns=col_names)
            df=(df-df.mean())/df.std()
            
            model.fit(df)

            chi2p = sm.calc_stats(model)["chi2 p-value"][0]
            xr_dataset = fill_xr_dataset(xr_dataset, model.inspect(), chi2p
            , lat, lon)

xr_dataset.to_netcdf(f"/Users/anand/Documents/data/project_3_data/data/sem_data_{model_num}.nc")