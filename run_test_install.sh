#!/bin/bash

if [ "$1" == "install" ]; then
    pip install -r requirement.txt

elif [ "$1" == "test" ]; then
    nosetests -s -v

elif [ "$1" == "run" ]; then
    python MDS.py
else
    echo "the argument can one of install/test/run"
fi
