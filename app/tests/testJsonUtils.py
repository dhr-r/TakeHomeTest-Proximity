import unittest
from src.jsonUtils import checkAndConvertCustomerStringToJSON, verifyAndConvertCustomerObjectKeys, verifyAndConvertKeys, VerificationException

class TestVerifyAndConvertKeys(unittest.TestCase):

    def test_types_correct(self):
        # Test for a few types
        keyTypes = {'int': int, 'str': str, 'float': float, 'list': list}
        obj = {
            'int': 3,
            'str': "abc",
            'float': 4.323,
            'list': [1, 2, 3]
        }
        try:
            verifyAndConvertKeys(obj, keyTypes)
        except VerificationException as e:
            self.fail()

        # Verify types
        for k, v in keyTypes.items():
            self.assertEqual(type(obj[k]), v)

    def test_type_int(self):
        # Test various scenarios for int
        keyTypes = {'int': int}
        obj = {}
        # PASS
        obj['int'] = "3"
        try:
            verifyAndConvertKeys(obj, keyTypes)
        except VerificationException:
            self.fail()
        
        # FAIL
        obj['int'] = "3.4"
        with self.assertRaises(VerificationException) as e:
            verifyAndConvertKeys(obj, keyTypes)
        self.assertEquals(e.exception.msg.split(":")[2].strip(), "Type Mismatch")

        # FAIL
        obj['int'] = None
        with self.assertRaises(VerificationException):
            verifyAndConvertKeys(obj, keyTypes)
        self.assertEquals(e.exception.msg.split(":")[2].strip(), "Type Mismatch")

        # FAIL
        obj['int'] = "abc"
        with self.assertRaises(VerificationException):
            verifyAndConvertKeys(obj, keyTypes)
        self.assertEquals(e.exception.msg.split(":")[2].strip(), "Type Mismatch")

        # FAIL
        obj['int'] = ["abc"]
        with self.assertRaises(VerificationException):
            verifyAndConvertKeys(obj, keyTypes)
        self.assertEquals(e.exception.msg.split(":")[2].strip(), "Type Mismatch")

    def test_missing(self):
        obj = {}
        keyTypes = {"int": int}
        with self.assertRaises(VerificationException) as e:
            verifyAndConvertKeys(obj, keyTypes)
        self.assertEquals(e.exception.msg.split(":")[2].strip(), "Missing key")

class TestVerifyAndConvertCustomerObjectKeys(unittest.TestCase):

    def test_correct(self):
        obj = {'user_id': 10, 'name': "alpha", 'latitude': 123.31, 'longitude': 13.12}
        try:
            verifyAndConvertCustomerObjectKeys(obj)
        except VerificationException as e:
            self.fail()
    
    def test_missing(self):
        obj = {'user_id': 10, 'name': "alpha", 'latitude': 123.31, 'longitude': 13.12}
        keys = list(obj.keys())
        # Remove each key and test for missing keys
        for key in keys:
            data = obj[key]
            del obj[key]
            with self.assertRaises(VerificationException) as e:
                verifyAndConvertCustomerObjectKeys(obj)
            self.assertEqual(e.exception.msg.split(":")[2].strip(), "Missing key")
            obj[key] = data

class TestCheckAndConvertCustomerStringToJSON(unittest.TestCase):

    def main_fn__must_not_fail__test(self, s):
        try:
            obj = checkAndConvertCustomerStringToJSON(s)
        except VerificationException as e:
            self.fail()
        return obj

    def test_correct(self):
        s = '{"latitude": "52.986375", "user_id": 12, "name": "Christina McArdle", "longitude": "-6.043701"}'
        obj = self.main_fn__must_not_fail__test(s)

        self.assertNotEquals(obj, None)
        self.assertEqual(type(obj['user_id']), int)
        self.assertEqual(type(obj['latitude']), float)
        self.assertEqual(type(obj['longitude']), float)
        self.assertEqual(type(obj['name']), str)

    def test_incorrect(self):
        obj = self.main_fn__must_not_fail__test("{ ")
        self.assertEquals(obj, None)

    def test_empty(self):
        obj = self.main_fn__must_not_fail__test(" ")
        self.assertEquals(obj, None)

if __name__ == '__main__':
    unittest.main()