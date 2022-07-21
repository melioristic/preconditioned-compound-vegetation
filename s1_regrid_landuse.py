from pcv.io import regrid_data

landuse_path = "/Users/anand/Documents/data/project_3_data/ESACCI-LC-L4-L_fromLUT_0d050_2018.nc"
temperature_path = "/Users/anand/Documents/data/project_3_data/t2m.monthly.era5.europe.1981-2020.nc"

regrid_data(landuse_path, temperature_path)