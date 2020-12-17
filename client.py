import socket
import threading
import time

#color codes
OKBLUE = '\033[94m'
OKYELLOW = '\033[93m'
OKGREEN = '\033[92m'
OKRED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'

HEADER = 64
PORT = 8760
SERVER = '192.168.208.9'
DISCONNECT_MSG = OKRED+BOLD+'#DISCONNECT'+ENDC

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

username = input(OKBLUE+"Enter your username: "+ENDC)
send_msg(username)
user_result = client.recv(1024).decode(FORMAT)
if user_result == "False":
	print (OKRED+BOLD+f"User account {username} was not found"+ENDC)
	print (OKRED+"Creating new account with same username"+ENDC)
	password = input(OKBLUE+"Enter new password: "+ENDC)
	password = username+"::"+password
	send_msg(password)
	result = client.recv(1024).decode(FORMAT)
	if result == "True":
		print (OKGREEN+BOLD+"User has been successfully added, Restart application"+ENDC)
		send_msg(DISCONNECT_MSG)
	else:
		print (OKRED+BOLD+"Unable to add new user, please try again later..."+ENDC)
		send_msg(DISCONNECT_MSG)
else:
	password = input(OKBLUE+"Enter password: "+ENDC)
	if user_result == password:
		text_msg = OKYELLOW+"Log in to the chat room"+ENDC
		for text in text_msg:
			print (text, end='', flush=True)
			time.sleep(0.04)
		print("\n")
		def client_main():
			connected = True
			send_msg(OKYELLOW+f"{username} has join the chat room"+ENDC)
			text_msg = OKYELLOW+"To send your message press ctrl+c"+ENDC
			for text in text_msg:
				print (text, end='', flush=True)
				time.sleep(0.04)
			print("\n")
			while connected:
				try:
					msg_check()
					print ("\n")
					message = input(OKBLUE+"MSG: "+ENDC)
					if message == 'disconnect':
						connected = False
						break
					send_msg(message)
				except KeyboardInterupt:
					connected = False
					break
			send_msg(DISCONNECT_MSG)
		send_msg(OKYELLOW+f"{username} has join the chat room"+ENDC)
		client_main()
	else:
		print (OKRED+BOLD+"Wrong password"+ENDC)
		send_msg(DISCONNECT_MSG)
