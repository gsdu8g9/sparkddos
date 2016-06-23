#
#   From the provided Gaussian Mixture Model, use a neural net to determine attacks.
#   AXJ 2016
#
from pyspark.mllib.clustering import GaussianMixture
from pyspark import SparkContext
from scipy.stats import multivariate_normal
from scipy.stats import logistic
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math

DIR="/home/adrianj/Desktop/MachineLearning/Resources/"
TITLE="GaussianMixtureModel"

sc = SparkContext(appName=TITLE)
gmm = pickle.load(open(DIR+"Model.sav", 'rb'))
weights = pickle.load(open(DIR+"Weights.sav", 'rb'))
numberOfGaussians = 0
gaussians = []

for i in gmm:
	var = multivariate_normal(mean = i.mu, cov = (i.sigma).toArray())
	gaussians.append((var, weights[numberOfGaussians]))
	numberOfGaussians += 1
	
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


if __name__ == "__main__":

	#sigmoid = logistic.cdf(x)

	file = open(DIR+"testSet.txt", 'rb')
	x = []
	for line in file:
		x.append(map(float, line.rstrip('\n').split(' ')))

	for i in x:
		judgment = 0
		for g in gaussians:
			var, w = g
			judgment += w*logistic.cdf(var.pdf(i))

		if judgment < 0.5:
			lat, lon = inverseCantor(x[0])
			url = decodeString(x[3])
			cc = decodeString(x[2])
			print("Anomaly detected at ["+str(lat)+","+str(lon)+"] from "+cc+" to "+url)