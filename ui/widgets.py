import os
import re

from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import (StringProperty,
NumericProperty, ObjectProperty,
BooleanProperty, DictProperty, OptionProperty, ListProperty)
from kivy.app import App #only for root
import urllib
from pytube import request
from pytube.exceptions import AgeRestrictedError
import pytube 
from plyer import storagepath
from tools import second_format, convert_million

if platform == "android":
	from android.storage import *
	external_path = primary_external_storage_path() \
	if secondary_external_storage_path() == None\
	else secondary_external_storage_path()
else:
	external_path = storagepath.get_downloads_dir()


Builder.load_file("kvs/widgets.kv")


app_path = None
app_external_path = external_path

import re

def sanitize_filename(filename):
    # Replace invalid characters with an underscore
    sanitized = re.sub(r'[\\/:*?"<>|]', '_', filename)
    return sanitized


class SearchUI(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			root = App.get_running_app().root
			root.ids.sm.current = "search screen"

	

class ShowDownloadingLabel(Label):
	bg_canvas_color = ListProperty ((0, 0, 0, 0))
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(text= self.update_text)
		
	def update_text(self,ins, text):
		if int(text) > 0:
			self.bg_canvas_color = [1, 0, 0, .5]
			
			
class DownloadCard(BoxLayout):
	icon = StringProperty("")
	title = StringProperty ("")
	filesize = NumericProperty(0)
	state = OptionProperty ("waiting", options=["waiting", "downloading..."])
	length= StringProperty("0")
	root = ObjectProperty (None)
	data = DictProperty({})
	loaded_bytes = NumericProperty (0)
	cancel = BooleanProperty (False)
	def __init__(self, icon="", title="", length=0, data= {}, **kwargs):
		super ().__init__(**kwargs)
		self.icon = icon # video thumbnail 
		self.title = title	# video title
		self.length = length # video duration
		self.data = data # video data eg itag, quality



	def on_filesize(self, ins, val):
		print ("update ", val)

	def on_data(self, ins, data):
		try:
			self.filesize = data['contentLength']
		except KeyError:
			try:
				self.filesize = request.filesize(data["url"])
			except urllib.error.URLError:
				self.filesize = "0"
				
	def on_calcel(self, ins, value):
		if value:
			root.remove_downloading_list(self)
						
			
	def download(self, callback=None):
		data = self.data
		if data and self.cancel == False:
			path = app_external_path
			title = sanitize_filename(self.title)
			extension = data["mimeType"].split(";")[0]. split ("/")[1]
			filename= os.path.join(path, title+"."+extension)
			print('Type:', filename)
			with open(filename, "wb") as writer:
				try:
					chunks = request.stream(data["url"])
				except urllib.error.URLError:
					self.root.notify(message="not internet connection", toast=True)
				except ConnectionAbortedError:
					self.root.notify(message="not internet connection", toast=True)

				for chunk in chunks:
					if self.cancel:
						return 
					writer.write(chunk)
					self.loaded_bytes = self.loaded_bytes+len(chunk)
					print ("download chunk")
					
				callback (self)
				
				
				
class ViewCard(BoxLayout):
	title = StringProperty ("")
	source= StringProperty ("")
	length= StringProperty ("")
	views= StringProperty ("0")
	ytobject = ObjectProperty (None)
	dparent = ObjectProperty (None)
	is_live = BooleanProperty (False)
	quality_label = ListProperty ([])
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
	def on_ytobject(self, ins, obj):
		if obj:
			try:
				self.title = obj.title
				print (self.title)
				self.source = obj.thumbnail_url
				self.length = second_format(obj.length)
				self.views = convert_million(obj.views)
				try:
					self.quality_label = obj.streaming_data["formats"]
				except AgeRestrictedError as e:
					print(str(e))
					pass
				#live = obj.check_availability()
			except KeyError:
				self.quality_label = obj.streaming_data["adaptiveFormats"]
			except ConnectionAbortedError:
				app = App.get_running_app()
				app.root.notify(message="not internet connection", toast=True)
			except:
				raise