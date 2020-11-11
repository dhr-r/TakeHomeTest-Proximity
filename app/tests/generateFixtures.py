from src.fileUtils import writeToFile, createFileIfNotExists, appendToFile
from time import time
import random, string, os
from json import dumps

FOLDER_PATH = "./tests/fixtures/"

def getRandomLatitude():
    """
    Get random Latitude
    """
    return random.random()*180 - 90

def getRandomLongitude():
    """
    Get random Longitude
    """
    return random.random()*360 - 180

def generateRandomCase(id):
    return {
        "latitude": getRandomLatitude(), 
        "user_id": id, 
        "name": ''.join(random.choices(string.ascii_lowercase, k=3)), 
        "longitude": getRandomLongitude()
    }

def generateFixture(radius=10, within=5, count=10):
    fp = FOLDER_PATH + "generated-{}-{}-{}".format(radius, within, count)
    if os.path.exists(fp):
        return fp
    createFileIfNotExists(fp)

    for i in range(count):
        appendToFile(fp, dumps(generateRandomCase(i)) + "\n")

    return fp

def generateRandomFixture(count=10):
    fp = FOLDER_PATH + "generated-random-" + str(count)
    if os.path.exists(fp):
        return fp
    createFileIfNotExists(fp)

    for i in range(count):
        appendToFile(fp, dumps(generateRandomCase(i)) + "\n")

    return fp
