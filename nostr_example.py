import sys
import os
import nostr
from colorama import init, Fore, Style

# Initialize colorama
init()
nostr_path = os.path.dirname(nostr.__file__)

# Debugging: List contents of the nostr package directory
print(Fore.GREEN + f"Contents of the nostr package directory ({nostr_path}):" + Style.RESET_ALL)
print(str(os.listdir(nostr_path)))

# Debugging: Print the Python path
print(Fore.GREEN + "Python path:" + Style.RESET_ALL)
print(str(sys.path))

print(Fore.GREEN + "Python executable:" + Style.RESET_ALL, sys.executable)

try:
    from nostr.relay import Relay
    from nostr.event import Event
    from nostr.key import PrivateKey
except ModuleNotFoundError as e:
    print(Fore.RED + "Module not found: " + Style.RESET_ALL, e)
    print(Fore.RED + "Please ensure the 'nostr' module is installed. You can install it using 'pip install nostr'." + Style.RESET_ALL)
    exit(1)

# Generate a new private key
private_key = PrivateKey()

# Create a new event
event = Event(  
    public_key=private_key.public_key.hex(),
    content="Hello, Nostr!",
    kind=1
)

# Debugging: Inspect the Event class
print(Fore.GREEN + "Event class methods:" + Style.RESET_ALL, str(dir(Event)))

# Debugging: Inspect the PrivateKey class
print(Fore.GREEN + "PrivateKey class methods:" + Style.RESET_ALL, str(dir(PrivateKey)))

# Compute the event ID
event_id = event.compute_id(
    public_key=event.public_key,
    created_at=event.created_at,
    kind=event.kind,
    tags=event.tags,
    content=event.content
)

# Sign the event using the private key
event.signature = private_key.sign_event(event)

# Nostr Relays and WebSockets Explanation:
# 
# Nostr (Notes and Other Stuff Transmitted by Relays) is a decentralized protocol for creating and sharing content.
# It uses relays to transmit messages between clients. Relays are servers that accept messages from clients and
# broadcast them to other clients. This allows for a decentralized and distributed network of communication.
#
# WebSockets are a protocol for full-duplex communication channels over a single TCP connection. They are used in
# Nostr to maintain a persistent connection between the client and the relay. This allows for real-time communication
# and updates.
#
# In this script:
# - We import MessagePool and RelayPolicy from the nostr module.
# - We create a relay connection to a WebSocket server running on ws://localhost:8080.
# - We open the WebSocket connection and attempt to publish the event.
# - We print messages indicating the success of the connection and event publication.
#
# The retry logic ensures that if the connection fails, it will attempt to reconnect multiple times before giving up.
# This helps in handling transient network issues or temporary unavailability of the relay server.

from nostr.message_pool import MessagePool
from nostr.relay_manager import RelayPolicy

# Connect to a relay
policy = RelayPolicy()
message_pool = MessagePool()
relay = Relay("ws://localhost:8080", policy, message_pool)

import time
from websocket import WebSocketConnectionClosedException

# Open the WebSocket connection with retry logic
max_retries = 5
retry_delay = 2  # seconds

for attempt in range(max_retries):
    try:
        relay.connect()
        print(Fore.GREEN + "WebSocket connection opened." + Style.RESET_ALL)
        break
    except Exception as e:
        print(Fore.RED + f"Failed to open WebSocket connection (attempt {attempt + 1}/{max_retries}): {e}" + Style.RESET_ALL)
        time.sleep(retry_delay)
else:
    print(Fore.RED + "Failed to open WebSocket connection after multiple attempts." + Style.RESET_ALL)
    exit(1)

print(Fore.GREEN + "Attempting to publish event..." + Style.RESET_ALL)
try:
    if relay.ws.sock and relay.ws.sock.connected:
        relay.publish(event)
        print(Fore.GREEN + "Event published successfully." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Failed to publish event: WebSocket connection is closed." + Style.RESET_ALL)
except WebSocketConnectionClosedException as e:
    print(Fore.RED + f"WebSocket connection closed unexpectedly: {e}" + Style.RESET_ALL)
except Exception as e:
    print(Fore.RED + f"An error occurred while publishing the event: {e}" + Style.RESET_ALL)
