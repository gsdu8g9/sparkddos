#
#   Trainer class - outputs a Gaussian Mixture Model.
#	For k in range (a, b) it assigns a performance score e, and picks the best model.
#   AXJ 2016
#

from pyspark.mllib.clustering import GaussianMixture
from pyspark import SparkContext
from scipy.stats import mvn
# from mpl_toolkits.mplot3d import Axes3D
import numpy as np
# import matplotlib.pyplot as plt
import time
import shutil
import os


DIR = "/home/adrianj/Desktop/MachineLearning/Resources/"
TRAIN_PATH = DIR+"newTrainingSet.txt"
TEST_PATH = DIR+"newTestSet.txt"
NUM_GAUSSIANS = 80


sc = SparkContext(appName="GMM Trainer")
data = sc.textFile(TRAIN_PATH)
parsedData = data.map(lambda line: np.array([float(x) for x in line.strip().split(' ')]))
testData = sc.textFile(TEST_PATH)
parsedTestData = testData.map(lambda line: np.array([float(x) for x in line.strip().split(' ')]))

scores = []

#fig = plt.figure()
#ax = fig.gca(projection='3d')

def plotFigure(mu, sigma):
	#a, b = np.random.multivariate_normal(mu, sigma, 5000).T
	#surf = ax.scatter(a, b, c, zdir='z')
	#plt.plot(a, b, "x")
	'''plt.axis("equal")
	plt.xlabel("Latitude")
	plt.ylabel("Longitude")
	plt.title("Composite Gaussian Mixture Model with "+str(NUM_GAUSSIANS) + " Gaussians.")
	plt.show()'''

def removeSuperfluousDirectories(k):
	for i in range(NUM_GAUSSIANS, NUM_GAUSSIANS+420):
		if i != k:
			shutil.rmtree(DIR+"GMM"+str(i)+"/")


def testGaussian(gmm):
	error = gmm.predictSoft(testData)
	return error


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


#loop starts here
print("Training... Dumping to "+DIR+"GMMx/...")
	
for i in range(NUM_GAUSSIANS, NUM_GAUSSIANS + 420):
	gmm = GaussianMixture.train(parsedData, i)
	directory = DIR+"GMM"+str(i)+"/"

	if os.path.exists(directory):
		print("Overwriting "+directory+"...")
		shutil.rmtree(directory)
	os.mkdir(directory)

	# Record the model
	gmm.save(sc, directory)

	# Calculate the score
	e = testGaussian(gmm)
	scores.append((e, i))

scores.sort()
k = scores[0][1]
removeSuperfluousDirectories(k)

print("Done. Model selected has "+str(k)+" Gaussians.")