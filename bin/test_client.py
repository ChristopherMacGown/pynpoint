from pynpoint import client, protocol
from pynpoint.config import Config

config = Config()

host = config.server_hostname
port = config.server_port

announcement = protocol.Packet('hi!', {'host': host, 'port': port, 'addresses': [host]})
query = protocol.Packet('heard of?', {'type': 'addresses', 'value': host})

client.Client().send(query)
#client.Client().send(announcement)
