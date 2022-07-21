import xarray as xr
from pcv.process import standardise_monthly
import matplotlib.pylab as plt




temperature_path = "/Users/anand/Documents/data/project_3_data/t2m.monthly.era5.europe.1981-2020.nc"


temp_data = xr.open_dataset(temperature_path)

temp_data.t2m[:,100,100].plot()
plt.savefig('scratch_1.png')
plt.close()

standardised_temp = standardise_monthly(temp_data, "t2m")

print(standardised_temp.keys())
standardised_temp.t2m[:,100,100].plot()
plt.savefig('scratch_2.png')


