from kivy.uix.modalview import ModalView
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, DictProperty

from kivy.lang import Builder
import urllib 
from tools import convert_bytes
from functools import partial
from pytube import request 

class SelectQuality (ModalView):
	ytobject= ObjectProperty (None)
	selected_data = DictProperty ({})
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Builder.load_file("kvs/select_quality.kv")
		
	def on_ytobject(self, ins, obj):
		self.ids.gl.clear_widgets()
		try:
			quary= obj.streaming_data["formats"]
		except KeyError:
			quary= obj.streaming_data["adaptiveFormats"]
			
		for i in quary:
			filesize = convert_bytes(0)
			try:
				filesize = convert_bytes(int(i["contentLength"]))
			except KeyError:
				try:
					filesize = convert_bytes(
					request.filesize(i["url"])
					)
				except urllib.error.URLError:
					pass

			check = CheckBox(group="a", size_hint=(None, None),
			background_radio_normal= "data/radio_normal.png",
			background_radio_down= "data/radio_active.png"
			)
			check.bind(active=partial(self.select_data, i))
			quality_label = Label(
			text=i["qualityLabel"],
			size_hint=(None, None),
			color= (.75, .75, .75, 1)
			)
			size_label = Label(text=filesize, size_hint_y= None, color=(.75, .75, .75, 1))
			self.ids.gl.add_widget(check)
			self.ids.gl.add_widget(quality_label)
			self.ids.gl.add_widget(size_label)
			
			
	def select_data(self, data, ins, value):
		if value:
			self.selected_data = data			
			
			