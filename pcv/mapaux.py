# ##########################################################
# Created on Fri Sep 02 2022
# 
# __author__ = Mohit Anand
# __copyright__ = Copyright (c) 2022, PCV Project
# __credits__ = [Mohit Anand,]
# __license__ = MIT License
# __version__ = 0.0.0
# __maintainer__ = Mohit Anand
# __email__ = itsmohitanand@gmail.com
# __status__ = Development
# ##########################################################

# The script will contain the things related to maps
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl

p1 = {
    "blue" : "#7776BC",
    "lavender" : "#CDC7E5",
    "light_yellow" : "#FFFBDB", 
    "corn" : "#FFEC51", 
    "tomato" : "#FF674D"
}

p3_1 = {
    "blue" : "#8da0cb",
    "orange" : "#fc8d62",
    "green" : "#66c2a5"
}

chi_bins = [0, 0.05, 0.10, 0.25, 0.50, 1.0]

def custom_cmap(palette, p_bins, reverse = True):
    p_list=  []
    for key, val in palette.items():
        p_list.append(val) 

    if reverse == True:
        p_list.reverse()
    # assert len(p_list) == len(p_bins)
    cmap = mpl.colors.ListedColormap(p_list)
    norm = mpl.colors.BoundaryNorm(boundaries=p_bins, ncolors=cmap.N)
    return cmap, norm, p_bins

def hex_to_rgb_norm(hex):
    h = hex.lstrip("#")

    return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

def make_colorbar(fig, ax, custom_cmap, label):
    return fig.colorbar(
            mpl.cm.ScalarMappable(cmap=custom_cmap[0], norm=custom_cmap[1]),
            cax=ax,
            boundaries=custom_cmap[2],
            ticks=custom_cmap[2],
            spacing='proportional',
            orientation='horizontal',
            label=label,
        )

chi_cmap = custom_cmap(p1, chi_bins)

