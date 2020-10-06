from socket import *
# In your command prompt, type in hostname and press enter.
# What comes up is your computer's hostname

class Client:
	def init(self, hostname, port):
		self.connectionSocket = socket(AF_INET, SOCK_STREAM)
		self.serverAddress = (hostname, port)
		self.connectionSocket.connect(self.serverAddress)
		self.isRunning = True
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
			self.connectionSocket.send(toServer.encode())
			data = self.connectionSocket.recv(1024).decode()
			if not data:
				print("[Client]: No response from the server.")
				break
			else:
				print("[Server]: {}".format(data))
	def input_handler(self, connection_socket, data):
		five = 5
	def shutdown(self):
		self.connectionSocket.close()
		print("[Client]: Disconnected from server.")

def main():
	client = Client()
	client.init("localhost", 5555)
	client.run()
	client.shutdown()

if __name__ == '__main__':
    main()