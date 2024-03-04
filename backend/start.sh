#!/bin/bash

# Source the virtual environment activation script
source venv/bin/activate

# Start Gunicorn with the specified options
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 wsgi:app.py