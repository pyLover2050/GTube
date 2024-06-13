from kivy.app import runTouchApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView 
from kivy.uix.label import Label
from iconfonts import icon, register 
from notification import Notification
import json

class MainWin (ScrollView):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.do_scroll_x= False
		self.child = GridLayout (cols=2, size_hint_y=None)
		self.child.height= self.child.minimum_height
		self.add_widget(self.child)
		file = open("icofont.fontd", "r")
		icons = json.loads(file.read())
		for i in icons:
			lb = Label(text="%s"%icon(i), size_hint=(None, None), markup=True)
			self.child.add_widget(lb)
			lb= Label(text= i, size_hint_y=None)
			self.child.add_widget(lb)
			
		
		
register("default_font", "icofont.ttf", "icofont.fontd")		
runTouchApp (MainWin ())