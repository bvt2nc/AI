"""
Authors:
    Ben Trans (bvt2nc)
"""

from random import *
from math import *
from copy import deepcopy
from time import time
TEAM_NAME = "idk"
MEMBERS = ["bvt2nc"]
MAX_DEPTH = 2 #Found to have worked best... will win by timeout or outright win if other player isn't as smart
token = ""
oppToken = ""
nCol = None
nRow = None

# this is a test state function for you to drive the following test case with
# NOTE: you will receive this when the game playing program calls your get_move
"""state = {
    "game":	"chicken",
    "opponent-name": "the_baddies",
    "team-code": "abc123",
    "prev-response-time": 0.5,
    "last-opponent-play": 0.71,
    "last-outcome": -10,
}
"""

# This will load whatever dictionary you last saved, stub included to drive example,
#   isn't actual function
def load_info():
    return {}

# This will save (and overwrite) whatever dictionary you last saved
# Stub included to drive example, isn't actual function
def save_info(info):
    print(info)

# returns a random move (for sake of example)
def get_chicken_move(state):
    info = load_info() # info might be "{}" if first use, otherwise reads dictionary from your save file
    # example for storing previous response times
    if state["prev-response-time"] is not None:
        info.setdefault("opponents",{}).setdefault(state["opponent-name"],[]).append(state["prev-response-time"])
    save_info(info)
    return {
        "move": random.randint(0,10) * random.random(),
        "team-code": state["team-code"],
    }

def get_move(state):
    if state["game"] == "chicken":
        return get_chicken_move(state)
    if state["game"] == "connect_more":
        return get_connect_move(state)

def get_connect_move(state):
    moves = {}
    board = makeBoardUniform(state["board"])
    #board = state["board"]
    #print_board(board)

    #set HEIGHT and WIDTH
    global nCol
    global nRow
    nCol = len(board)
    nRow = len(board[0])

    #set your token and opponent's token
    global token
    global oppToken
    token = state["your-token"]
    for c in range(nCol):
        for r in range(nRow):
            if board[c][r] != token and board[c][r] != " " and board[c][r] != "" and board[c][r] != None:
                oppToken = board[c][r]
                break
    #opponent's token not found which means we are making the first move
    if oppToken == "":
        #make move in center
        return {
            "move": ceil(nCol / 2),
            "team-code": state["team-code"]
        }

    for c in range(nCol):
        if legal_move(c, board):
            temp = make_fake_move(board, c, token)
            moves[c] = -simulate(temp, 1, oppToken, state["connect_n"])
            #print_board(temp)
            """print(moves[c])
            print(h(temp, 1, 5))
            print(find_streak(temp, 1, 5))"""
            #moves[c] = -h(temp, 0, state["connect_n"])

    #print(moves)

    best_h = -9999999999
    best_move = None
    for c, hVal in moves.items():
        if hVal >= best_h:
            best_h = hVal
            best_move = c

    return {
        "move": best_move, #Column in which you will move (create mark "your-token")
        "team-code": state["team-code"]
    }

def legal_move(c, board):
    return c < nCol

def make_fake_move(board, c, color):
    temp = [x[:] for x in board] #copy board
    for r in range(len(temp[c])):
        if temp[c][r] == ' ':
            temp[c][r] = color
            break
    return temp

def make_move(board, c, color):
    for r in range(len(board[c])):
        if board[c][r] == ' ':
            board[c][r] = color
            break
    return board


def simulate(board, depth, color, streak):
    #print_board(board)
    moves = []
    for c in range(nCol):
        if legal_move(c, board):
            temp = make_fake_move(board, c, color)
            moves.append(temp)

    myToken = 1
    nextColor = oppToken
    if color == oppToken:
        myToken = 0
        nextColor = token

    if depth == MAX_DEPTH or len(moves) == 0 or winner_found(board, streak):
        #print_board(board)
        #print("H: %s" % (h(board, myToken, streak)))
        return h(board, myToken, streak)

    f = -9999999999
    for child in moves:
        f = max(f, -simulate(child, depth + 1, nextColor, streak))
    return f

def winner_found(board, streak):
    if find_streak(board, 1, streak) > 0:
        return True
    if find_streak(board, 0, streak) > 0:
        return True
    return False

def h(board, myToken, streak):
    #print_board(board)
    oppToken = myToken ^ 1
    score = 0

    if find_streak(board, oppToken, streak) > 0:
        #print_board(board)
        #print("Streak: %s \t myToken: %s" % (streak, oppToken))
        return -1000000000

    #better if we have multiple win conditions since we are predicting which forces opponent into unfavorable position
    ai_streak = find_streak(board, myToken, streak) * 1000000000
    #if ai_streak > 0:
        #print(ai_streak)
    for i in range(2, streak):
        myScore = (find_streak(board, myToken, i) * pow(10, i - 1))
        oppScore = (find_streak(board, oppToken, i) * pow(10, i - 1))
        score += myScore
        score -= oppScore
        #print("Streak: %s \t myScore: %s \t oppScore: %s \t myToken: %s" % (i, myScore, oppScore, myToken))

    return score + ai_streak

