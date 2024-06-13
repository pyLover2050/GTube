from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

import iconfonts
import json
from os.path import join, dirname

f = json.load(open("/storage/emulated/0/Mycd/yt/libs/garden/garden.iconfonts/iconfont_sample.fontd"))




class MainWin (GridLayout):
	def __init__(self, **kwargs):
		super ().__init__(**kwargs)
		self.cols = 4
		for i in f:
			self.add_widget(Label(
			text= iconfonts.icon(i), markup= True, size_hint= (None, None))
			)
			
			
class MyApp (App):
	def build (sef):
		return MainWin ()
		

if __name__=="__main__":
	iconfonts. register('default_font', 'iconfont_sample.ttf',
             join(dirname(__file__), 'iconfont_sample.fontd'))
	MyApp ().run()
		
		