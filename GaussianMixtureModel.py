from pyspark.mllib.clustering import GaussianMixture
from pyspark import SparkContext
from scipy.stats import mvn
import numpy as np
import matplotlib.pyplot as plt

FILE_PATH = "/home/adrianj/Desktop/MachineLearning/trainingSet.txt"
NUM_GAUSSIANS = 115

sc = SparkContext(appName="perceptron")
data = sc.textFile(FILE_PATH)
parsedData = data.map(lambda line: np.array([float(x) for x in line.strip().split(' ')]))
gmm = GaussianMixture.train(parsedData, NUM_GAUSSIANS)

x, y = -1, -1
for i in range(NUM_GAUSSIANS):
	
	mu = gmm.gaussians[i].mu
	sigma = (gmm.gaussians[i].sigma).toArray()
	weight = gmm.weights[i]
	print("weight = ", weight, "mu = ", mu, "sigma = ", sigma)
	print("xxxxxxxx")

	a, b = np.random.multivariate_normal(mu, sigma, 5000).T
	plt.plot(a, b, "x")
	plt.axis("equal")
	x += weight*a
	y += weight*b

plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.title("Gaussian Mixture Model with "+str(NUM_GAUSSIANS) + " Gaussians.")
plt.show()

plt.plot(x, y, "x")
plt.axis("equal")
#plt.show()
