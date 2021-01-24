from gt_domain import *

class Contents(BoxLayout):
	def __init__(self, **kwargs):
		super(Contents, self).__init__(**kwargs)
		
class Container(Button):
	count=NumericProperty(0)
	contents=ObjectProperty()
	def __init__(self, **kwargs):
		super(Container, self).__init__(**kwargs)
		
class dropdown_root(BoxLayout):
	grid_root=ObjectProperty
	switch=BooleanProperty(False)
	containers=ListProperty()
	
	def __init__(self, **kwargs):
		super(dropdown_root, self).__init__(**kwargs)
		Clock.schedule_once(self.setup)
		
	def setup(self, *args):
		self.setup_containers(names=["A", "B", "C", "D", "E", "F"])
		
	def setup_containers(self, names=[]):
		self.containers=[]
		for i in names:
			self.containers.append(Container(text=i))
		
		for container in self.containers:
			self.grid_root.add_widget(container)
			container.fbind("on_release", self.click_container)
		return self.containers
		
	def click_container(self, button):
		button.count = (button.count + 1) % 2
		
		for index, container in enumerate(self.containers):
			if button is container:
			#All other containers below the selected container
				drop_index=range(index+1, len(self.containers))
				for i in drop_index:
					self.content_dropdown(container=self.containers[i], button=button)

	def content_dropdown(self, container=None, button=None):
		content_height=0
		content_height= container.y-160 if button.count == 1 else container.y+160
			
		anim=Animation(y=content_height, duration=0.5)
		anim.start(container)
		
class dropdown_x(App):
	def __init__(self, **kwargs):
		super(dropdown_x, self).__init__(**kwargs)
		
	def build(self):
		return dropdown_root()
		
dropdown_x().run()
