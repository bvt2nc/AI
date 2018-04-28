"""
Authors:
    Ben Trans (bvt2nc)
    Oliver Shi (oys4cv)
"""

from random import *
from math import *
from copy import deepcopy
from time import time
import json
import numpy as np

TEAM_NAME = "idk"
MEMBERS = ["bvt2nc", 'oys4cv']

def main():
	alpha = randint(1, 5)
	beta = randint(1, 5)
	scale = randint(1, 50)
	size = 100
	data = generateData(alpha, beta, scale, size)
	mean = np.mean(data) # / scale
	x = 10
	cdf = ecdf(data, x)
	mode = getMode(data)
	var = variance(data, mean) # / (scale ** 2)
	empA, empB = getParams(mean, var)

	print("alpha: %s" % (alpha))
	print("beta: %s" % (beta))
	print("scale: %s" % (scale))
	print("max: %s" % (max(data)))
	print("mean: %s" % (mean)) #empirical average
	print("E[x]: %s" % (betaMean(alpha, beta, scale))) #theoretical average
	print("Var[x]: %s" % (var)) #empirical variance
	print("alpha: %s" % (empA))
	print("beta: %s" % (empB))
	#print("mode: %s" % (mode))
	#print("betaMode: " + str(betaMode(alpha, beta, scale)))
	print("cdf[%s]: %s" % (x, cdf))

def generateData(alpha, beta, scale, size):
	ret = []
	np.random.seed(1)

	for i in range(size):
		ret.append(np.random.beta(a=alpha, b=beta) * scale)

	return ret

def ecdf(data, x):
	total = 0
	for el in data:
		if el <= x:
			total = total + 1

	return (total / len(data))

def getMode(data):
	return max(set(data), key=data.count)

def variance(data, mean):
	total = 0
	for el in data:
		total = total + ((el - mean) ** 2)
	return total / len(data)

def betaMode(a, b, scale):
	if a == 1 and b == 1:
		return -1
	if(a == 1 and b > 1):
		return 0
	if(a > 1 and b == 1):
		return 1
	return ((a - 1) / (a + b - 2)) * scale

def betaMean(a, b, scale):
	return (a / (a + b)) * scale

"""
Due to scaling factor, the will not produce accurate alph and beta
values unless scale = 1
"""
def getParams(mean, var):
	alpha = (((1 - mean) / var) - (1 / mean)) * mean * mean
	beta = alpha * ((1 / mean) - 1)
	return round(alpha), round(beta)




if __name__=='__main__':
	main()