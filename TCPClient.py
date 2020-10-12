import sys
import errno
from socket import *
# In your command prompt, type in hostname and press enter.
# What comes up is your computer's hostname

class Client:
	def init(self, hostname, port):
		self.user_name = raw_input("Username: ")

		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (host_name, port)
		self.client_socket.connect(self.server_address)

		read_thread = threading.Thread(target=self.read_thread)
		read_thread.start()

		write_thread = threading.Thread(target=self.write_thread)
		write_thread.start()

		self.isRunning = True
		return self.isRunning

	def read_thread(self):
		while True:
			try:
				message = self.client_socket.recv(1024).decode()
				if message == 'req_username':
					self.client_socket.send(self.user_name.encode())
				else:
					print(message)
			except:
				print("An error occured.")
				self.client_socket.close()
				break
	def write_thread(self):
		while True:
			message = '{}: {}'.format(self.user_name, raw_input(''))
			self.client_socket.send(message.encode())

	def run(self):
		self.shake_hands()
		while self.isRunning:
			if not self.isWaitingForFriends:
				toServer = raw_input("You: ")
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
			if data:
				if "att_match_found" in data:
					self.isWaitingForFriends = False
					print("Match found! Abuse that nerd!")
					continue
				self.input_handler(self.connectionSocket, data)
	def input_handler(self, connection_socket, data):
		print("[Server]: {}".format(data))
	# this function is called at the very begining to make sure
	# we have a valid username.
	def shake_hands(self):
		while True:
			name = raw_input("Username: ")
			toServer = "req_username " + name + "\n"
			self.send_to(self.connectionSocket, toServer)
			fromServer = self.receive_from(self.connectionSocket)
			if "ack_username" in fromServer:
				self.username = name
				print("Login success.")
				self.isWaitingForFriends = True
				print("Waiting for opponents...")
				break
			elif "req_denied" in fromServer:
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