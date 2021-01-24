import cv2, sys, os, cvui, numpy as np

class snap_capture(object):
	cam=None
	cvui.init("Control")
	counter=0
	
	record=[False]
	handsign_state=[False]
	
	def __init__(self, **kwargs):
		self.__dict__.update(**kwargs)
		self.cam=cv2.VideoCapture(0)
		
		cv2.createTrackbar("thresh", "Control", 140, 255, lambda x:None)
		cv2.createTrackbar("x", "Control", 440, 1000, lambda x:None)
		cv2.createTrackbar("y", "Control", 115, 1000, lambda x:None)
		cv2.createTrackbar("w", "Control", 180, 1000, lambda x:None)
		cv2.createTrackbar("h", "Control", 145, 1000, lambda x:None)
		
	def handsign_capture(self, local_image, global_image, x, y, w, h):
		cvui.text(global_image, 0, 0, f"images: {self.counter}")
		thresh=cv2.getTrackbarPos("thresh", "Control")
		local_image = cv2.cvtColor(local_image, cv2.COLOR_BGR2GRAY)
		local_image= local_image[y:y+h, x:x+w]
		
		ret, local_image = cv2.threshold(local_image, thresh, 255, cv2.THRESH_BINARY_INV)
		cvui.rect(global_image, x, y, w , h, 0xff0000)
		cv2.imshow("Image", local_image)
		
	def record_images(self, handsign):
		self.counter+=1
		cv2.imwrite(f"../dataset/handsign/test/option/hs{self.counter}.png", handsign)
		
	def user_interface(self, global_image):
		handsign=global_image.copy()
		cvui.checkbox(global_image, 0,50, "handsign", self.handsign_state)
		cvui.checkbox(global_image, 0,75, "start recording", self.record)
		x=cv2.getTrackbarPos("x", "Control")
		y=cv2.getTrackbarPos("y", "Control")
		w=cv2.getTrackbarPos("w", "Control")
		h=cv2.getTrackbarPos("h", "Control")
				
		if self.handsign_state[0] == True:
			self.handsign_capture(handsign, global_image, x,y,w,h)
			 
		if self.record[0] == True:
			self.record_images(handsign)
			
		#cv2.destroyWindow("Image")
			
		cv2.imshow("Control", global_image)
		cvui.update()
		
	def show_capture(self, *args):
		print(self.cam.isOpened())
		while(self.cam.isOpened()):
			ret, frame=self.cam.read()
			if cvui.button(frame, 0, 150, "Quit"):
				break
			self.user_interface(global_image=frame)
			if(cv2.waitKey(1) > 0):pass
		self.cam.release()
		cv2.destroyAllWindows()
		
snap_capture().show_capture()

