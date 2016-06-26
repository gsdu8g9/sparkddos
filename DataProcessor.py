#
#   Parses the data as returned by the streamer.py class
#   AXJ 2016
#

#from pyspark.mllib.clustering import GaussianMixture
#from pyspark import SparkContext
from scipy.stats import multivariate_normal
from scipy.stats import logistic
import matplotlib.pyplot as plt
import numpy as np
import string
import math
import pickle

WIDTH = 2058
HEIGHT = 1746
DIR = "/home/adrianj/Desktop/MachineLearning/Resources/"
OUTPUT_FILE = DIR+"atemporalTrain.txt"
INPUT_FILE = DIR+"newTrainingSet.json"

def encodeString(name):
	ans = []
	for char in name:
		c = ord(char)
		if c < 10:
			ans.append('00' + str(c))
		elif c < 100:
			ans.append('0' + str(c))
		else:
			ans.append(str(c))
	return ''.join(ans)

def cantorPairingFunction(x, y):
	return int(0.5*(x+y)*(x+y+1) + y)

def mercatorProjection(latitude, longitude):
    u = (longitude+180.0)*(WIDTH/360.0)
    phi = latitude*math.pi / 180.0
    m = math.log(math.tan((math.pi / 4) + (phi/2)))
    v = (HEIGHT/2.0) - (WIDTH*m/(2*math.pi))
    return (u, v)

def doPlottingStuff():
	outputFile = open(OUTPUT_FILE)
	x, y = [], []

	for line in outputFile:
		a, b = tuple(map(float, line.strip('\n').split(' ')))
		x.append(a)
		y.append(b)

	outputFile.close()
	plt.plot(x, y, "x")
	plt.axis("equal")
	plt.title("Plot of latitude vs longitude in "+OUTPUT_FILE)
	plt.ylabel("Longitude")
	plt.xlabel("Latitude")
	plt.show()

'''
def generateRandomData(option, size):
	
	sc = SparkContext(appName=TITLE)
	gmm = pickle.load(open(DIR+"Model.sav", 'rb'))
	weights = pickle.load(open(DIR+"Weights.sav", 'rb'))
	numberOfGaussians = 180

	outputfile = open(DIR+"TrainingSet.txt", 'w')

	if option == "anomaly":
		pass	
	else:
		pass

	for _ in range(size):
		pass

	outputfile.close()
'''

###
# Parse the data
###
inputFile = open(INPUT_FILE)
outputFile = open(OUTPUT_FILE, "w")

for line in inputFile:

	## parse file

	dic = {}
	line = ((line.rstrip('\n').replace('}', '')).replace('{', '')).replace("\"", '')
	chars = line.split(",")
	key, value = "", ""

	for i in range(0, len(chars)):

		breaking = 0

		if chars[i].startswith("a:"):
			chars[i] = chars[i] + chars[i+1]
			del(chars[i+1])
		elif chars[i].startswith("ll:["):
			chars[i] = chars[i] + ","+ chars[i+1]
			del(chars[i+1])
			tmp = chars[i].split(":", 1)
			key = tmp[0]
			if len(tmp) > 1:
				value = tmp[1].replace("[", '').replace("]",'')
				a, b = tuple(map(float, value.split(",")))
				dic[key] = (a, b)
			else:
				dic[key] = ""
			break
				
		tmp = chars[i].split(":", 1)
		key = tmp[0]
		value = ""
		if len(tmp) > 1:
			value = tmp[1]
		dic[key] = value

		if 'c' not in dic:
			dic['c'] = "ZZ"

	## Write to outputfile
	cantor = cantorPairingFunction(dic["ll"][0], dic["ll"][1])
	#shorturl = encodeString(dic["hh"])
	refurl = encodeString(dic["r"])
	cc = encodeString(dic["c"])
	outputFile.write(str(cantor) + " " + cc +" "+ dic["nk"] +'\n')
	#a, b = mercatorProjection(dic["ll"][0], dic["ll"][1])
	#outputFile.write(str(a) +" " + str(HEIGHT - b) + '\n') #Height - b is necessary so that plots look correct
	

inputFile.close()
outputFile.close()
#doPlottingStuff()