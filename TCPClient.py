import sys
import errno
from socket import *
# In your command prompt, type in hostname and press enter.
# What comes up is your computer's hostname

class Client:
	def init(self, hostname, port):
		self.connectionSocket = socket(AF_INET, SOCK_STREAM)
		self.serverAddress = (hostname, port)
		self.isRunning = self.connect_to(self.serverAddress)
		return self.isRunning
	def run(self):

		while self.isRunning:
			toServer = input("You: ")
			if "auth_shutdown" in toServer:
				# don't use a break here.
				# we want to send to the server.
				# let this little loop finish its last
				# iteration
				self.isRunning = False
			elif "exit" in toServer:
				# we can exit immediately.
				# don't bother our precious server.
				break
			self.send_to(self.connectionSocket, toServer)
			data = self.receive_from(self.connectionSocket)
			if not data:
				print("[Client]: No response from the server.")
				break
			else:
				self.input_handler(self.connectionSocket, data)
	def input_handler(self, connection_socket, data):
		print("[Server]: {}".format(data))
	# this function is called at the very begining to make sure
	# we have a valid username.
	def shake_hands(self):
		while True:
			name = input("Username: ")
			toServer = "req_username " + name + "\n"
			self.send_to(self.client_socket, toServer)
			fromServer = self.receive_from(self.client_socket)
			if "ack_username" in fromServer:
				self.username = name
				break
			else
				print("That username is unavailable.")
	def connect_to(self, address):
		result = False
		try:
			self.connectionSocket.connect(address)
			result = True
		except error as e:
			print("[Client]: Failed to connect. {}".format(e))
		return result
	def send_to(self, client_socket, data):
		try:
			data += "\n"
			client_socket.send(data.encode())
			return True
		except error as e:
			print(e)
			return False
	def receive_from(self, client_socket):
		try:
			data = client_socket.recv(1024).decode()
		except error as e:
			print(e)
			return None
		else:
			return data
	def shutdown(self):
		self.connectionSocket.close()
		print("[Client]: Disconnected from server.")

def main():
	client = Client()
	result = client.init("192.168.1.117", 5555)
	if result:
		client.run()
	client.shutdown()

if __name__ == '__main__':
    main()