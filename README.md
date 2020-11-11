# TakeHomeTest-Proximity

### Introduction
This repository is built as a solution to a take home test for finding customers to be invited within 100km of an office location; sorted by user_id

### Prerequisites
Needs `Python 3` installed or `Docker` installed.

### How to run
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
