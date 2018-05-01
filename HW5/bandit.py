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

def load_info():
	f_name = TEAM_NAME + ".json"
	try:
		return json.loads(open(f_name).read())
	except:
		return {}

def save_info(info):
	f_name = TEAM_NAME + ".json"
	f = open(f_name,"w")
	f.write(json.dumps(info))
	f.flush()
	f.close()

def main():
	simulate()

def get_move(state):
	info = load_info()
	return get_move_bandit(state, info)
	#save_info_bandit(state, info)
	# print(state,info)


def phase_2_a(state, info):
	top15 = info['bestslots']
	auctions = []
	for x, y in top15[-10:]:
		auctions.append(x)
	return {
		"team-code": state['team-code'],
		"game": "phase_2_a",
		"auctions": auctions
	}

def get_expected_value(top15, auction_number):
	for number, value in top15:
		if number == auction_number:
			return value
	return 0

def in_top15(top15, auction_number):
	for number, value in top15:
		if number == auction_number:
			return True
	return False

def phase_2_b(state, info):
	top15 = info['bestslots']
	bid = 0
	if in_top15(top15, state['auction-number']):
		expected_value = get_expected_value(top15, state['auction-number'])
		bid = expected_value // 3 + 1

	return {
		"team-code": state['team-code'],
		"game": "phase_2_b",
		"bid": bid
	}


def get_move_bandit(state, info):
	if state["game"] == "phase_1":

		slot = 0

		if "pull-to-gain" in info:
			if info["pull-to-gain"] is not None:
				slot = info["pull-to-gain"]
			else:
				lastpull = info["last-pull"]
				slot = lastpull
				#print(lastpull)
				if str(lastpull) in info:
					data = info[str(lastpull)]
					data.append(state["last-payoff"] - state["last-cost"])
					if len(data) >= 30:
						#print("next")
						slot = slot + 1
						info[str(slot)] = []
						if slot >= 100:
							info["pull-to-gain"] = bestSlot(info)
							slot = info["pull-to-gain"]
					else:
						info[str(slot)] = data
				else:
					info[str(lastpull)] = [state["last-payoff"]]
		else:
			info["pull-to-gain"] = None
			info["last-pull"] = 0
			slot = 0

		info["last-pull"] = slot
		save_info(info)
		return {
			"team-code": state["team-code"],
			"game": state["game"],
			"pull": slot,
		}

	elif state["game"] == "phase_2_a":
		# auctions = []
		# return {
		# 	"team-code": state["team-code"],
		# 	"game": state["game"],
		# 	"auctions": auctions
		# }
		return phase_2_a(state, info)

	elif state["game"] == "phase_2_b":
		# bid = 0
		# return {
		# 	"team-code": state["team-code"],
		# 	"game": state["game"],
		# 	"bid" : bid
		# }
		return phase_2_b(state, info)

def bestSlot(info):
	bestslots = []
	for i in range(100):
		total = 0
		for el in info[str(i)]:
			total = total + el
		
		total = total / 30
		if len(bestslots) < 15:
			bestslots.append((i, total))
			bestslots = sorted(bestslots, key=lambda tup: tup[1])
		else:
			if bestslots[0][1] < total:
				bestslots[0] = (i, total)
				bestslots = sorted(bestslots, key=lambda tup: tup[1])
	info["bestslots"] = bestslots
	save_info(info)

	return bestslots[14][0]

def phase1(slots):
	ret = None
	lastcost = None
	payoff = None
	credits = 1000000
	for i in range(10000):
		#print("Round: " + str(i))
		if ret is None:
			lastcost = None
			payoff = None
		else:
			alpha = slots[ret["pull"]][0]
			beta = slots[ret["pull"]][1]
			scale = slots[ret["pull"]][2]
			lastcost = slots[ret["pull"]][3]
			credits = credits - lastcost
			payoff = np.random.beta(a=alpha, b=beta) * scale

		state = {
			"team-code": "aaaaaa",
			"game": "phase_1",
			"pulls-left": 10000 - i - 1,
			"last-cost": lastcost,
			"last-payoff": payoff,
			"last-metadata": 00000000,
		}

		ret = get_move(state)

	return credits

def phase2(slots):

	net = 0

	state = {
		"team-code": "aaaaaa",
		"game": "phase_2_a",
	}

	print(get_move(state))

	auctions = get_move(state)["auctions"]
	print("auctions: " + str(auctions))

	for machine in auctions:
		state = {
			"team-code": "aaaaaa",
			"game": "phase_2_b",
			"auction-number": machine,
			"your-slots": [],
			"auction-lists": [],
		}
		bid = get_move(state)["bid"]

		alpha = slots[machine][0]
		beta = slots[machine][1]
		scale = slots[machine][2]
		cost = slots[machine][3]

		machineNet = 0	
		#assume you win each bid
		for i in range (10000):
			payoff = np.random.beta(a=alpha, b=beta) * scale
			machineNet = machineNet + payoff - cost

		net = net + machineNet - bid
		print("===========================================SLOT %s============================================" % (machine))
		print("Bid: %s \t AverageNet: %s \t BetaMean: %s" % (bid, machineNet / 10000, betaMean(alpha, beta, scale)))
		print("alpha: %s \t beta: %s \t scale: %s \t cost: %s" %(alpha, beta, scale, cost))

	return net

def simulate():
	slots = []
	for i in range(100):
		alpha = randint(1, 5)
		beta = randint(1, 5)
		scale = randint(2, 10)
		cost = 3 #randint(2, 10)
		slots.append((alpha, beta, scale, cost))

	credits = phase1(slots)
	
	phase1Net = 1000000 - credits
	print("Phase 1 Net: %s" % (phase1Net))

	info = load_info()
	print(info["bestslots"])

	expectedPhase2Net = 0
	for machine, profit in info["bestslots"][-10:]:
		expectedPhase2Net = expectedPhase2Net + (profit * 10000)
	print("Expected Phase 2 Net: " + str(expectedPhase2Net))

	phase2Net = phase2(slots)
	print("Phase 2 Net: %s" % (phase2Net))
	print("Total Net: %s" %(phase1Net + phase2Net))

	print(slots[24])

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

def test():
	alpha = randint(1, 5)
	beta = randint(1, 5)
	scale = randint(1, 50)
	size = 30
	data = generateData(alpha, beta, scale, size)
	mean = np.mean(data) #/ scale
	x = 10
	cdf = ecdf(data, x)
	mode = getMode(data)
	var = variance(data, mean) #/ (scale ** 2)
	empA, empB = getParams(mean, var)

	print("alpha: %s" % (alpha))
	print("beta: %s" % (beta))
	print("scale: %s" % (scale))
	print("max: %s" % (max(data)))
	print("mean: %s" % (mean)) #empirical average
	print("E[x]: %s" % (betaMean(alpha, beta, scale))) #theoretical average
	print("Error: %s" % (abs(mean - betaMean(alpha, beta, scale)) / betaMean(alpha, beta, scale) * 100))
	print("Var[x]: %s" % (var)) #empirical variance
	print("alpha: %s" % (empA))
	print("beta: %s" % (empB))
	#print("mode: %s" % (mode))
	#print("betaMode: " + str(betaMode(alpha, beta, scale)))
	print("cdf[%s]: %s" % (x, cdf))

if __name__=='__main__':
	main()