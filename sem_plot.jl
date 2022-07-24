using NCDatasets
using GLMakie
using GeoMakie
using ColorSchemes
using Colors


i = 2
data_path = "/Users/anand/Documents/data/project_3_data/data/"
sem_data_path = data_path*"sem_data_$i.nc"
land_use_path = data_path*"regridded_LU_2018.nc"

sem_data = Dataset(sem_data_path)
land_data = Dataset(land_use_path)

lat = sem_data["latitude"][:]
lon = sem_data["longitude"][:]
p_val = sem_data["chi2p"][:,:]

sm_summer_to_lai_spring = sem_data["swvlall_summer_to_lai_spring_E"]
lai_summer_to_lai_spring = sem_data["lai_summer_to_lai_spring_E"]

### Process landuse data

land_use_classes = zeros(14, 220, 200)
class_list = keys(land_data)[begin+5:end-2]
for (i, class) in enumerate(class_list)
    land_use_classes[i,:,:] = land_data[class]
end


max_class = findmax(land_use_classes, dims=(1))[2]

land_class = getindex.(max_class, [1])[1,:,:]
land_class = reverse(land_class, dims=2)
land_class = [ x==12 ? missing : x for x in land_class]
labels = [class_list[i] for i in sort(unique(land_class))[begin:end-1]]

### Create plot
fontsize_theme = Theme(fontsize = 15)
set_theme!(fontsize_theme)

fig = Figure(resolution=(1500,1000))
ax_1 = GeoAxis(fig[1,1], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50",
        title="p value > 0.05 ~ acceptable model", 
        titlesize=25)
ax_2 = GeoAxis(fig[2,1], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50",
        title = "spring LAI influence on summer Soil Moisture", 
        titlesize=25)
ax_3 = GeoAxis(fig[1,3], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50", 
        title = "spring LAI influence on summer LAI", 
        titlesize=25)
ax_4 = GeoAxis(fig[2,3], lonlims = (minimum(lon),maximum(lon)), 
        latlims = (minimum(lat),maximum(lat)), 
        dest = "+proj=laea +lon_0=10 +lat_0=50", 
        title="Landuse Map", 
        titlesize=25)

s1 = surface!(ax_1, lon, lat, p_val, shading=false )
s2 = surface!(ax_2, lon, lat, sm_summer_to_lai_spring, shading=false, colormap=:redsblues)
s3 = surface!(ax_3, lon, lat, lai_summer_to_lai_spring, shading=false, colormap=:redsblues)
s4 = surface!(ax_4, lon, lat, land_class, colormap = cgrad(:Paired_9, 9, categorical = true), shading=false)

Colorbar(fig[1,2], s1)
Colorbar(fig[2,2], s2)
Colorbar(fig[1,4], s3)

cb = Colorbar(fig[2, 4], s4; height=Relative(1.0))

edges = range(1, 14, length = 10)
centers = (edges[1:9] .+ edges[2:10]) .* 0.5
cb.ticks = (centers, labels)
fig

save("images/sem_plot_$i.png", fig)
