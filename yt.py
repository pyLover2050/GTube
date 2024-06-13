import os
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context


from pytube import YouTube, Search 
#from android.storage import secondary_external_storage_path, primary_external_storage_path

# external_path = primary_external_storage_path() \
# if secondary_external_storage_path() == None\
# else secondary_external_storage_path()


# self_path = os.path.join(external_path, "yt loader")

def convert_bytes(bytes_number):
    tags = [ "B", "Kb", "Mb", "Gb", "Tb" ]
 
    i = 0
    double_bytes = bytes_number
 
    while (i < len(tags) and  bytes_number >= 1024):
            double_bytes = bytes_number / 1024.0
            i = i + 1
            bytes_number = bytes_number / 1024
 
    return str(round(double_bytes, 2)) + " " + tags[i]
 
		
		
class YouTubeD:
	def __init__(self):
		self.data = []
		self.method = ""
		
	def load_url(self, url):
		if url:
			self.method = "url"
			yt = YouTube (url)
			if self.data:
				self.data.clear()
			self.data.append(yt)
			return self.data
			
	def search(self, query):
		if query:
			self.method = "search"
			yt = Search(query)
			if self.data:
				self.data.clear()
			self.data.extend(yt.results)
		return self.data