def find_streak(board, myToken, streak):
    count = 0

    for r in range(nRow):
        for c in range(nCol):
            #only want to compute for color you choose
            if myToken == 1:
                if board[c][r] == token:
                    count += find_vertical_streak(c, r, board, streak)
                    count += find_horizontal_streak(c, r, board, streak)
                    count += find_diaganol_streak(c, r, board, streak)
            else:
                if board[c][r] == oppToken:
                    count += find_vertical_streak(c, r, board, streak)
                    count += find_horizontal_streak(c, r, board, streak)
                    count += find_diaganol_streak(c, r, board, streak)
                    """"if streak == 4:
                        print_board(board)
                        print("C: %s \t R: %s \t MyToken: %s" % (c, r, myToken))
                        print("token: %s \t board[c][r]: %s" % (token, board[c][r]))
                        print("vertical: %s" % (find_vertical_streak(c, r, board, streak)))
                        print("horizontal: %s" % (find_horizontal_streak(c, r, board, streak)))
                        print("vertical: %s" % (find_diaganol_streak(c, r, board, streak)))"""""
    """if myToken == 0:
        print_board(board)
        print("Streak: %s \t myToken: %s \t Count: %s" % (streak, myToken, count))"""
    return count

def find_vertical_streak(c, r, board, streak):
    count = 0

    if r + streak - 1 >= nRow:
        return 0

    for i in range(streak):
        if board[c][r] == board[c][r + i]:
            count += 1
        else:
            break

    if count == streak:
        #print("connectN |")
        return 1
    return 0

def find_horizontal_streak(c, r, board, streak):
    count = 0

    if c + streak - 1 >= nCol:
        return 0

    for i in range(streak):
        if board[c][r] == board[c + i][r]:
            count += 1
        else:
            break

    if count == streak:
        #print("connectN -")
        return 1
    return 0

def find_diaganol_streak(c, r, board, streak):
    numStreaks = 0

    #check y=x diaganol
    count = 0
    if r + streak - 1 < nRow and c + streak - 1 < nCol:
        for i in range(streak):
            if board[c][r] == board[c + i][r + i]:

                count += 1
            else:
                break
    if count == streak:
        #print_board(board)
        #print("connectN /")
        numStreaks += 1

    #check y=-x diaganol
    count = 0
    if r - streak + 1 >= 0 and c + streak - 1 < nCol:
        for i in range(streak):
            if board[c][r] == board[c + i][r - i]:
                count += 1
            else:
                break
    if count == streak:
        #print_board(board)
        #print("connectN \/")
        numStreaks += 1

    return numStreaks

def makeBoardUniform(board):
    height = len(board[0])

    for c in range(len(board)):
        colHeight = len(board[c])
        if colHeight > height:
            height = colHeight

    for c in range(len(board)):
        r = len(board[c])
        while r < height + 5:
            board[c].append(" ")
            r += 1

    return board

def print_board(board):
    s = ""
    line = ""

    for r in range(len(board[0])):
        line = "|"
        for c in range(len(board)):
            line = line + "%s|" % (board[c][r])
        line = line + "\n"
        s = line + s

    print(s)

def main():
    state = {
        "team-code": "eef8976e",
        "game": "connect_more",
        "opponent-name": "mighty_ducks",
        "columns": 6,
        "connect_n": 5,
        "your-token": "R",
        "board": [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]
        #"board": [
        #    ["Y", "R", "Y", "Y", "R"],
        #    ["R", "Y", "Y", "R"],
        #    ["Y", "Y", "R"],
        #    ["Y", "R"],
        #    ["R"],
        #    ["Y"],
        #]
    }
    """player1Time = 30
    player2Time = 30
    state["board"] = makeBoardUniform(state["board"])
    #set HEIGHT and WIDTH
    global nCol
    global nRow
    nCol = len(state["board"])
    nRow = len(state["board"][0])
    flip = 1
    winner = ""
    while not winner_found(state["board"], state["connect_n"]):
        state["your-token"] = "R"
        global MAX_DEPTH
        MAX_DEPTH = 2
        start = time()
        ret = get_move(state)
        end = time()
        player1Time -= (end - start)
        if player1Time <= 0:
            winner = "Player 2 wins by timeout"
            break
        state["board"] = make_move(state["board"], ret["move"], "R")
        if winner_found(state["board"], state["connect_n"]):
            winner = "Player 1 wins!"
            break

        #now player 2
        state["your-token"] = "Y"
        flip = flip ^ 1
        if flip == 1:
            MAX_DEPTH = 4
        else:
            MAX_DEPTH = 2
        MAX_DEPTH = 1
        start = time()
        ret = get_move(state)
        end = time()
        player2Time -= (end - start)
        if player2Time <= 0:
            winner = "Player 1 wins by timeout"
            break
        state["board"] = make_move(state["board"], ret["move"], "Y")
        if winner_found(state["board"], state["connect_n"]):
            winner = "Player 2 wins!"
            break

    print_board(state["board"])

    print(winner)
    print("Player 1 Time Remaining: %s" % (player1Time))
    print("Player 2 Time Remaining: %s" % (player2Time))"""

if __name__ == '__main__':
    main()