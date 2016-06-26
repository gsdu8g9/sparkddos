#
#   From the provided Gaussian Mixture Model, use a neural net to determine attacks.
#   AXJ 2016
#
from pyspark.mllib.clustering import GaussianMixtureModel
from pyspark import SparkContext
from scipy.stats import logistic
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math

DIR="/home/adrianj/Desktop/MachineLearning/Resources/"
FILE_PATH = DIR+"newTestSet.txt"
TITLE="GaussianMixtureModel"

sc = SparkContext(appName=TITLE)
gaussians = GaussianMixtureModel.load(sc, DIR+"GMM/")

print("Model loaded.")

def decodeString(arg):
	name = str(arg)
	if len(name)%3 == 1:
		name = '00' + name
	elif len(name)%3 == 2:
		name = '0' + name

	decoded = ""
	for i in xrange(len(name) - 1, 0, -3):
		decoded = decoded + chr(name[i]) + chr(name[i - 1]) + chr(name[i - 2])

	return decoded


def inverseCantor(num):
	w = math.floor((math.sqrt(8*num + 1) -1) / 2.0)
	t = (w**2 + w)/2.0
	return (int(num-t), int(w-num + t))


#sigmoid = logistic.cdf(x)
data = sc.textFile(FILE_PATH, 'rb')
parsedData = data.map(lambda line: np.array([float(x) for x in line.strip().split(' ')]))
	
print(parsedData)

'''
	file = open(DIR+"testSet.txt", 'rb')
	x = []
	for line in file:
		x.append(map(float, line.rstrip('\n').split(' ')))
		a = gaussians.predict(sc.parallelize([x]).collect())
		print(str(x[0]) + ": " + str(a))
'''
'''
	for i in x:
		judgment = gaussians.predict(i)
		
		if judgment < 0.5:
			lat, lon = inverseCantor(i[0])
			usr = decodeString(i[3])
			if usr == 0:
				usr = "Unknown user."
			else:
				usr = "Known user."
			cc = decodeString(i[2])
			print("Anomaly detected at ["+str(lat)+","+str(lon)+"] from " +cc + ": " + usr)
'''