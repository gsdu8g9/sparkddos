import matplotlib.pyplot as plt
import numpy as np
import math

WIDTH = 2058
HEIGHT = 1746
OUTPUT_FILE = "trainingSet.txt"
INPUT_FILE = "TrainingSet.json"


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


	## Write to outputfile
	# cantor = cantorPairingFunction(dic["ll"][0], dic["ll"][1])
	a, b = mercatorProjection(dic["ll"][0], dic["ll"][1])
	outputFile.write(str(a) +" " + str(HEIGHT - b) + '\n') #Height - b is necessary so that plots look correct

inputFile.close()
outputFile.close()
#doPlottingStuff()