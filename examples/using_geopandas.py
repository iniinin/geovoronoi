"""
Example script to show how to incorporate GeoPandas with geovoronoi.

Author: Markus Konrad <markus.konrad@wzb.eu>
March 2018
"""

import logging

import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.ops import cascaded_union

from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from geovoronoi import voronoi_regions_from_coords, points_to_coords


logging.basicConfig(level=logging.INFO)
geovoronoi_log = logging.getLogger('geovoronoi')
geovoronoi_log.setLevel(logging.INFO)
geovoronoi_log.propagate = True

#
# load geo data
#

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

# focus on South America, convert to World Mercator (unit: meters)
south_am = world[world.continent == 'South America'].to_crs(epsg=3395)
cities = cities.to_crs(south_am.crs)   # convert city coordinates to same CRS!

# create the bounding shape as union of all South American countries' shapes
south_am_shape = cascaded_union(south_am.geometry)
south_am_cities = cities[cities.geometry.within(south_am_shape)]   # reduce to cities in South America


#
# calculate the Voronoi regions, cut them with the geographic area shape and assign the points to them
#

# convert the pandas Series of Point objects to NumPy array of coordinates
coords = points_to_coords(south_am_cities.geometry)

# calculate the regions
poly_shapes, pts, poly_to_pt_assignments = voronoi_regions_from_coords(coords, south_am_shape)


#
# Plotting
#

fig, ax = subplot_for_map()

plot_voronoi_polys_with_points_in_area(ax, south_am_shape, poly_shapes, pts, poly_to_pt_assignments)

ax.set_title('Cities data for South America from GeoPandas\nand Voronoi regions around them')

plt.tight_layout()
plt.savefig('using_geopandas.png')
plt.show()


