import socket
import sys
import threading


class ClientThread(threading.Thread):

	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.client = conn

	def run(self):
		while 1:
			data = self.client.recv(1024)
			if (data.rstrip() == '\x1b'):
				self.client.close()
				break
			else:
				response = str(data).rstrip() + " Han\n"
				self.client.sendall(response.encode('UTF8'))
		

class PyServer(object):

	def __init__(self):
		self.port = 8080
		self.queue_size = 10
		self.host = "localhost"
		self.read_buff_size = 1024
		self.server = None

	def setup_server(self):
		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind((self.host, self.port))
			self.server.listen(self.queue_size)
		except socket.error as msg:
			print(msg)
			if (self.server):
				self.server.close()
			sys.exit()
	
	def run(self):
		self.setup_server()
		while 1:
			conn, addr = self.server.accept()
			client = ClientThread(conn)
			client.start()

		self.server.close()

if __name__ == "__main__":
	server = PyServer()
	server.run()
