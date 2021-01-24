from opencv_gui import *
class HeartbeatSender(DatagramProtocol):
	def startProtocol(self):
		self.transport.connect("192.168.0.26", 8005)
		self.loopObj = LoopingCall(self.sendHeartBeat)
		self.loopObj.start(10, now=False)

	def stopProtocol(self):
		print("GT")

	def datagramReceived(self, datagram, address):
		print(datagram, address)
		print(self.numPorts)
		
	def connectionRefused(self):
		pass
		
	def sendHeartBeat(self):
		pass


application=Application("OpenCV Server")
udp_service=MulticastServer(8005, HeartbeatSender(), listenMultiple=True)
udp_service.setServiceParent(application)
