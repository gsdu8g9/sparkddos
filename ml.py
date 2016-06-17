#
#   Simple example of a multilayer perceptron to detect credit card fraud.
#   AXJ
#

# We use the native ml libraries
from __future__ import print_function
from pyspark import SparkContext
from pyspark.sql import SQLContext
from PIL import Image, ImageDraw, ImageTk
import Tkinter as Tk
import itertools as it
import os
import atexit

DIR = '/home/adrianj/Desktop/p/'
BACKGROUND_PATH = DIR+'WorldMap.jpg'
GOOD_PATH = DIR+'goodpoint.gif'
BAD_PATH = DIR+'badpoint.gif'
TITLE = "Clicks"

sc = SparkContext(appName=TITLE)
sqlContext = SQLContext(sc)
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

    def removeFile():

        for i in range(1, 53):
            fname = (DIR)+(("{}{:02d}.gif").format("gpoint", i))
            if os.path.isfile(fname): 
                os.remove(fname)
            fname = (DIR)+(("{}{:02d}.gif").format("bpoint", i))
            if os.path.isfile(fname):
                os.remove(fname)
            

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
    
    CircleDrawer(window, "bad").drawCircle(40, 500)
    window.mainloop()


