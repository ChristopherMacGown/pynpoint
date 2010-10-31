from pynpoint import client, config, protocol

host = config.hostname
port = config.port
packet = protocol.Packet('hi!', {'host': host, 'port': port})

client.Client().send(packet)
