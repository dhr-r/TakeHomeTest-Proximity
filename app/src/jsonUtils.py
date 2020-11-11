import json

class VerificationException(Exception):
    """
    Custom Exception showing Verification issues
    """
    def __init__(self, message):
        message = "Verification Exception: " + message
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.msg = message

def checkAndConvertCustomerStringToJSON(s):
    """
    Function to convert the string read from file to JSON object.
    Fails if invalid structure
    """
    jObj = None
    try:
        jObj = json.loads(s)
    except:
        # TODO: Log issue here
        # raise VerificationException("Invalid JSON Object: Invalid Structure")
        return None

    verifyAndConvertCustomerObjectKeys(jObj)
    
    return jObj

def verifyAndConvertCustomerObjectKeys(jObj):
    """
    Wrapper for Customer Objects.
    
    Parameters:
        jObj: a dictionary like object containing the keys to be verified
    
    Raises:
        VerificationException: Any Error that occurred throughout the task
    """
    keyTypes = {'user_id': int, 'name': str, 'latitude': float, 'longitude': float}
    verifyAndConvertKeys(jObj, keyTypes)

def verifyAndConvertKeys(jObj, keyTypes):
    """
    Generic internal function that allows verification of required object keys 
        in a single layered object.
    Also converts the value held by the key to the correct datatype.

    Parameters:
        jObj: a dictionary like object containing the keys to be verified
        keyTypes: a dictionary containing the expected types

    Raises:
        VerificationException: Any Error that occurred throughout the task
    """
    for key, keyType in keyTypes.items():
        if key not in jObj:
            raise VerificationException("Invalid JSON Entry: Missing key: " + key)
        val = jObj[key]
        try:
            jObj[key] = keyType(val)
        except:
            raise VerificationException("Invalid JSON Entry: Type Mismatch: '" + str(val) + "' cannot be converted to " + keyType.__name__)