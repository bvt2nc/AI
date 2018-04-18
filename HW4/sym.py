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

def get_move_sym(state):
	prospects = state['prospects']

	a = prospects[0][0]
	b = prospects[0][1]
	c = prospects[1][0]
	d = prospects[1][1]

	#Base cases for if dominant strategy exists
	if a >= c and b >= d:
		return 0
	if c >= a and d >= b:
		return 1
	
	y = (d - b) / ((a - c) + (d - b))
	x = 1 - y

	EU = [0, 0]
	EU[0] = (a * x) + (b * y)
	EU[1] = (c * x) + (d * y)

	print("x: %s" % (x))
	print("y: %s" % (y))
	print("EU[0]: %s" % (EU[0]))
	print("EU[1]: %s" % (EU[1]))

	if EU[0] > EU[1]:
		return 0
	else:
		return 1

def get_move(state):
	move = get_move_sym(state)
	return {
		'team-code': state['team-code'],
		'move': move
	}

def main():
	state = {
		"team-code": "eef8976e",
		"game": "sym",
		"opponent-name": "mighty-ducks",
		"prev-repetitions": 10, #Might be None if first game ever, or other number
		"last-opponent-play": 1, #0 or 1 depending on strategy played
		"last-outcome": 4, #Might be None if first game, or whatever outcome of play is
		"prospects": [
		[10,99],
		[100,0] ]
	}
	print(get_move(state))

if __name__ == '__main__':
	main()