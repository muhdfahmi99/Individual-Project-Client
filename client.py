import socket
import threading
import time

#color codes
OKBLUE = '\833[94m'
OKYELLOW = '\833[93m'
OKGREEN = '\833[92m'
OKRED = '\833[91m'
BOLD = '\833[1m'
ENDC = '\833[0m'

HEADER = 64
PORT = 8760
SERVER = '192.168.208.9'
DISCONNECT_MSG = '#DISCONNECT'

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def msg_check():
	while True:
		try:
			message = client.recv(1024).decode(FORMAT)
			print (message)
		except KeyboardInterrupt:
			break

def send_msg(msg):
	msg = username+"::"+msg
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length+=b' '*(HEADER - len(send_length))
	client.send(send_length)
	client.send(message)

username = input("Enter your username:")
send_msg(username)
user_result = client.recv(1024).decode(FORMAT)
if user_result == "False":
	print (f"User account {username} was not found")
	print ("Creating new account with same username")
	password = input("Enter new password: ")
	password = username+"::"+password
	send_msg(password)
	result = client.recv(1024).decode(FORMAT)
	if result == "True":
		print ("User has been successfully added, Restart application")
		send_msg(DISCONNECT_MSG)
	else:
		print ("Unable to add new user, please try again later...")
		send_msg(DISCONNECT_MSG)
else:
	password = input("Enter password: ")
	if user_result == password:
		text_msg = "Log in to the chat room"
		for text in text_msg:
			print (text, end='', flush=True)
			time.sleep(0.04)
		print("\n")
		def client_main():
			connected = True
			send_msg("has join the chat room")
			text_msg = "To send your message press ctrl+c"
			for text in text_msg:
				print (text, end='', flush=True)
				time.sleep(0.04)
			print("\n")
			while connected:
				try:
					msg_check()
					print ("\n")
					message = input("MSG: ")
					if message == 'disconnect':
						connected = False
						break
					send_msg(message)
				except KeyboardInterupt:
					connected = False
					break
			send_msg(DISCONNECT_MSG)
		send_msg("has join the chat room")
		client_main()
	else:
		print ("Wrong password")
		send_msg(DISCONNECT_MSG)
