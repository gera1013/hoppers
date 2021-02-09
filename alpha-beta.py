import copy
import math
import random
import numpy as np
from board import print_board
from hoppers import Node, check_horizontal, check_vertical, check_diagonal

evals = [number for number in range(1, 102)]

class Game(object):
    def __init__(self, b):
        self.board = b
        self.player = 1
        self.max_depth = 4

    def alpha_beta_pruning(self):
        player = self.player
        self.max_depth = 2 if self.missing(self.board) <= 2 else 4

        value, mov, depth = self.max_value(self.board, float('-inf'), float('inf'), 1)
        print(value, mov, depth)

        return mov

    def max_value(self, board, a, b, d, action = None):
        alpha = a
        beta = b

        if self.is_cutoff(board, d, 2, action):
            return self.utility(board, 2, action), None, d

        v = float('-inf')
        move = (-1, -1)
        depth = 10

        for action in self.get_actions(board, 1):
            v_2, a_2, d_2 = self.min_value(self.ply(board, action, 1), alpha, beta, d+1, action)
            
            if v_2 > v:
                v = v_2
                move = action
                alpha = max(alpha, v)
                depth = d_2

            if v_2 == v:
                if d_2 < depth:
                    v = v_2
                    move = action
                    beta = min(beta, v)

            if v >= beta:
                return v, move, depth
        
        return v, move, depth

    def min_value(self, board, a, b, d, action = None):
        alpha = a
        beta = b

        if self.is_cutoff(board, d, 1, action):
            return self.utility(board, 1, action), None, d

        v = float('inf')
        move = (-1, -1)
        depth = 10

        for action in self.get_actions(board, 2):
            v_2, a_2, d_2 = self.max_value(self.ply(board, action, 2), alpha, beta, d+1, action)
            
            if v_2 < v:
                v = v_2
                move = action
                beta = min(beta, v)
                depth = d_2

            if v_2 == v:
                if d_2 < depth:
                    v = v_2
                    move = action
                    beta = min(beta, v)
            
            if v <= alpha:
                return v, move, depth
        
        return v, move, depth

    def ply(self, b, a, p):
        new_board = copy.deepcopy(b)
        new_board[a[0][0]][a[0][1]] = 0
        new_board[a[1][0]][a[1][1]] = p

        return new_board

    def is_cutoff(self, board, depth, player, action):
        if self.is_terminal(board, player):
            return True

        return True if depth % self.max_depth == 0 else False

    def utility(self, board, player, action):
        if self.is_terminal(board, player):
            return 0 if player == 2 else 1

        if self.missing(board) <= 2:
            suma = 60
            corner = [
                (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                (1, 0), (1, 1), (1, 2), (1, 3), (2, 0),
                (2, 1), (2, 2), (3, 0), (3, 1), (4, 0),
            ]

            if action[0] in corner:
                return 0

            for x in range(10):
                for y in range(10):
                    piece = board[x][y]
                    if (x, y) in corner:
                        if piece == 0:
                            suma = suma - abs(x - action[1][0]) - abs(y - action[1][1])
        
            suma = suma - 2 * (self.missing(board))

            return suma / 61

        suma = 275

        for x in range(10):
            for y in range(10):
                piece = board[x][y]

                if piece == player:
                    suma = suma - x - y

        suma = suma - 2 * self.left(board)

        return (suma / 300)

    def get_actions(self, b, p):
        actions = []

        for x in range(10):
            for y in range(10):
                piece = b[x][y]

                possible = []

                if piece == p:
                    possible += check_diagonal(b, piece, x, y)
                    possible += check_vertical(b, piece, x, y)
                    possible += check_horizontal(b, piece, x, y)

                    possible = set(possible)
                    possible = list(possible)

                    for ply in possible:
                        actions.append(((x, y), ply))
        
        return actions

    def is_terminal(self, board, player):
        if player == 1:
            corner = [
                board[0][0], board[0][1], board[0][2], board[0][3], board[0][4], 
                board[1][0], board[1][1], board[1][2], board[1][3], board[2][0], 
                board[2][1], board[2][2], board[3][0], board[3][1], board[4][0], 
            ]

            if not 0 in corner:
                if not 2 in corner:
                    return True

        if player == 2:
            corner = [
                board[9][9], board[9][8], board[9][7], board[9][6], board[9][5], 
                board[8][9], board[8][8], board[8][7], board[8][6], board[7][9], 
                board[7][8], board[7][7], board[6][9], board[6][8], board[5][9], 
            ]

            if not 0 in corner:
                if not 1 in corner:
                    return True

        return False

    def left(self, board):
        corner = [
            board[9][9], board[9][8], board[9][7], board[9][6], board[9][5], 
            board[8][9], board[8][8], board[8][7], board[8][6], board[7][9], 
            board[7][8], board[7][7], board[6][9], board[6][8], board[5][9], 
        ]

        count = 0
        for x in corner:
            if x == 1:
                count += 1

        return count
    
    def missing(self, board):
        corner = [
            board[0][0], board[0][1], board[0][2], board[0][3], board[0][4], 
            board[1][0], board[1][1], board[1][2], board[1][3], board[2][0], 
            board[2][1], board[2][2], board[3][0], board[3][1], board[4][0], 
        ]

        count = 0
        for x in corner:
            if x != 1:
                count += 1

        return count


# board = [
#     #0 #1 #2 #3 #4 #5 #6 #7 #8 #9
#     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], #0
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0], #1
#     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], #2
#     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], #3
#     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], #4
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], #5
#     [0, 0, 0, 2, 0, 0, 0, 0, 2, 2], #6
#     [0, 0, 0, 2, 0, 0, 0, 2, 2, 2], #7
#     [0, 0, 0, 0, 0, 0, 2, 2, 2, 2], #8
#     [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], #9
# ]

