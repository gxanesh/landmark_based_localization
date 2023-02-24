'''
ref: https://stackoverflow.com/questions/24617013/convert-latitude-and-longitude-to-x-and-y-grid-system-using-python
'''

import math


def arc_to_deg(arc):
    """convert spherical arc length [m] to great circle distance [deg]"""
    return float(arc) / 6371 / 1000 * 180 / math.pi


def deg_to_arc(deg):
    """convert great circle distance [deg] to spherical arc length [m]"""
    return float(deg) * 6371 * 1000 * math.pi / 180


def latlon_to_xyz(lat, lon):
    """Convert angluar to cartesian coordiantes

    latitude is the 90deg - zenith angle in range [-90;90]
    lonitude is the azimuthal angle in range [-180;180]
    """
    r = 6371  # https://en.wikipedia.org/wiki/Earth_radius
    theta = math.pi / 2 - math.radians(lat)
    phi = math.radians(lon)
    x = r * math.sin(theta) * math.cos(phi)  # bronstein (3.381a)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)
    # return [round(x,2), round(y,2), round(z,2)]
    return [x,y]



def xyz_to_latlon(x, y, z):
    """Convert cartesian to angular lat/lon coordiantes"""
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = math.asin(z / r)  # https://stackoverflow.com/a/1185413/4933053
    phi = math.atan2(y, x)
    lat = math.degrees(theta)
    lon = math.degrees(phi)
    return [lat, lon]


lat_long = [
    37.3031,
    -78.2271
]



# print(lat_long)
# xyz = latlon_to_xyz(lat_long[0], lat_long[1])
# print(xyz)

# import utm
# xyz = utm.from_latlon(lat_long[0], lat_long[1])
# # (395201.3103811303, 5673135.241182375, 32, 'U')
# print(xyz)
