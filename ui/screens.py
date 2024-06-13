from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from functools import partial
from iconfonts import icon
from tools import get_search_history, remove_from_history

from kivy.graphics import Rectangle, Color 
from kivy.app import App

class HomeScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Builder.load_file("kvs/home_screen.kv")
		


class DownloadScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Builder.load_file("kvs/download_screen.kv")
		
class SearchScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Builder.load_file("kvs/search_screen.kv")
		
	def on_enter(self):
		self.ids.search_text_bar.focus = True
		self.ids.history_label_container.clear_widgets()
		for i in get_search_history():
			if i == "":
				continue
			history_button = Button (
			text= i,
			halign= "left",
			valign= "center",
			font_size= "50px",
			size_hint_y= None,
			size_hint_x= .9,
			#text_size = [0, 0],
			color= (.25, .25, .25, 1),
			background_normal= "",
			background_down= "",
			background_color= (1, 1, 1, 1),
			on_release= partial (self.enter_text, i),
			)
			history_button.bind(
			texture_size= self.update_button_size_with_texture, size= self.update_button_size)
			
			self.ids.history_label_container.add_widget(history_button)
			
			delete_history_button = Button(
			text="%s"%icon("icofont-bin"),
			font_size= "50px",
			valign= "center",
			size_hint= (None, None),
			markup= True,
			color= (.25, .25, .25, 1),
			background_normal= "",
			background_down= "",
			background_color= (1, 1, 1, 1),
			on_release= partial (self.delete_from_history, i)
			)
			self.ids.history_label_container.add_widget(delete_history_button)
			
			
			
	def update_button_size(self, ins, size):
		ins.text_size= ins.size
		
	def update_button_size_with_texture(self, ins, size):
		ins.size = size
		ins.text_size= ins.size
		
		with ins.canvas.before:
			Color (1, 0, 0, .5)
			Rectangle (size=ins.size, pos= ins.pos)
		
		
		
	def enter_text(self, text, ins):
		self.ids.search_text_bar.text = text

	def delete_from_history(self, text, ins):
		remove_from_history(text)
		self.on_enter()
					
		