import socket
import threading

class Client:
	def init(self, host_name, port):
		self.user_name = raw_input("Username: ")

		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = (host_name, port)
		self.client_socket.connect(server_address)

		read_thread = threading.Thread(target=self.read_thread)
		read_thread.start()

		write_thread = threading.Thread(target=self.write_thread)
		write_thread.start()

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


def main():
	client = Client()
	client.init("localhost", 5555)

if __name__ == '__main__':
	main()
