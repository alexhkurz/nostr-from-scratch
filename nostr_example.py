import sys
import pkg_resources
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
    pkg_resources.get_distribution('nostr')
    print("'nostr' module is installed.")
except pkg_resources.DistributionNotFound:
    print("'nostr' module is not installed.")
    print("Please install it using 'pip install nostr'.")
    exit(1)

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

# Sign the event
event.signature = private_key.sign(event.serialize())

# Connect to a relay and publish the event
relay = Relay("ws://localhost:8080")
relay.publish(event)
