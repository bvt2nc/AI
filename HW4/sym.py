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

def save_info_sym(state, info):
	if state["last-outcome"] is not None:
		info.setdefault(state["opponent-name"],[]).append(state["last-opponent-play"])
		save_info(info)

def opponent_has_pattern(state, info):
	opponent_name = state['opponent-name']
	if opponent_name in info:
		opponent_moves = info[opponent_name]
		pattern_length = randint(3,4) #how long is long enough to be considered a pattern? use randint to avoid predictable strategy 
		if len(opponent_moves) > pattern_length:
			pattern = [opponent_moves[len(opponent_moves) - 1 - i] for i in range(pattern_length)]
			pattern.append(state['last-opponent-play'])
			# print('patt array =-', pattern)
			if all(pattern[0] == move for move in pattern):
				return opponent_moves[0] #return move that was repeated
		return -1 #-1 if no pattern
	return -2 #-2 if player has not been played enough

def get_move_sym(state, info):
	pattern = opponent_has_pattern(state, info)
	# print('pattern --- ', pattern)

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
	
	#if there is a pattern and the opponent does not do too much better than us, choose the higher payout according to the pattern
	if pattern == 0 or pattern == 1:
		# print('pattern is', pattern)
		# print('prospects')
		# print(prospects[0])
		# print(prospects[1])
		zero_move = prospects[0][pattern]
		one_move = prospects[1][pattern]
		# print('zero-move', zero_move)
		if zero_move > one_move and one_move * 1.8 <= zero_move:
			return 0
		elif zero_move < one_move and zero_move * 1.8 <= one_move:
			return 1

	y = (d - b) / ((a - c) + (d - b))
	x = 1 - y

	EU = [0, 0]
	EU[0] = (a * x) + (b * y)
	EU[1] = (c * x) + (d * y)

	# print("x: %s" % (x))
	# print("y: %s" % (y))
	# print("EU[0]: %s" % (EU[0]))
	# print("EU[1]: %s" % (EU[1]))

	if EU[0] > EU[1]:
		return 0
	else:
		return 1

def get_move(state):
	info = load_info()
	move = get_move_sym(state, info)
	save_info_sym(state, info)
	# print(state,info)
	return {
		'team-code': state['team-code'],
		'move': move
	}

def main():
	# for i in range(5):
	# 	opponent_move = randint(0,1)
	# 	opponent_move = 0
	# 	state = {
	# 		"team-code": "eef8976e",
	# 		"game": "sym",
	# 		"opponent-name": "mighty-ducks",
	# 		"prev-repetitions": 10, #Might be None if first game ever, or other number
	# 		"last-opponent-play": opponent_move, #0 or 1 depending on strategy played
	# 		"last-outcome": 4, #Might be None if first game, or whatever outcome of play is
	# 		"prospects": [

	# 		# [7000,0],
	# 		# [1001,1]

	# 		# [1000,0],
	# 		# [1001,1]

	# 		[10,99],
	# 		[100,0] 

	# 		]
	# 	}
	# 	print(get_move(state))
	# 	print()


if __name__ == '__main__':
	main()