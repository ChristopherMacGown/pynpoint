import pynpoint
import socket

host = pynpoint.config.hostname
port = pynpoint.config.port

packet = pynpoint.protocol.Packet('hi!', {'host':host, 'port':port})

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.sendall(packet.encode())
