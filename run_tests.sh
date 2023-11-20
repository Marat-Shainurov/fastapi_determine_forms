#!/bin/bash

pytest -vv

if [ $? -eq 0 ]; then

  ./run_app.sh
else
  exit 1
fi