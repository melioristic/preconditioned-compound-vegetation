import xarray as xr
from pcv.process import standardise_monthly, detrend, aggregate_seasons, select_data
import matplotlib.pylab as plt

temperature_path = "/Users/anand/Documents/data/project_3_data/t2m.monthly.era5.europe.1981-2020.nc"
tp_path = "/Users/anand/Documents/data/project_3_data/tp.monthly.era5.europe.1981-2020.nc"

temp_data = xr.open_dataset(temperature_path)
tp_data = xr.open_dataset(tp_path)

detrended_temp = detrend(temp_data, deg=1, var="t2m")
detrended_tp = detrend(tp_data, deg=1, var="tp")

standardised_temp = standardise_monthly(detrended_temp, "t2m")
standardised_tp = standardise_monthly(detrended_tp, "tp")

aggregated_temp = aggregate_seasons(standardised_temp)
aggregated_tp = aggregate_seasons(standardised_tp)

temp_winter = select_data(aggregated_temp, "t2m", "winter")
tp_summer = select_data(aggregated_tp, "tp", "summer")
tp_winter = select_data(aggregated_tp, "tp", "winter")