# board = [
#     #0 #1 #2 #3 #4 #5 #6 #7 #8 #9
#     [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], #0
#     [1, 1, 1, 1, 0, 0, 0, 0, 0, 0], #1
#     [0, 1, 1, 0, 0, 0, 0, 0, 0, 0], #2
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #3
#     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0], #4
#     [0, 0, 0, 2, 0, 0, 0, 0, 2, 0], #5
#     [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], #6
#     [0, 0, 0, 1, 0, 0, 2, 0, 2, 2], #7
#     [0, 0, 0, 0, 0, 2, 2, 0, 2, 2], #8
#     [0, 0, 0, 0, 0, 0, 2, 0, 2, 2], #9
# ]

board = [
    #0 #1 #2 #3 #4 #5 #6 #7 #8 #9
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], #0
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0], #1
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], #2
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #3
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 2], #5
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 2], #6
    [0, 0, 0, 1, 0, 0, 0, 2, 2, 2], #7
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2], #8
    [0, 0, 0, 0, 0, 0, 2, 0, 2, 2], #9
]

# board = [
#     #0 #1 #2 #3 #4 #5 #6 #7 #8 #9
#     [2, 2, 2, 2, 2, 0, 0, 0, 0, 0], #0
#     [2, 2, 2, 2, 0, 0, 0, 0, 0, 0], #1
#     [2, 2, 2, 0, 0, 0, 0, 0, 0, 0], #2
#     [2, 2, 0, 0, 0, 0, 0, 0, 0, 0], #3
#     [2, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #5
#     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1], #6
#     [0, 0, 0, 0, 0, 0, 0, 1, 1, 1], #7
#     [0, 0, 0, 0, 0, 0, 1, 1, 1, 1], #8
#     [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], #9
# ]

test_game = Game(board)

print("START")
print_board(board)

while True:
    print("\nCalculating...")
    pick = test_game.alpha_beta_pruning()

    board[pick[0][0]][pick[0][1]] = 0
    board[pick[1][0]][pick[1][1]] = 1

    print("\nMOVE MINIMAX", "(", pick[0][0] + 1, ",", pick[0][1] + 1, ")", ", (", pick[1][0] + 1, ",", pick[1][1] + 1, ")\n")
    print_board(board)

    if test_game.is_terminal(board, 1):
        print("MINIMAX WINS!!")
        break

    xi = int(input("INGRESE X INIT: "))
    yi = int(input("INGRESE Y INIT: "))
    xf = int(input("INGRESE X FINAL: "))
    yf = int(input("INGRESE Y FINAL: "))

    board[xi - 1][yi - 1] = 0
    board[xf - 1][yf - 1] = 2

    print("\nMOVE PLAYER", "(", xi, ",", yi, ")", ", (", xf, ",", yf, ")\n")
    print_board(board)
    if test_game.is_terminal(board, 1):
        print("PLAYER WINS!!")
        break