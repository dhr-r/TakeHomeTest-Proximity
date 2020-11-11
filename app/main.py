from src.proximity import retrieveCustomersToInvite
from sys import argv

CUSTOMERS_FILE_PATH = "./tests/fixtures/customers.txt"

def main():
    obj = {
        "local_fp": CUSTOMERS_FILE_PATH,
        # "remote_address": None,
        "radius": 100,
        "center_lat": 53.339428, 
        "center_long": -6.257664,
        "output": "PRINT"
        # "output": "./temp/output"
    }
    print()
    parse_args_and_change_obj(argv[1:], obj)
    if "debug" in obj:
        print("==================== Configuration ====================")
        for k, v in obj.items():
            print(k, ":", v)
        print("=======================================================\n")

    error = retrieveCustomersToInvite(obj)
    if error is not None:
        print(error)
    else:
        print("============= Task Completed Successfully =============")

def parse_args_and_change_obj(args, obj):
    for arg in args:
        a = arg.split("=")

        # Ignore if incorrect format
        if len(a) != 2:
            continue

        # Special case
        if a[1] == "null":
            del obj[a[0]]
            continue

        # change object
        obj[a[0]] = a[1]
        

if __name__ == "__main__":
    main()