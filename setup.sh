#!/bin/bash

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the nostr module
pip install nostr
pip install websockets
pip install colorama

# Debugging: Check if nostr is installed

echo "Virtual environment setup complete. 'nostr' module installed."

#pip show nostr
#pip show websockets

