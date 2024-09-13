#!/bin/bash

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the nostr module
pip install nostr

# Ensure 'nostr' package is installed
pip install nostr

echo "Virtual environment setup complete. 'nostr' module installed."
