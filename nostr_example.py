import sys
import os
import nostr
from colorama import init, Fore, Style

# Initialize colorama
init()
nostr_path = os.path.dirname(nostr.__file__)

# Debugging: List contents of the nostr package directory
print(Fore.GREEN + f"Contents of the nostr package directory ({nostr_path}):" + Style.RESET_ALL)
print(Fore.YELLOW + str(os.listdir(nostr_path)) + Style.RESET_ALL)

# Debugging: Print the Python path
print(Fore.GREEN + "Python path:" + Style.RESET_ALL)
print(Fore.YELLOW + str(sys.path) + Style.RESET_ALL)

print(Fore.GREEN + "Python executable:" + Style.RESET_ALL, Fore.YELLOW + sys.executable + Style.RESET_ALL)

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
print(Fore.GREEN + "Event class methods:" + Style.RESET_ALL, Fore.YELLOW + str(dir(Event)) + Style.RESET_ALL)

# Debugging: Inspect the PrivateKey class
print(Fore.GREEN + "PrivateKey class methods:" + Style.RESET_ALL, Fore.YELLOW + str(dir(PrivateKey)) + Style.RESET_ALL)

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

from nostr.message_pool import MessagePool
from nostr.relay_manager import RelayPolicy

# Connect to a relay
policy = RelayPolicy()
message_pool = MessagePool()
relay = Relay("ws://localhost:8080", policy, message_pool)

# Open the WebSocket connection
relay.connect()
print(Fore.GREEN + "WebSocket connection opened." + Style.RESET_ALL)
print(Fore.GREEN + "Attempting to publish event..." + Style.RESET_ALL)
if relay.ws.sock and relay.ws.sock.connected:
    relay.publish(event)
    print(Fore.GREEN + "Event published successfully." + Style.RESET_ALL)
else:
    print(Fore.RED + "Failed to publish event: WebSocket connection is closed." + Style.RESET_ALL)
