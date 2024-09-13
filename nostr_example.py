try:
    from nostr.client.client import Client
    from nostr.event.event import Event
    from nostr.key import PrivateKey
except ModuleNotFoundError as e:
    print("Module not found: ", e)
    print("Please ensure the 'nostr' module is installed. You can install it using 'pip install nostr'.")
    exit(1)

# Generate a new private key
private_key = PrivateKey()

# Create a new event
event = Event(
    pubkey=private_key.public_key.hex(),
    content="Hello, Nostr!",
    kind=1
)

# Sign the event
event.sign(private_key.hex())

# Connect to a relay and publish the event
client = Client("ws://localhost:8080")
client.publish(event)
