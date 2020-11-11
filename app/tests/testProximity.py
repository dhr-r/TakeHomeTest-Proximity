import unittest, os
import timeout_decorator
from memory_profiler import memory_usage

from src.proximity import retrieveCustomersToInvite, verify_inputs, ProximityBasedCustomerFilter
from src.jsonUtils import VerificationException
from src.fileUtils import readLineAsStream
from .generateFixtures import generateRandomFixture

FIXTURES_FOLDER_PATH = "./tests/fixtures/"
TEMP_FOLDER_PATH = "./temp/"

class BaseTestClass(unittest.TestCase):

    def fixture_1(self):
        obj = {
            "local_fp": FIXTURES_FOLDER_PATH + "customers.txt",
            "radius": 100,
            "center_lat": 53.339428, 
            "center_long": -6.257664,
            "output": TEMP_FOLDER_PATH + "output"
        }
        expected_fp = FIXTURES_FOLDER_PATH + "expected_output.txt"
        return (obj, expected_fp)

    def fixture_remote_1(self):
        obj, expected_fp = self.fixture_1()
        del obj["local_fp"]
        obj["remote_address"] = "https://s3.amazonaws.com/intercom-take-home-test/customers.txt"
        
        return (obj, expected_fp)

    def fixture_2(self):
        obj, expected_fp = self.fixture_1()
        obj["local_fp"] = FIXTURES_FOLDER_PATH + "customers_2.txt"
        expected_fp = FIXTURES_FOLDER_PATH + "expected_output_2.txt"
        return (obj, expected_fp)

class TestRetrieveCustomersToInvite(BaseTestClass):
    
    def correctness_test(self, fixture):
        obj, expected_fp = fixture()
        error = retrieveCustomersToInvite(obj)

        # Check error
        self.assertEquals(error, None)

        if expected_fp is None:
            return
        # Check if correctly written in file
        with open(expected_fp, 'r') as f:
            op = f.read()
        with open(obj["output"], 'r') as f:
            exp = f.read()
        self.assertEquals(op, exp)
    
    def failure_test(self, obj):
        e = retrieveCustomersToInvite(obj)
        self.assertNotEquals(e, None)
        return e
    
    def test_failure(self):
        obj = {}
        e = self.failure_test(obj)
        self.assertEquals(e.split(":")[0], "Verification Exception")

    def test_correct_from_file(self):
        self.correctness_test(self.fixture_1)
        self.correctness_test(self.fixture_2)

    @timeout_decorator.timeout(10)  # Source: https://stackoverflow.com/a/34743601/5115992
    def test_correct_from_remote_source(self):
        # Check internet
        if not isInternetConnected():
            self.skipTest("Test requires Internet")

        # Test remote source fixture
        self.correctness_test(self.fixture_remote_1)

    def test_memory_large(self):
        obj, _ = self.fixture_1()
        obj["local_fp"] = generateRandomFixture(count=10**6)
        obj["output"] = TEMP_FOLDER_PATH + "output_large"
        # print(obj)
        self.correctness_test(lambda: (obj, None))
        
        # Performing correctness_test
        m = memory_usage(lambda: self.correctness_test(lambda: (obj, None)))
        # get max memory usage after subtracting initial memory usage
        max_memory_usage = max([a-m[0] for a in m]) 
        
        # get input file size
        file_size = os.path.getsize(obj["local_fp"])/(1024*1024) # in MBs

        # Asserts that memory usage is atleast 10 times lesser as compared to file size
        self.assertLessEqual(max_memory_usage * 10, file_size)

    def test_random_increasing_radius(self):
        obj, _ = self.fixture_1()
        obj["local_fp"] = generateRandomFixture(count=10**3)

        # Various radius's to check
        radius_list = [100, 500, 1000, 5000]

        class Counter:
            def __init__(self):     self.cnt = 0
            def increment(self):    self.cnt += 1
        
        last = 0
        # Loop over the radius
        for rad in radius_list:
            obj["radius"] = rad
            # Test correctness for that radius
            self.correctness_test(lambda: (obj, None))
            # Get number of lines (number of Customers)
            c = Counter()
            readLineAsStream(obj["output"], lambda line: c.increment())

            #  Check if current number of lines is atleast greater than last
            self.assertGreaterEqual(c.cnt, last)
            last = c.cnt

# HELPER FUNCTION
def isInternetConnected():
    # TODO: Find a better and more robust way
    import requests
    try:
        requests.get('https://www.google.com/').status_code
        return True
    except:
        pass
        
    return False

class TestVerify_inputs(BaseTestClass):
    
    def correctness_test(self, fixture):
        """
        Common method to test correctness
        """
        try:
            obj, _ = fixture()
            verify_inputs(obj)
        except Exception:
            self.fail()
    
    def failure_test(self, obj):
        """
        Common method to test failure
        """
        with self.assertRaises(VerificationException) as e:
            verify_inputs(obj)
        return e.exception.msg

    def missing_keys_test(self, fixture):
        obj, _ = fixture()
        keys = list(obj.keys())
        for key in keys:
            data = obj[key]
            del obj[key]
            self.failure_test(obj)
            obj[key] = data
    
################# TESTS #####################
    def test_correctness(self):
        for f in [self.fixture_1, self.fixture_2, self.fixture_remote_1]:
            self.correctness_test(f)
        
    def test_input_path_failure(self):
        self.assertEquals(self.failure_test({}), "Verification Exception: Input Object must contain either local_fp or remote_address")

    def test_output_path_failure(self):
        obj, _ = self.fixture_1()
        obj["output"] = TEMP_FOLDER_PATH
        self.assertEquals(self.failure_test(obj), "Verification Exception: Output path cannot be a directory")

    def test_missing_keys(self):
        for f in [self.fixture_1, self.fixture_remote_1]:
            self.missing_keys_test(f)

if __name__ == '__main__':
    unittest.main()