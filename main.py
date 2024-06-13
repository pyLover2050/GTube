import os
import sys

import kivy
from kivy.app import App
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock, mainthread
from kivy.config import Config
from kivy.animation import Animation

from kivy.properties import (
	NumericProperty,
	ListProperty,
	ObjectProperty,
	BooleanProperty,
)

from plyer import storagepath
from iconfonts import register

import threading
import urllib


from yt import YouTubeD
from tools import add_search_history

if platform == 'android':
	import android
	from android.permissions import Permission, request_permissions, check_permission
	from android.storage import (
		primary_external_storage_path,
		secondary_external_storage_path
	)
	from notification import AndroidNotification as notification
else:
	android = None


	
__version__ =  "0.0.5"

if platform == "android":
	external_path = primary_external_storage_path() \
	if secondary_external_storage_path() == None\
	else secondary_external_storage_path()
else:
	external_path = storagepath.get_downloads_dir()


app_path = None
app_external_path = os.path.join(external_path, "yt loader")
app_log_dir = os.path.join(app_external_path, "logs")
					
		

class MainWin(BoxLayout):
	avl = BooleanProperty (False)
	downloading_list = ListProperty([])
	ytobjects = ListProperty ([])
	last_download_object = ObjectProperty(None)
	err_type = ObjectProperty (None)
	exit_number = NumericProperty (0)
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.yt = YouTubeD()
		Window.bind(on_keyboard= self.keyboard_key_pressed)

	def watch(self):
		url = self.yt.url
		if url:
			android.open_url(url)
			#"https://api.whatsapp.com/send/?phone=919987537919&text=hii"
			
	def select_quality(self, obj):
		pass
			
									
	def download(self, obj, data):
		if obj.title in [i.title for i in self.downloading_list]:
			return

		if self.ids.downloader_scroll not in \
		self.ids.second_body.children:
			self.ids.second_body.add_widget(self.ids.downloader_scroll)
		data = {
		"title": obj.title,
		"icon": obj.thumbnail_url,
		"length": second_format(obj.length),
		"data": data
		}
		dbox = DownloadCard(**data)
		self.ids.downloading_box_con.add_widget(dbox)
		self.downloading_list.append(dbox)
				
						
	def insert_url(self, url):
		if url:
			is_url = url.startswith("https://")
			try:
				if is_url:
					ytobjects = self.yt.load_url(url)
				else:
					ytobjects= self.yt.search(url)
					add_search_history(url)
					
				self.ytobjects = ytobjects 
				self.url = url
			except pytube.exceptions.RegexMatchError:
				info = self.ids.show_info
				info.text = "incorrect url please enter correct one!"
				info.open()
			except urllib.error.URLError:
				self.notify(message="no internet connection", toast=True)
			except ConnectionAbortedError:
				self.notify(message="no internet connection", toast=True)
			except Exception as e:
				info = self.ids.show_info
				info.text = str(e)
				info.open()
				
				
	def search(self, text):
		home_screen = self.ids.home_screen
		home_body = self.ids.home_screen.ids.home_body_widget
		home_scroller = self.ids.home_screen.ids.home_scroller
		loader_label = self.ids.home_screen.ids.loader_label
		
		if text:
			home_screen.ids.search_blind.text = text
			try:
				self.ids.sm.current = "home"
				if home_scroller in home_body.children:
					home_body.remove_widget(home_scroller)
				if loader_label not in home_body.children:
					home_body.add_widget(loader_label)
					
				ani = Animation (p= 360, d=1)+Animation (p=0, d=0)
				ani.repeat = True
				ani.start(loader_label)
				th = threading.Thread(target=self.insert_url, args=(text,))
				th.start()
			except:
				pass
	
	def viewcards_add_ytobject(self):
		home_body = self.ids.home_screen.ids.home_body_widget
		viewbox_container = self.ids.home_screen.ids.viewbox_container
		for w, t in zip(viewbox_container.children[::-1],
		self.ytobjects):
			w.ytobject = t
		
		
	@mainthread	
	def on_ytobjects(self, ins, objs):
		home_body = self.ids.home_screen.ids.home_body_widget
		home_scroller = self.ids.home_screen.ids.home_scroller
		loader_label = self.ids.home_screen.ids.loader_label
		viewbox_container = self.ids.home_screen.ids.viewbox_container
		if objs:
			if loader_label in home_body.children:
				home_body.remove_widget(loader_label)
			if home_scroller not in home_body.children:
				home_body.add_widget(home_scroller)
				
			
			viewbox_container.clear_widgets()
			for obj in objs:
				vb = ViewCard()
				vb.dparent = self
				viewbox_container.add_widget(vb)
			self.viewcards_add_ytobject()
				
				
	
	def download_complete(self, obj):
		if obj in self.downloading_list:
			self.ids.downloading_box_con.remove_widget(obj)
			self.downloading_list.remove(obj)
			try:
				self.notify(title="Download Successfull", message=f"{obj.title}", app_icon="icon.png")
			except:
				pass
			finally:
				del obj 

	def on_downloading_list(self, ins, obj):
		self.ids.home_screen.ids.count_downloading_label.text = \
		str(len(obj))
		if threading.active_count() <= 4:
			if obj:
				if self.ids.info_not_downloading in \
				self.ids.second_body.children:
					self.ids.second_body.remove_widget(self.ids.info_not_downloading)
				if self.ids.downloader_scroll not in \
				self.ids.second_body.children:
					self.ids.second_body.add_widget(self.ids.downloader_scroll)
					
				t = threading.Thread(target=obj[-1].download, args= (self.download_complete, ))
				t.start()
			else:
				if self.ids.info_not_downloading not in self.ids.second_body.children:
					self.ids.second_body.add_widget( self.ids.info_not_downloading)
					if self.ids.downloader_scroll in self.ids.second_body.children:
						self.ids.second_body.remove_widget(self.ids.downloader_scroll)
	
	def remove_downloading_list(self, obj):
		if obj in self.downloading_list:
			self.ids.downloading_box_con.remove_widget(obj)
			self.downloading_list.remove(obj)
	
	@mainthread				
	def notify(self, title="", message="",app_icon="", toast=False, ticker= "", timeout= 10):
		notification().notify(
		title=title,
		message= message,
		toast= toast,
		app_icon=app_icon,
		ticker= ticker,
		timeout= timeout
		)
				
						
	def keyboard_key_pressed(self, win, key, *largs):
		if key == 27:
			self.exit_number = self.exit_number+1
			if self.ids.sm.current == "home":
				if self.exit_number > 1:
					sys.exit(0)
				else:
					self.notify(message="press once again", toast=True)
					Clock.schedule_once(self.exit_number_release, 1)
					
			else:
				self.ids.sm.current = "home"
			return True

	def exit_number_release(self, dt):
		self.exit_number = 0
		
		
		
		
		
		
		
class MainApp(App):
	def build(self):
		return MainWin()
		
	def on_start(self):
		super().on_start()
		# request permission if not granted 
		try:
			pr = [Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
			for i in pr:
				has_permission= check_permission(i)
				all_permission_ok.append(has_permission)
					
			if all([i==True for i in all_permission_ok]):
				Config.set("kivy", "log_dir", app_log_dir)
			else:
				request_permissions(pr)
		except Exception as e:
			info = self.root.ids.show_info
			err_type, err, tb = sys.exc_info()
			info.text = (str(err_type)+str( err))
			info.open()
			pass

	def on_pause(self):
		return True
		
		
if __name__=="__main__":
	register("default_font", "icofont.ttf", "icofont.fontd")
	register("ui-font", "ui-icofont.ttf", "ui-fonts.fontd")
	from ui.screens import *
	from ui.popups import *
	from ui.widgets import *
	app = MainApp()
	app.run()