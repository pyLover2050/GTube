def second_format(sec):
   sec = sec 
   hour = sec // 3600
   sec %= 3600
   min = sec // 60
   sec %= 60
   if hour > 0:
   	return "%02d:%02d:%02d" % (hour, min, sec)
   else:
   	return"%02d:%02d" %(min, sec)
   
   
   
def convert_million(num):
	if num >= 1000 and num  < 1000000:
		x = (num/1000)
		return f"{x:.1f}k"
	elif num >= 1000000 and num < 1000000000:
		x = (num/1000000)
		return f"{x:.1f}m"
	elif num >= 1000000000:
		x = (num/1000000000)
		return f"{x:.1f}b"
	else:
		return f"{num}"
		
		
def convert_bytes(bytes_number):
    tags = [ "B", "Kb", "Mb", "Gb", "Tb" ]
 
    i = 0
    double_bytes = bytes_number
 
    while (i < len(tags) and  bytes_number >= 1024):
            double_bytes = bytes_number / 1024.0
            i = i + 1
            bytes_number = bytes_number / 1024
 
    return str(round(double_bytes, 2)) + " " + tags[i]


def add_search_history(param):
	try:
		with open("history.txt", "r") as f:
			if len(f.readlines()) == 0:
				pass
			else:
				param = "\n"+param
	except:
		pass
	with open("history.txt", "a") as f:
		f.write(param)
		
def get_search_history(n=20):
	with open("history.txt", "r") as f:
		lines = f.read().split("\n")
		unique= list(set(lines))
		if len(unique) > 20:
			return unique[:20]
		return unique
		
		

def remove_from_history(text):
	with open("history.txt", "r") as f:
		data = f.read().split("\n")
		if text in data:
			data.remove(text)
			fl = "\n".join(data)
			with open("history.txt", "w") as w:
				w.write(fl)
			

		
def share_url(url):
        from kivy.utils import platform 
        if platform == 'android':
            from android.storage import primary_external_storage_path
            from jnius import autoclass
            from jnius import cast
            import os
            
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')

            shareIntent = Intent(Intent.ACTION_SEND)
            shareIntent.setType("text/plain")
            shareIntent.putExtra(Intent.EXTRA_TEXT, String (url))

            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            currentActivity.startActivity(shareIntent)
            
            
def shorten_text(text, font_size, size):
       from kivy.core.text import Label
       label = Label(text = text, shorten=True, shorten_from= "right", size=size, font_size=font_size)
       f = label.shorten(text)
       if "." in f:
     	  f = f[:f.index(".")+3]
       return f
       
             

#text = "Hello world and good evening I have a meeting with you and your family a happy new day source of your name is a b and"                   
#print (shorten_text(text, 10, (300, 300)))                                    