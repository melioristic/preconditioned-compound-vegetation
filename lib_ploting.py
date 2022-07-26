from typing import Union, List

import matplotlib
import xarray
import cartopy.crs as ccrs
import cartopy.feature as cf
from matplotlib import pyplot as plt

def plotMap_withBorders(map_to_plot: xarray.DataArray,
                        ax: object = None,
                        title: str = '',
                        add_colorbar: bool = True,
                        cmap="jet", cbar_shrink: float = 0.65, label_cb: str = "",
                        vmin: float = None, vmax: float = None,
                        region_extend: Union[str, List[float]] = "the whole domain",
                        plot_gridlines_labels: bool = False,
                        *args, **kwargs):
    """ plot a my_map of Spain with countries border on top. The lai comes from a xarray my_map in lat lon.
    :param map_to_plot: a xarray of dim latitude, longitude.
    :param ax: the ax on which to plot, if subplot
    :param title: the title of the plot
    :param vmax: max value for the colormap and colorbar. If None, then the max value of the lai is taken.
    :param vmin: same, with min.
    :param cmap: color this_map
    :param add_colorbar: whether or not to plot the colorbar.
    :param label_cb: the label for the colorbar. Vertical by default.
    :param cbar_shrink: factor to shrink the size of the colorbar.
    :param region_extend: either 'Spain' or "the whole domain". It is used to set the lat lon limites for the plot.
    We can also give a list of 4 floats, corresponding to the region extend : [lat_min, lat_max, lon_min, lon_max] in degrees
    :param plot_gridlines_labels: wether or not to plot the gridlines and the associated labels.
    """


    proj = ccrs.PlateCarree()
    # or Mercator()

    if ax is None:
        ax = plt.axes(projection=proj)

    # select the lat lon extend
    if region_extend == "the whole domain":
        lat_min, lat_max = 25, 70
        lon_min, lon_max = -10, 45
    elif type(region_extend) == list:
        lat_min, lat_max = region_extend[0], region_extend[1]
        lon_min, lon_max = region_extend[2], region_extend[3]
    else:
        raise ValueError("Wrong region")
    ax.set_extent((lon_min, lon_max, lat_min, lat_max))

    # TODO : see how to plot a this_map with vmin=-20, vmax=+5, tout en gardant le 0 en blanc.

    if add_colorbar:
        map_to_plot.plot(cmap=cmap, vmin=vmin, vmax=vmax,
                         cbar_kwargs={"shrink": cbar_shrink, 'label': label_cb},
                         *args, **kwargs)
    else:
        map_to_plot.plot(cmap=cmap, vmin=vmin, vmax=vmax,
                         add_colorbar=add_colorbar,
                         *args, **kwargs)
    plt.title(title)

    # plot the borders on top
    ax.coastlines()
    ax.add_feature(cf.BORDERS)

    # à explorer : gridlines
    if plot_gridlines_labels:
        gl = ax.gridlines(draw_labels=True, color='gray', alpha=0.5,
                          dms=True, x_inline=False, y_inline=False)
        gl.top_labels = False
        gl.right_labels = False

    return ax



def labels(xtitle: str = "", ytitle: str = "", title: str = "") -> None:
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(title)


def cmap_single_color(color: str = 'b'):
    """
    :param color: a string of a receivable python color, such as 'k', 'r', 'm', etc.
    :return: the colormap object corresponding to a single color.
    """
    return matplotlib.colors.ListedColormap([color])


def savefigure(saveas: str) -> None:
    """ the figure is saved with a tight white bow around it.
    saveas : the save address must have the relative or absolute path location
    it can already contain the extension, like '.png' or '.pdf' """
    plt.savefig(saveas, dpi=300, bbox_inches='tight', pad_inches=0.03, transparent=False)
    print('The figure has been saved')

