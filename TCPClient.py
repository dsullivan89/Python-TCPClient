from socket import *
# In your command prompt, type in hostname and press enter.
# What comes up is your computer's hostname

class Client:
	def init(self, hostname, port):
		self.connectionSocket = socket(AF_INET, SOCK_STREAM)
		self.serverAddress = (hostname, port)
		self.connectionSocket.connect(self.serverAddress)
	def run(self):
		toServer = input("You: ")
		self.connectionSocket.send(toServer.encode())
		data = self.connectionSocket.recv(1024).decode()
		if not data:
			self.connectionSocket.close()
			return
		else:
			print(data)
	def input_handler(self, connection_socket, data):
		pass
	def shutdown(self):
		self.connectionSocket.close()

def main():
	client = Client()
	client.init("localhost", 5555)
	client.run()
	client.shutdown()

if __name__ == '__main__':
    main()