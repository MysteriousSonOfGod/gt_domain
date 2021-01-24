from gt_domain import *

Builder.load_file("cvcustom.kv")
		
class Draw_Rectangle(BoxLayout):
	grid_x=ObjectProperty()
	x_co_ordinate, y_co_ordinate, w_co_ordinate, h_co_ordinate=[ObjectProperty() for i in range(4)]
	def __init__(self, **kwargs):
		super(Draw_Rectangle, self).__init__(**kwargs)
		Clock.schedule_once(self.setup)
		
	def setup(self, *args):
		self.x_co_ordinate.name="x"
		self.y_co_ordinate.name="y"
		self.w_co_ordinate.name="w"
		self.h_co_ordinate.name="h"
			
class Input_Holder(GridLayout):
	name=StringProperty()
	slider_value=NumericProperty()
	slider_x=ObjectProperty()
	
class TabbedScreen(TabbedPanelItem):
	opencv_cam=ObjectProperty()
	def __init__(self, **kwargs):
		super(TabbedScreen, self).__init__(**kwargs)
		Clock.schedule_once(self.setup)
		
	def setup(self, *args):
		self.clear_widgets()
		self.add_widget(self.opencv_cam)
	
##########*********** Camera Section ************###########
class OpencvCamera(Image):
	cv_root=ObjectProperty()
	capture = cv2.VideoCapture(0)
	def __init__(self, **kwargs):
		super(OpencvCamera, self).__init__(**kwargs)
		Clock.schedule_interval(self.update, 1.0/45.0)
		Clock.schedule_once(self.setup)
		
	def setup(self, *args):
		pass
		
	def update(self, dt):
		ret, frame = self.capture.read()
		frame=cv2.flip(frame, 0)
		
		draw_rectangle=self.draw_rectangle(frame)
		
		image_texture=Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgra')
		image_texture.blit_buffer(draw_rectangle.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
		self.texture=image_texture
		
	def draw_rectangle(self, image):
		rect_cv, x, y, w ,h=[None for i in range(5)]
		if self.cv_root.rect_cv:
			rect_cv=self.cv_root.rect_cv
			x=int(rect_cv.x_co_ordinate.slider_x.value)
			y=int(rect_cv.y_co_ordinate.slider_x.value)
			w=int(rect_cv.w_co_ordinate.slider_x.value)
			h=int(rect_cv.h_co_ordinate.slider_x.value)

		image=cv2.rectangle(image, (x,y),(x+w,y+h),(0,255,0),2)
		return image
		
class CVRoot(BoxLayout):
	sm, rect_cv=[ObjectProperty() for i in range(2)]
	def __init__(self, **kwargs):
		super(CVRoot, self).__init__(**kwargs)
		
class main(App):
	cv_root=ObjectProperty()
	def __init__(self, **kwargs):
		super(main, self).__init__(**kwargs)
		
	def build(self):
		self.cv_root=CVRoot()
		return self.cv_root
		
main().run()
