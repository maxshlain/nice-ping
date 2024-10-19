#! /bin/bash

# create new virtual environment with uv and python 3.12
uv venv --python 3.12

# activate the environment
source .venv/bin/activate

# install the requirements
uv pip install -r requirements.txt