import unittest
from src.distanceUtils import GeoPoint, getSphericalDistance, EARTH_RADIUS_KMS
from .generateFixtures import getRandomLatitude, getRandomLongitude
from math import radians
from random import random

class TestGetSphericalDistance(unittest.TestCase):

    def test_1(self):
        p1 = GeoPoint(0, 0)
        p2 = GeoPoint(10, 10)
        expected = 1568.5205567985759 # Source: https://www.onlineconversion.com/map_greatcircle_distance.htm
        calculated = getSphericalDistance(p1, p2)
        self.assertAlmostEqual(expected, calculated, places=2)

    def test_2(self):
        p1 = GeoPoint(0, 0)
        p2 = GeoPoint(0, 10)
        expected = 1111.9492664455872 # Source: https://www.onlineconversion.com/map_greatcircle_distance.htm
        calculated = getSphericalDistance(p1, p2)
        self.assertAlmostEqual(expected, calculated, places=2)

    def test_360_degree_wrap(self):
        p1 = GeoPoint(0 + 360, 0) # should be same as test_1
        p2 = GeoPoint(10, 10 + 360) # should be same as test_1
        expected = 1568.5205567985759 # same as test_1
        calculated = getSphericalDistance(p1, p2)
        self.assertAlmostEqual(expected, calculated, places=2)

    def test_acos_bounding_issue(self):
        # During testing, found the expression to be greater than 1 for the following input
        # Resulted in an error as acos(1.00000002) is Invalid
        # Problem due to floating point multiplication. 
        # Solved by adding bounds on the expressions output
        p = GeoPoint(1.087646681348228, 2.456310138185898, isRadians=True)
        calculated = getSphericalDistance(p, p)
        self.assertAlmostEqual(calculated, 0, places=2)

    def test_same_point(self):
        p = GeoPoint(getRandomLatitude(), getRandomLongitude())
        calculated = getSphericalDistance(p, p)
        self.assertAlmostEqual(calculated, 0, places=2)
    
    def test_along_a_longitude(self):
        lon = getRandomLongitude() # Fixed
        lat = getRandomLatitude()
        # get a list of latitudes
        latitudes = range(-90, 91, 10)

        for latitude2 in latitudes:
            # get expected distance keeping longitude same
            expected = EARTH_RADIUS_KMS * radians(abs(latitude2-lat))

            # Calculate distance
            p1 = GeoPoint(lat, lon)
            p2 = GeoPoint(latitude2, lon)
            calculated = getSphericalDistance(p1, p2)
            self.assertAlmostEqual(expected, calculated, places=2)

    def test_along_a_latitude(self):
        lat = 0 # because across different latitudes, the radius is different and 
                    # radius of the earth can only be used for latitude 0
        lon = getRandomLongitude()

        # get a list of longitudes
        longitudes = range(-180, 181, 10)

        for longitude2 in longitudes:
            angle = abs(longitude2-lon)
            if angle > 180:
                angle = 360 - angle
            # get expected distance keeping latitude same
            expected = EARTH_RADIUS_KMS * radians(angle)

            # Calculate distance
            p1 = GeoPoint(lat, lon)
            p2 = GeoPoint(lat, longitude2)
            calculated = getSphericalDistance(p1, p2)
            self.assertAlmostEqual(expected, calculated, places=2)

if __name__ == '__main__':
    unittest.main()