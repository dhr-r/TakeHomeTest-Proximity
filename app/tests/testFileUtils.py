import unittest
from memory_profiler import memory_usage
from src.fileUtils import readLineAsStream, writeToFile, createFileIfNotExists, appendToFile
from .generateFixtures import generateRandomFixture

FOLDER_PATH = "./tests/fixtures/"

class TestReadLineAsStream(unittest.TestCase):

    def test_correct(self):
        fp = FOLDER_PATH + "customers.txt"
        data = []
        # Reading as a stream
        readLineAsStream(fp, lambda line: data.append(line))

        # Expected output
        with open(fp, 'r') as f:
            expected = f.readlines()

        # Verification
        self.assertEqual(data, expected)

    def test_empty(self):
        fp = FOLDER_PATH + "empty.txt"
        data = []
        # Reading as a stream
        readLineAsStream(fp, lambda line: data.append(line))
        
        self.assertEqual(data, [])

    def test_incorrect(self):
        fp = FOLDER_PATH + "wrong.txt"
        # Should throw a file not found error
        with self.assertRaises(FileNotFoundError):
            readLineAsStream(fp, lambda x: None)

    def test_memory_large(self):
        fp = generateRandomFixture(count=10**6)
        # Utilising data as a stream
        m = memory_usage(lambda: readLineAsStream(fp, lambda line: line))
        # get max memory usage after subtracting initial memory usage
        memory_stream = max([a-m[0] for a in m]) 
        
        # Loading complete data into memory
        data = []
        m = memory_usage(lambda: readLineAsStream(fp, lambda line: data.append(line)))
        # get max memory usage after subtracting initial memory usage
        memory_load = max([a-m[0] for a in m])

        # Asserts that its atleast 100 times lesser memory consumption using as a stream
        if memory_stream != 0:
            self.assertGreater(memory_load/memory_stream, 100)

if __name__ == '__main__':
    unittest.main()