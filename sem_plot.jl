using NCDatasets
using GLMakie
using GeoMakie
using ColorSchemes
using Colors

i = 5

data_path = "/Users/anand/Documents/data/project_3_data/data/"
sem_data_path = data_path*"sem_data_$i.nc"

sem_data = Dataset(sem_data_path)
keys(sem_data)

lat = sem_data["latitude"][:]
lon = sem_data["longitude"][:]
p_val = sem_data["chi2p"][:,:]

lai_spring_to_temp_winter_E = sem_data["lai_spring_to_temp_winter_E"]
lai_spring_to_tp_winter_E= sem_data["lai_spring_to_tp_winter_E"]
lai_summer_to_lai_spring_E = sem_data["lai_summer_to_lai_spring_E"]
lai_summer_to_temp_winter_E = sem_data["lai_summer_to_temp_winter_E"]
lai_summer_to_tp_winter_E = sem_data["lai_summer_to_tp_winter_E"]

### Create plot
fontsize_theme = Theme(fontsize = 15)
set_theme!(fontsize_theme)

fig = Figure(resolution=(1200,1600))
ax_1 = GeoAxis(fig[1,1], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50",
        title="p value > 0.05 ~ acceptable model", 
        titlesize=25)
ax_2 = GeoAxis(fig[1,3], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50",
        title = "lai_spring_to_temp_winter_E", 
        titlesize=25)
ax_3 = GeoAxis(fig[2,1], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50", 
        title = "lai_spring_to_tp_winter_E", 
        titlesize=25)
ax_4 = GeoAxis(fig[2,3], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50", 
        title="lai_summer_to_lai_spring_E", 
        titlesize=25)
ax_5 = GeoAxis(fig[3,1], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50", 
        title="lai_summer_to_temp_winter_E", 
        titlesize=25)
ax_6 = GeoAxis(fig[3,3], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50", 
        title="lai_summer_to_tp_winter_E", 
        titlesize=25)

s1 = surface!(ax_1, lon, lat, p_val, shading=false )
s2 = surface!(ax_2, lon, lat,lai_spring_to_temp_winter_E, shading=false, colormap=:redsblues)
s3 = surface!(ax_3, lon, lat, lai_spring_to_tp_winter_E, shading=false, colormap=:redsblues)
s4 = surface!(ax_4, lon, lat, lai_summer_to_lai_spring_E, colormap =:redsblues , shading=false)
s5 = surface!(ax_5, lon, lat, lai_summer_to_temp_winter_E, shading=false, colormap=:redsblues)
s6 = surface!(ax_6, lon, lat, lai_summer_to_tp_winter_E, colormap =:redsblues, shading=false)

# s6 = surface!(ax_6, lon, lat, lai_summer_to_tp_winter_E, colormap = cgrad(:Paired_9, 3, categorical = true), shading=false)

Colorbar(fig[1,2], s1)
Colorbar(fig[1,4], s2)
Colorbar(fig[2,2], s3)
Colorbar(fig[2,4], s4)
Colorbar(fig[3,2], s5)
Colorbar(fig[3,4], s6)


fig

save("images/sem_plot_$i.png", fig)


### P_val count
p_val[ismissing.(p_val)].=9999

count(p_val.<0.05)
count(p_val.<1)