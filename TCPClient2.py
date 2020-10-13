import socket
import threading

class Client:
	keep_alive = True
	def init(self, host_name, port):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = (host_name, port)
		self.client_socket.connect(server_address)

		self.user_name = raw_input("Username: ")

		read_thread = threading.Thread(target=self.read_thread)
		read_thread.start()

		write_thread = threading.Thread(target=self.write_thread)
		write_thread.start()

		read_thread.join()
		write_thread.join()

	def read_thread(self):
		while self.is_alive():
			try:
				message = self.client_socket.recv(1024).decode()
				if "req_username" in message:
					self.client_socket.send(self.user_name.encode())
				elif "req_shutdown" in message:
					begin_shutdown()
					print("Goodbye!")

					break
				else:
					print(message)
			except:
				self.client_socket.close()
				self.begin_shutdown()
				break
	def write_thread(self):
		while self.is_alive():
			message = '{}: {}'.format(self.user_name, raw_input(''))
			try:
				self.client_socket.send(message.encode())
				if "auth_shutdown" in message:
					self.begin_shutdown()
					break
			except:
				break
	def is_alive(self):
		result = None
		lock = threading.Lock()
		lock.acquire()
		try:
			result = Client.keep_alive
		finally:
			lock.release()
			return result
	def begin_shutdown(self):
		lock = threading.Lock()
		lock.acquire()
		try:
			Client.keep_alive = False
		finally:
			lock.release()
			

def main():
	client = Client()
	client.init("192.168.1.117", 5555)

if __name__ == '__main__':
	main()
