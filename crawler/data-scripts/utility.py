import shapefile
import matplotlib.path as mplPath
import numpy as np
from pymongo import MongoClient

myshp = open("neigh_data/ZillowNeighborhoods-NY.shp", "rb")
mydbf = open("neigh_data/ZillowNeighborhoods-NY.dbf", "rb")
r = shapefile.Reader(shp=myshp, dbf=mydbf)


def find_neighborhood(latitude, longitude):
    for x in r.shapeRecords():
        path = mplPath.Path(np.array([list(elem) for elem in x.shape.points]))
        y = (latitude, longitude)
        if path.contains_point(y):
            return x.record[3].lower().replace(" ", "_")

    return None


def get_db():
    connection = MongoClient('ds023654.mlab.com', 23654)
    db = connection['apartmentdb']
    db.authenticate('admin', 'craigslistsucks')

    return db


def print_names():
    db = get_db()
    for x in r.shapeRecords():
        # path = mplPath.Path(np.array([list(elem) for elem in x.shape.points]))
        print(x.record[3].lower().replace(" ", "_"))
        if 'New York City' in x.record[2]:
            for i in range(0, 5):
                output = {'name': str(x.record[3].lower().replace(" ", "_")) + '_' + str(i), 'avg_price': 0.0,
                          'count': 0, 'avg_num_bedrooms': 0.0, 'avg_num_bathrooms': 0.0, 'avg_sq_foot': 0.0,
                          'sq_foot_count': 0}
                db.neighborhoods.insert(output)
                # print(output)


# print_names()

# def ray_tracing_method(x, y, poly):
#
#     n = len(poly)
#     inside = False
#
#     p1x, p1y = poly[0]
#     for i in range(n+1):
#         p2x, p2y = poly[i % n]
#         if y > min(p1y, p2y):
#             if y <= max(p1y, p2y):
#                 if x <= max(p1x, p2x):
#                     if p1y != p2y:
#                         xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
#                     if p1x == p2x or x <= xints:
#                         inside = not inside
#         p1x, p1y = p2x, p2y
#
#     return inside
