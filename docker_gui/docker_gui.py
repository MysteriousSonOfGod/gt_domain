from gt_domain import *

dclient = DockerClient(base_url='tcp://127.0.0.1:2375')
dclient.login(username="gtdonny18")

Window.maximize()

class bubbles(Bubble):
	button_x=ObjectProperty()
	def __init__(self, **kwargs):
		super(bubbles, self).__init__(**kwargs)
		
class action(ActionBar):
	def __init__(self, **kwargs):
		super(action, self).__init__(**kwargs)
		
	def restart(self):
        	print(f'exec: {sys.executable} {["python"] + sys.argv}')
        	os.execvp(sys.executable, ['python'] + sys.argv)
	
class box_slot(BoxLayout):
	btext=StringProperty()
	button_x = ObjectProperty()
	def __init__(self, **kwargs):
		super(box_slot, self).__init__(**kwargs)
		
	def bubble(self, button=None):
		self.button_x.clear_widgets()
		self.button_x.add_widget(bubbles(button_x=self.button_x))

class tabs_slot(TabbedPanelItem):
	scroll_x, grid_x=[ObjectProperty() for i in range(2)]
	ID=StringProperty()
	
	def __init__(self, **kwargs):
		super(tabs_slot, self).__init__(**kwargs)
		
	def insert_docker(self, **kwargs):
		dc=eval(f"dclient.{self.ID}.list()")
		if len(self.grid_x.children) > 0:self.grid_x.clear_widgets()
		for i in dc:
			if self.ID == "containers":self.grid_x.add_widget(box_slot(btext=f"{i.name} image:{i.image.tags}"))
			elif self.ID == "images":self.grid_x.add_widget(box_slot(btext=f"{i.tags[0]}"))
			elif self.ID == "volumes":self.grid_x.add_widget(box_slot(btext=f"{i.name}"))
			elif self.ID == "networks":self.grid_x.add_widget(box_slot(btext=f"{i.name}"))
			elif self.ID == "services":self.grid_x.add_widget(box_slot(btext=f"{i.name}"))
								
class docker_home(Screen):
	tabs=[ObjectProperty() for i in range(1)]
	def __init__(self, **kwargs):
		super(docker_home, self).__init__(**kwargs)
		self.tabbed_panel()
		print(self.tabs.background_image)
		
	def tabbed_panel(self, **kwargs):
		for i in ["Images", "Containers", "Volumes", "Networks", "Services"]:
			self.tabs.add_widget(tabs_slot(text=i, ID=i.lower()))
		
class docker_root(BoxLayout):
	def __init__(self, **kwargs):
		super(docker_root, self).__init__(**kwargs)
		self.screen_m()
		self.orientation="vertical"
		
	def screen_m(self):
		self.sm=ScreenManager()
		self.action=action()
		self.sm.add_widget(docker_home())
		
		self.add_widget(self.sm, index=0)
		self.add_widget(self.action, index=1)
			
class docker_gui(App):
	def __init__(self, **kwargs):
		super(docker_gui, self).__init__(**kwargs)
		
	def build(self):
		return docker_root()
	
main_app=docker_gui()
main_app.run()

'''docker run -it --name kivy \
--env DISPLAY=${DISPLAY} \
--env="QT_X11_NO_MITSHM=1" \
--net=host --ipc=host \
--volume ${HOME}/Documents/gt_domain:/home/gt_domain \
--volume /tmp/.X11-unix:/tmp/.X11-unix \
--device=/dev/video0 \
--device=/dev/input \
gtdonny18/kivy:default
'''
