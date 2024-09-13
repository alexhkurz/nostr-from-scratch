import sys
import os

# Debugging: List contents of the nostr package directory
import nostr
nostr_path = os.path.dirname(nostr.__file__)
print(f"Contents of the nostr package directory ({nostr_path}):")
print(os.listdir(nostr_path))

# Debugging: Print the Python path
print("Python path:")
print(sys.path)

print("Python executable:", sys.executable)

try:
    from nostr.relay import Relay
    from nostr.event import Event
    from nostr.key import PrivateKey
except ModuleNotFoundError as e:
    print("Module not found: ", e)
    print("Please ensure the 'nostr' module is installed. You can install it using 'pip install nostr'.")
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
print("Event class methods:", dir(Event))

# Debugging: Inspect the PrivateKey class
print("PrivateKey class methods:", dir(PrivateKey))

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
print("WebSocket connection opened.")
print("Attempting to publish event...")
relay.publish(event)
print("Event published successfully.")
