import overpy
import numpy as np
import numpy.random
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import tqdm
from PIL import Image
Image.MAX_IMAGE_PIXELS = 933120000
api = overpy.Overpass()

raw = "42.049475,-87.678077,42.060154,-87.668861"
bbox = "42.0468547205597,-87.681519985199,42.0627791681205,-87.6654374599457"
bbox = "42.0627791681205,-87.681519985199,42.0468547205597,-87.6654374599457"
# BBox = [-87.678077, -87.668861, 42.049475, 42.060154]
BBox = [-87.681519985199,-87.6654374599457, 42.0468547205597, 42.0627791681205]

# node(42.0468547205597,-87.681519985199,42.0627791681205,-87.6654374599457);

# fetch all ways and nodes
result = api.query("""
    way(42.0468547205597,-87.681519985199,42.0627791681205,-87.6654374599457) ["highway"];
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

# for node in result.nodes:
#     print("Name: %s" % node.tags.get("name", "n/a"))
#     # print("  Highway: %s" % way.tags.get("highway", "n/a"))
#     # print("  Amenity: %s" % node.tags.get("amenity", "n/a"))
#     print("  Nodes:")
#     print(node.lat, node.lon)

for way in result.ways:
    print("Name: %s" % way.tags.get("name", "n/a"))
    # print("  Highway: %s" % way.tags.get("highway", "n/a"))
    print("  Amenity: %s" % way.tags.get("amenity", "n/a"))
    print("  Nodes:")
    if len(way.nodes) is 1:
        print(way.nodes)
        # for node in way.nodes:
        #     print("    Lat: %f, Lon: %f" % (node.lat, node.lon))

# background_path = './code/background_1.jpeg'
# background = plt.imread(background_path)

# fig, ax = plt.subplots(figsize=(8, 5))
# ax.set_title('Plotting')
# ax.set_xlim(BBox[0], BBox[1])
# ax.set_ylim(BBox[2], BBox[3])
# ax.imshow(background, zorder=0, extent=BBox, aspect='equal')

# # L = len(result.ways)
# # pbar = tqdm.tqdm(L)
# for way in result.ways:
#     # pbar.update()
#     x, y = [], []
#     for index, node in enumerate(way.nodes[:-1]):
#         y.append(node.lat)
#         x.append(node.lon)
#     color = [np.random.randint(1000)/1000 for i in range(3)]
#     # markerfacecolor=color,  marker='H'
#     ax.plot(x, y, c=color, alpha=0.8, linewidth=0.1,  marker='o', markersize=0.3, markeredgewidth=0)
#     # ax.text(x[0], y[0], way.tags.get("name", "n/a"))  

# fig = plt.gcf()
# # plt.show()
# # plt.plot()

# # plt.rcParams['figure.figsize'] = (8.0, 4.0)
# plt.rcParams['savefig.dpi'] = 2000
# fig.savefig('matched_1.jpg')