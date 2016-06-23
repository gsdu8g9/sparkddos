#
#   Simple example of a single layer neural net to detect DDoS attacks.
#   AXJ 2016
#

# We use the native ml libraries
from __future__ import print_function
# from pyspark import SparkContext
# from pyspark.sql import SQLContext
from PIL import Image, ImageDraw, ImageTk
import Tkinter as Tk
import itertools as it
import os
import atexit
import random
import urllib2
import math
import json


DIR = '/home/adrianj/Desktop/MachineLearning/Images/'
BACKGROUND_PATH = DIR+'MapMercator.jpg'
GOOD_PATH = DIR+'goodpoint.gif'
BAD_PATH = DIR+'badpoint.gif'
URL = "http://developer.usa.gov/1usagov"

TITLE = "Clicks"
FREQUENCY = 2000
block_size = 512
w = 2058
h = 1746

# sc = SparkContext(appName=TITLE)
# sqlContext = SQLContext(sc)
#data = sqlContext.read.format("libsvm").load("data/mllib/sample_multiclass_classification_data.txt")

class ImageSequence:
        def __init__(self, img):
            self.img = img
        def __getitem__(self, ix):
            try:
                if ix:
                    self.img.seek(ix)
                return self.img
            except EOFError:
                raise IndexError # end of sequence


class CircleDrawer(Tk.Frame):
        
    pictures = []
    gif = 0
    delay = 15
    label = 0
    fname_list = []
    lifetime = 100

    def __init__(self, parent, param):
        Tk.Frame.__init__(self, parent)
        
        self.delay = 15
        
        if param == "bad":
            self.gif = Image.open(BAD_PATH)
            name = "bpoint"
        else:
            self.gif = Image.open(GOOD_PATH)
            name = "gpoint"

        count = 1
        for frame in ImageSequence(self.gif):
            fname = (DIR)+(("{}{:02d}.gif").format(name, count))
            frame.save(fname)
            self.fname_list.append(fname)
            count += 1
        
    def animate(self):

        if self.lifetime == 0:
            self.label.destroy()
        else:
            self.lifetime -= 1
            gif = next(self.pictures)
            self.label["image"] = gif
            panel.after(self.delay, self.animate)


    def drawCircle(self, cx, cy):
        
        self.label =  Tk.Label(panel)
        self.label.pack()
        self.label.place(x = cx, y = cy)
        self.pictures = it.cycle(Tk.PhotoImage(file=img_name) for img_name in self.fname_list)
        self.animate()


if __name__ == "__main__":

    def mercatorProjection(latitude, longitude):

        u = (longitude+180.0)*(w/360.0)
        phi = latitude*math.pi / 180.0
        m = math.log(math.tan((math.pi / 4) + (phi/2)))
        v = (h/2.0) - (w*m/(2*math.pi))

        return (u, v)

    def cantorPairingFunction(x, y):
        return int(0.5*(x+y)*(x+y+1) + y)


    def removeFile():

        for i in range(1, 53):
            fname = (DIR)+(("{}{:02d}.gif").format("gpoint", i))
            if os.path.isfile(fname): 
                os.remove(fname)
            fname = (DIR)+(("{}{:02d}.gif").format("bpoint", i))
            if os.path.isfile(fname):
                os.remove(fname)
    
    global data
    data = ""

    def getData(chars):

    	u, v = -1, -1
    	index = -1

    	for i in range(0, len(chars)):
    		if chars[i].split(":")[0] == "\"ll\"":
    			index = i
    			break

    	if index == -1:
    		return (u,v)

    	u = (chars[index].split(":")[1]).split("[")[1]
    	v = (chars[index + 1]).split("]")[0]

    	return (float(u), float(v))


    def URLListener():
        
        a, b = "a", "b"
        global data

        try:
            buffer = response.read(block_size)
            if buffer:
            	
            	if data == "":
            		data = buffer.split("{")[1]
            	else:
            		temp = buffer.split("}")
            		if len(temp) <= 1:

            			data += temp[0]

            			if buffer[-1] == "}":
            				
            				chars = map(str, data.split(","))
            				chars[0] = chars[0][3:]
            				u, v = getData(chars)
            				a, b = mercatorProjection(u,v)
            				data = ""
            		else:

            			data += temp[0]
            			chars = map(str, data.split(","))
            			chars[0] = chars[0][3:]
            			u, v = getData(chars)
            			a, b = mercatorProjection(u, v)
            			data = temp[1]

        except Exception, e:
            print(e)
        
        if a != "a" and b != "b":
        	print(str(a) + " " + str(b))
        	CircleDrawer(window, "bad").drawCircle(int(a), int(b))
        
        window.after(FREQUENCY, URLListener)

    
    atexit.register(removeFile)
    image = Image.open(BACKGROUND_PATH)
    window = Tk.Tk()
    window.title(TITLE)
    window.configure(background='grey')
    window.geometry('{}x{}'.format(image.size[0], image.size[1]))

    img = ImageTk.PhotoImage(image)
    panel = Tk.Label(window, image = img)
    panel.image = img
    panel.pack(side="top", fill="both", expand=True)

    response = urllib2.urlopen(URL)
    print("Listening...")
    URLListener()
    window.mainloop()
