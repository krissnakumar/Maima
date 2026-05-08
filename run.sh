#!/bin/bash
# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

# Run the application using the venv's python
./venv/bin/python3 maima/main.py
