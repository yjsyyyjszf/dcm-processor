#!/bin/bash

if [ $1 = "closed" ]
then
  python -m pip install -r "$2"
fi
