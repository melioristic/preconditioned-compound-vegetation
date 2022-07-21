
def comp_area_lat_lon(lat,lon):
    import numpy as np

    radius = 6.37122e6 # in meters

    lat=np.squeeze(lat); lon=np.squeeze(lon)
    nlat=len(lat)
    nlon=len(lon)

    # LATITUDE
    lat_edge=np.zeros((nlat+1))
    lat_edge[0] = max(-90, lat[0]-0.5*(lat[1]-lat[0])); #ana
    lat_edge[1:nlat] = 0.5*(lat[0:nlat-1] + lat[1:nlat])
    lat_edge[nlat] = min(90, lat[nlat-1]-0.5*(lat[nlat-2]-lat[nlat-1]))
    dlat=np.diff(lat_edge)

    #LONGITUDE
    lon_edge=np.zeros((nlon+1))
    lon_edge[0] = lon[0]-0.5*(lon[1]-lon[0])
    lon_edge[1:nlon] = 0.5*(lon[0:nlon-1] + lon[1:nlon])
    lon_edge[nlon] = lon[nlon-1]-0.5*(lon[nlon-2]-lon[nlon-1])
    dlon=np.diff(lon_edge)

    dlon_2d, dlat_2d = np.meshgrid(dlon,dlat) # create mesh with cell size in deg
    lon_2d, lat_2d = np.meshgrid(lon, lat)

    dy = radius * (dlat_2d * (np.pi/180.0))
    dx = radius * np.multiply(dlon_2d * (np.pi/180.0),np.cos(lat_2d * (np.pi/180.0)))

    area = np.multiply(dx , dy)
    if np.sum(area)<0:
        area=-1*area

    return area