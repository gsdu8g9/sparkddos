#
#   Trainer class - outputs a Gaussian Mixture Model.
#   AXJ 2016
#

from pyspark.mllib.clustering import GaussianMixture
from pyspark import SparkContext
from scipy.stats import mvn
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

DIR = "/home/adrianj/Desktop/MachineLearning/Resources/"
FILE_PATH = DIR+"atemporalTest.txt"
NUM_GAUSSIANS = 500

sc = SparkContext(appName="GMM Trainer")
data = sc.textFile(FILE_PATH)
parsedData = data.map(lambda line: np.array([float(x) for x in line.strip().split(' ')]))
gmm = GaussianMixture.train(parsedData, NUM_GAUSSIANS, seed=10)

print("Dumping to "+DIR+"GMMA/...")
#fig = plt.figure()
#ax = fig.gca(projection='3d')
# Record the model
gmm.save(sc, DIR+"GMMA/")
'''
for i in range(NUM_GAUSSIANS):
	
	mu = gmm.gaussians[i].mu
	sigma = (gmm.gaussians[i].sigma).toArray()
	weight = gmm.weights[i]
	#a, b = np.random.multivariate_normal(mu, sigma, 5000).T
	#surf = ax.scatter(a, b, c, zdir='z')
	#plt.plot(a, b, "x")
'''

print("Done.")
'''plt.axis("equal")
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.title("Composite Gaussian Mixture Model with "+str(NUM_GAUSSIANS) + " Gaussians.")
plt.show()'''