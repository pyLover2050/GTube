from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage 
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty 
from kivy.lang import Builder
#from yt import YTLoader
from tools import second_format
from kivy.animation import Animation
import threading 
from pytube import Search 
#from kivy.garden.icofonts import resigter

#yt = YTLoader ()
#yt.load("https://youtu.be/-FTNbqxCfhA")
from kivy.garden.iconfonts import icon, create_fontdict_file, register 

#create_fontdict_file("icofont/icofont/icofont.css", "icofont.fontd")
register("default_font", "icofont.ttf", "icofont.fontd")

class BBox(BoxLayout):
	source= StringProperty ("")
	title = StringProperty ("")
	length = StringProperty ("")
	views = NumericProperty (0)
	ytobjects= ListProperty (None)
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
	def search (self):
		s = Search ("twinkle twinkle")
		ytobjects= s.results
		self.ytobjects = ytobjects
		self.ids.bt.text = "search fill"

	def start(self):
		ani = Animation (p=360, d=2)+Animation (p=0, d=2)
		ani.repeat = True
		ani.start(self.ids.lb)
		th = threading.Thread(target=self.search)
		th.start()
		
	def on_ytobjects(self, ins, obj):
		self.remove_widget(self.ids.lb)

		
b = Builder.load_string("""
#: import icon iconfonts.icon
BoxLayout
	orientation: "vertical"
	ScrollView:
		do_scroll_x: False
		size_hint_y: .9
		BoxLayout:
			id: con
			orientation: "vertical"
			size_hint_y: None
			height: self.minimum_height
	Button:
		text: "go"
		size_hint_y: .1
		on_release: app.go()
			
""")



#b = BBox()
#b.source = yt.yt.thumbnail_url
#b.title = yt.yt.title
#b.length = second_format(yt.yt.length)
#b.views = yt.yt.views
class MyApp (App):
	def build (self):
		return b
	def go(self):
		objs = Search ("pathan")
		#print (dir(objs))
		for i in objs.results:
			url = i.thumbnail_url
			im = AsyncImage (source=url, size_hint_y=None, height=400)
			self.root.ids.con.add_widget(im)


MyApp ().run()