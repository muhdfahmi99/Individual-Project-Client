import socket
import threading

HEADER = 64
PORT = 8760
SERVER = '192.168.208.9'
DISCONNECT_MSG = 'DISCONNECT'

ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_msg(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' '*(HEADER-len(send_length))
	client.send(send_length)
	client.send(message)
	print(client.recv(1024).decode(FORMAT))

def client_main():
	connected = True
	send_msg("Connection Established")
	while connected:
		message = input("MSG: ")
		if message == 'disconnect':
			connected = False
			break
		send_msg(message)
	send(DISCONNECT_MSG)

client_main()
