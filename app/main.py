from src.proximity import retrieveCustomersToInvite

if __name__ == "__main__":
    CUSTOMERS_FILE_PATH = "./tests/fixtures/customers.txt"

    error = retrieveCustomersToInvite({
        "local_fp": CUSTOMERS_FILE_PATH,
        # "remote_address": None,
        "radius": 100,
        "center_lat": 53.339428, 
        "center_long": -6.257664,
        # "output": "PRINT"
        "output": "./temp/output"
    })
    if error is not None:
        print(error)