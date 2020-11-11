from math import cos, sin, acos, radians

# Source: https://en.wikipedia.org/wiki/Earth_radius#Mean_radius
EARTH_RADIUS_KMS = 6371.0088

class GeoPoint:
    """
    Class that stores information about a point on earth in radians
    """
    def __init__(self, latitude, longitude, isRadians=False):
        self.lat = latitude if isRadians else radians(latitude)
        self.long = longitude if isRadians else radians(longitude)
    
    def __repr__(self):
        return "<GeoPoint: {}, {}".format(self.lat, self.long)

def getSphericalDistance(c1, c2):
    """
    Calculate the Spherical Distance between two points on the globe.

    Source: https://en.wikipedia.org/wiki/Great-circle_distance#Formulae
    """

    # delta between longitudes
    delta_long = abs(c2.long - c1.long)

    # Calculating the expression
    exp = sin(c1.lat) * sin(c2.lat)  +  cos(c1.lat) * cos(c2.lat) * cos(delta_long)
    # Bounding the expression from -1 to 1
    if exp > 1: exp = 1
    if exp < -1: exp = -1

    # central angle between point 1 and point 2
    delta_sigma = acos(exp)

    # distance, in KMs, is central angle * Earth radius
    return EARTH_RADIUS_KMS * delta_sigma