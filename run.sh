#!/bin/sh

if [ $1 == "test" ]; then
    echo
    echo "Note: When Running tests for the first time, it can take upto 2 minutes"
    echo
    python test.py
else
    python main.py "$@"
fi