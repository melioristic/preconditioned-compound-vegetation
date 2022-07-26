from pcv.io import regrid_data

landuse_path = "/Users/anand/Documents/lai/project_3_data/ESACCI-LC-L4-L_fromLUT_0d050_2018.nc"
temperature_path = "/Users/anand/Documents/lai/project_3_data/t2m.monthly.era5.europe.1981-2020.nc"

regridded_landuse = regrid_data(landuse_path, temperature_path)

regridded_landuse.to_netcdf("/Users/anand/Documents/lai/project_3_data/regridded_LU_2018.nc")