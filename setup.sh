#!/bin/bash

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the nostr module
pip install nostr

# Debugging: Check if nostr is installed
pip show nostr

echo "Virtual environment setup complete. 'nostr' module installed."
