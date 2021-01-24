from gt_domain.opencv_gui import *

class opencv_client(DatagramProtocol):
	def startProtocol(self):
		print("connect: ")
		self.transport.joinGroup('224.0.0.1')

	def stopProtocol(self):
		pass

	def datagramReceived(self, datagram, address):
		print(datagram)
