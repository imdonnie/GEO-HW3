import overpy
import numpy as np
import numpy.random
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

api = overpy.Overpass()

bbox = [42.049475,-87.678077,42.060154,-87.668861]

# fetch all ways and nodes
result = api.query("""
    node(42.049475,-87.678077,42.060154,-87.668861) ["amenity"];
    (._;>;);
    out body;
    """)

# def inBbox(point):

# fig, ax = plt.subplots()
# for way in result.ways:
#     x, y = [], []
#     for index, node in enumerate(way.nodes[:-1]):
#         y.append(node.lat)
#         x.append(node.lon)
#     ax.plot(x, y, c=[np.random.randint(1000)/1000 for i in range(3)], alpha=0.5)
# plt.plot()
# plt.show()

for way in result.ways:
    print("Name: %s" % way.tags.get("name", "n/a"))
    # print("  Highway: %s" % way.tags.get("highway", "n/a"))
    print("  Amenity: %s" % way.tags.get("amenity", "n/a"))
    print("  Nodes:")
    for node in way.nodes:
        print("    Lat: %f, Lon: %f" % (node.lat, node.lon))