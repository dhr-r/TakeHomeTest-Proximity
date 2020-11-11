from .jsonUtils import checkAndConvertCustomerStringToJSON, verifyAndConvertKeys, VerificationException
from .distanceUtils import getSphericalDistance, GeoPoint
from .fileUtils import createFileIfNotExists, readLineAsStream, writeToFile, appendToFile, download_data
import os, time

TEMP_FOLDER_PATH = "./temp/"

def retrieveCustomersToInvite(obj):
    """
    Wrapper method for catching and handling any exceptions.
    Parameters:
        obj: A dictionary object consisting of the following keys

    Returns:
        error: Any Error that occurred throughout the task
    """
    obj["cleaner"] = Cleanup()
    error = None
    try:
        retrieveCustomersToInviteInternal(obj)
    except VerificationException as e:
        # TODO: Log the error
        error = e.msg
    except Exception as e:
        # TODO: Log the error
        error = str(e)

    obj["cleaner"].clean()

    return error       

def retrieveCustomersToInviteInternal(obj):
    """
    The Main Controller Function that will be exposed.

    It retrieves the customers to be invited and outputs them.
    It supports the following:
    - Fetching from a Local File
    - Fetching from a Remote File
    - Search Radius Definition from a CENTER point
    - CENTER point Definition
    - How to output the solution: PRINT or saved in a file 

    Parameters:
        obj: A dictionary object consisting of the following keys
            local_fp: The local file path for the file to be read from
            remote_address: The remote address for the file to be read from
            radius: The search radius upto which invitations can be sent from a defined CENTER
            center_lat: The latitude for the CENTER point from which the distances will be calculated
            center_long: The longitude for the CENTER point from which the distances will be calculated
            output: Can be either 'PRINT' or a file path to the saved into
    """

    # VERIFY IF INPUTS TO THIS FUNCTION ARE VALID
    verify_inputs(obj)
    
    # Download file if required
    if "local_fp" not in obj:
        obj["local_fp"] = TEMP_FOLDER_PATH + "data_" + str(time.time())
        writeToFile(obj["local_fp"], "")
        download_data(obj["remote_address"], obj["local_fp"])
        obj["cleaner"].add(lambda: os.remove(obj["local_fp"]))

    # SET UP CLASS
    p = ProximityBasedCustomerFilter(latitude=obj['center_lat'], longitude=obj['center_long'], radius=obj["radius"])

    # Iterate over the file
    readLineAsStream(obj["local_fp"], p.doForEachLine)

    # Sort Customers to be invited
    p.sortCustomersByID()

    # Output the Customers
    out = "Office Location:- {}, {}\nRadius:- {} kms\n\nCustomers to be invited:\n".format(obj['center_lat'], obj['center_long'], obj["radius"])
    if obj["output"] == "PRINT":
        print(out)
        obj["output_fn"] = print
    else:
        writeToFile(obj["output"], out)
        # create a function
        obj["output_fn"] = lambda data: appendToFile(obj["output"], "\n" + data)

    # output the customers
    p.outputEachCustomer(obj["output_fn"])

def verify_inputs(obj):
    """
    Helper function to verify if the inputs to the function are valid.

    Raises:
        VerificationException: Any Error that occurred throughout the task
    """
    # file path
    path = 'local_fp'
    if 'local_fp' not in obj or obj['local_fp'] is None:
        if 'remote_address' in obj and obj['remote_address'] is not None:
            path = 'remote_address'
        else:
            raise VerificationException("Input Object must contain either local_fp or remote_address")

    # key verification and type conversion
    keyTypes = {path: str, 'radius': float, 'center_lat': float, 'center_long': float, 'output': str}
    verifyAndConvertKeys(obj, keyTypes)

    # output check
    if obj["output"] != "PRINT":
        fp = obj["output"]
        try:
            createFileIfNotExists(fp)
            writeToFile(fp, "")
        except IsADirectoryError:
            raise VerificationException("Output path cannot be a directory")

class ProximityBasedCustomerFilter:
    """
    Class that manages distance checks and orders the IDs.
    """

    def __init__(self, latitude, longitude, radius):
        self.center = GeoPoint(latitude, longitude)
        self.radius = radius

        self.customers = []

    def doForEachLine(self, line):
        # Get Object
        obj = checkAndConvertCustomerStringToJSON(line)
        if obj is None:
            return

        # Get Distance
        dist = getSphericalDistance(self.center, GeoPoint(obj["latitude"], obj["longitude"]))
        
        # Decide whether to invite or not
        if dist > self.radius:
            # TODO: Log this information
            return
        
        # Remember this customer for future
        self.rememberCustomer(obj)
        
    def rememberCustomer(self, obj):
        # store the customer information in a list
        self.customers.append((obj["user_id"], obj["name"]))

    def sortCustomersByID(self):
        # sort the customers by ID
        self.customers.sort(key=lambda x: x[0])

    def outputEachCustomer(self, fn):
        for (id, name) in self.customers:
            fn("{}: {}".format(id, name))

class Cleanup:
    """
    Helper class to assist code cleanup
    """
    def __init__(self):
        self.fns = []
    def add(self, fn):
        self.fns.append(fn)
    def clean(self):
        for fn in self.fns:
            fn()