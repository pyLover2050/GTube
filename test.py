from kivy.app import App, runTouchApp 
from kivy.lang import Builder
from kivy.uix.image import AsyncImage

from threading import Thread 

b = Builder.load_string("""
BoxLayout:
	orientation: "vertical"
	canvas.before:
		Color:
			rgba: 1, 1, 1, 1
		Rectangle:
			size: self.size
			pos: self.pos
	ScrollView:
		do_scroll_x: False
		BoxLayout:
			id: con
			orientation: "vertical"
			size_hint_y: None
			height: self.minimum_height
			AsyncImage:
				size_hint_y: None
				height: 400
				allow_stretch: True
				keep_radio: False
				source: "https://upload.wikimedia.org/wikipedia/commons/f/f9/Phoenicopterus_ruber_in_S%C3%A3o_Paulo_Zoo.jpg"
			
		
	Button:
		size_hint_y: None
		on_release: app.lload()
	""")

class MyApp (App):
	def build (self):
		return b

	def lload(self):
		t = Thread (target=self.load)
		t.start()
	
	def load(self):
		for i in range (50):
			im = AsyncImage (
			size_hint_y= None,
			height= 400,
			source= "https://upload.wikimedia.org/wikipedia/commons/f/f9/Phoenicopterus_ruber_in_S%C3%A3o_Paulo_Zoo.jpg"
			)
			b.ids.con.add_widget(im)
			
			
MyApp ().run()