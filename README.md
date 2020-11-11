# TakeHomeTest-Proximity

### Introduction
This repository is built as a solution to a take home test for finding customers to be invited within 100km of an office location; sorted by user_id

### Prerequisites
Needs `Python 3` installed or `Docker` installed.

### How to INSTALL, RUN and TEST
- Clone the repository
- Choose either Python or Docker installation given below:

#### --> Directly via Python
- Change environment if required
- Run the following commands for installation:
```
pip install -r requirements.txt
cd app
```
- To run:
```
python main.py
```
- To test:
```
python test.py
```

#### --> via Docker
- Run the following commands for building the docker file:
```
docker build . -t proximity
```
- To run:
```
docker run proximity
```
- To test:
```
docker run proximity test
```
### OUTPUT
The output for the default input is:
```
Office Location:- 53.339428, -6.257664
Radius:- 100.0 kms

Customers to be invited:

4: Ian Kehoe
5: Nora Dempsey
6: Theresa Enright
8: Eoin Ahearn
11: Richard Finnegan
12: Christina McArdle
13: Olive Ahearn
15: Michael Ahearn
17: Patricia Cahill
23: Eoin Gallagher
24: Rose Enright
26: Stephen McArdle
29: Oliver Ahearn
30: Nick Enright
31: Alan Behan
39: Lisa Ahearn
```

## Understanding Configuration
#### Parameters Explanation
```
local_fp        : The local file path for the file to be read from
remote_address  : The remote address for the file to be read from
radius          : The search radius upto which invitations can be sent from a defined CENTER
center_lat      : The latitude for the CENTER point from which the distances will be calculated
center_long     : The longitude for the CENTER point from which the distances will be calculated
output          : Can be either 'PRINT' or a file path to the saved into
```
#### Default configuration
```
"local_fp"    : "./tests/fixtures/customers.txt"
"radius"      : 100
"center_lat"  : 53.339428
"center_long" : -6.257664
"output"      : "PRINT"
```
## Changing the Configuration
The configuration can be easily changed by adding parameters at the end of the run commands using the following format:
`[parameter_name]=[parameter_value]`
*Note: There are no spaces between parameter name and parameter value*

For instance, if you want to change the **radius** to **150 kms** you will have to:
```
[RUN COMMAND] radius=150
```

Usage Example:
```
python main.py radius=150           # for python
docker run proximity radius=150     # for docker
```

### Multiple changes
Similary, changing the **local file path** and the **radius** can be done as follows
```
[RUN COMMAND] radius=150 local_fp=./tests/fixtures/customers_2.txt
```

### Deleting preset parameters
In order to delete preset parameters, you can simply set them to "null"

Usage Example: If we want to use a **remote address** instead of a **local file path**.
```
[RUN COMMAND] local_fp=null remote_address=https://s3.amazonaws.com/intercom-take-home-test/customers.txt
```

### Support for whitespaces
A file path could have a whitespace in it. Such file paths need to be enclosed with quotes.

For example: If a file path is `./tests/fixtures/customers 3.txt`.
##### Wrong Usage:
```
[RUN COMMAND] local_fp=./tests/fixtures/customers 3.txt
```
##### Correct Usage:
```
[RUN COMMAND] local_fp='./tests/fixtures/customers 3.txt'
```

## OTHER EXAMPLES:
#### 1. Change filepath for Docker to a path on local machine (Can be done by volume mounting)
```
docker run -v [LOCAL PATH TO FOLDER]:[DOCKER CONTAINER FOLDER PATH] proximity local_fp=[DOCKER CONTAINER FOLDER PATH]/[FILENAME] radius=1
```
Example:
```
docker run -v [LOCAL PATH]/app/tests/fixtures/:/app/temp2/ proximity local_fp=./temp2/customers_2.txt radius=1
```
Output:
```
Office Location:- 53.339428, -6.257664
Radius:- 1.0 kms

Customers to be invited:

101: Dhruv Reshamwala
```

#### 2. Testing for incorrect parameters
```
[RUN COMMAND] proximity output=null
```
Output:
```
Verification Exception: Invalid JSON Entry: Missing key: output
```

#### 3. Testing for incorrect parameters
```
[RUN COMMAND] proximity local_fp=null
```
Output:
```
Verification Exception: Input Object must contain either local_fp or remote_address
```
