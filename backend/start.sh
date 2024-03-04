#!/bin/bash

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source the virtual environment activation script
source "$DIR/venv/bin/activate"

# Start Gunicorn with the specified options
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 wsgi:app
