import sys
sys.path.append('../')
import localization.update_json as update
# import geocoder
import warnings as warn
warn.filterwarnings("ignore")

from geopy.geocoders import Nominatim  # for location


def get_location(address):
    '''
    :param address: address of the detected and retrieved landmark as string
    :return: location of landmark as a list [long,lat]
    '''
    try:
        geolocator = Nominatim(user_agent = "Landmark Location") # landmark location is the app name
        location = geolocator.geocode(address)
        # print(location.address)
        # print('Location:', (location.latitude,location.longitude))
        lat  = round(location.latitude,4)
        long = round(location.longitude,4)
        if lat is None or long is None:
            lat = 0
            long = 0

        loc_geo = (lat,long)
        # update.update_json(location = loc_geo)
        return loc_geo

    except AttributeError:
        print("Landmark Location Not available! Scan other landmarks")

