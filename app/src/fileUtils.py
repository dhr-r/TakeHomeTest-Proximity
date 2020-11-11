import os
import urllib.request

def download_data(url, fp):
    """ Reads from URL and saves to file
    Parameters:
        url: URL to read from
        fp: Filepath to save on
    """

    data = urllib.request.urlretrieve(url, fp)

def readLineAsStream(fp, fn):
    """
    Function that allows the file to be read one line at a time.
    Also ensures to close the file properly in case of any error.

    Parameters:
        fp: file path for the file to be read from
        fn: the external function that will be run on each line
    """
    with open(fp, 'r') as f:
        for line in f:
            fn(line)

def writeToFile(fp, data):
    """
    Function that allows to write to a file.
    Also ensures to close the file properly in case of any error.

    Parameters:
        fp: file path for the file to be written into
        data: the data to be written into the file
    """
    with open(fp, 'w') as f:
        f.write(data)

def createFileIfNotExists(fp):
    """
    Creates a file if it does not exist. 
    """
    if not os.path.exists(fp):
        open(fp, 'w').close()

def appendToFile(fp, data):
    """
    Function that allows to append to a file.
    Also ensures to close the file properly in case of any error.

    Parameters:
        fp: file path for the file to be written into
        data: the data to be written into the file
    """
    with open(fp, 'a') as f:
        f.write(data)
