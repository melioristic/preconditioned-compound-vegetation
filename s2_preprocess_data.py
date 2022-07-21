import xarray as xr

from pcv.process import standardise_monthly, detrend, aggregate_seasons
import matplotlib.pylab as plt

temperature_path = "/Users/anand/Documents/data/project_3_data/t2m.monthly.era5.europe.1981-2020.nc"

temp_data = xr.open_dataset(temperature_path)

temp_data.t2m[:,100,100].plot()
plt.savefig('scratch_0.png')
plt.close()

detrended_temp = detrend(temp_data, deg=1, var="t2m")
detrended_temp.t2m[:,100,100].plot()
plt.savefig('scratch_1.png')
plt.close()

standardised_temp = standardise_monthly(detrended_temp, "t2m")

standardised_temp.t2m[:,100,100].plot()
plt.savefig('scratch_2.png')
plt.close()

aggregated_temp = aggregate_seasons(standardised_temp)

aggregated_temp.t2m[:,100, 100].plot()
plt.savefig('scratch_3.png')
plt.close()