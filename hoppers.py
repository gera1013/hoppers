import copy
import numpy as np
from board import print_board

board = [
    #0 #1 #2 #3 #4 #5 #6 #7 #8 #9
    [2, 2, 2, 2, 2, 0, 0, 0, 0, 0], #0
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0], #1
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0], #2
    [2, 2, 0, 0, 0, 0, 0, 0, 0, 0], #3
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #5
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1], #6
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1], #7
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1], #8
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], #9
]

class Node(object):
    def __init__(self, b, l, p, sp, fp):
        self.board_status = b
        self.level = l
        self.parent = p
        self.s_position = sp
        self.f_position = fp
        self.eval_value = 0
        self.terminal = False

states = []

def check_possible_moves(board, moves, parent):
    print_board(parent.board_status)
    print(parent.level, parent.s_position, parent.f_position)
    for x in range(10):
        for y in range(10):
            piece = board[x][y]

            possible = []

            if piece == moves:
                possible += check_vertical(board, piece, x, y)
                possible += check_horizontal(board, piece, x, y)
                possible += check_diagonal(board, piece, x, y)

                possible = set(possible)
                possible = list(possible)

                print(x, y, " -> ", possible)

            for move in possible:
                new_board = copy.deepcopy(board)
                new_board[x][y] = 0
                new_board[move[0]][move[1]] = moves
                
                states.append(Node(new_board, parent.level + 1, parent, (x, y), (move[0], move[1])))

def check_vertical(board, piece, x, y, checked = [], hop = False):
    v = []

    if x > 0:
        if(board[x - 1][y] == 0):
            if hop:
                return v

            v.append((x - 1, y))
        else:
            if x > 1:
                if(board[x - 2][y] == 0):
                    if ((x - 2, y) in checked):
                        return v
                    
                    v.append((x - 2, y))
                    v += check_vertical(board, piece, x - 2, y, checked=checked + v, hop=True)
                    v += check_horizontal(board, piece, x - 2, y, checked=checked + v, hop=True)
                    v += check_diagonal(board, piece, x - 2, y, checked=checked + v, hop=True)

    if x < 9:
        if(board[x + 1][y] == 0):
            if hop:
                return v
            
            v.append((x + 1, y))
        else:
            if x < 8:
                if(board[x + 2][y] == 0):
                    if ((x + 2, y) in checked):
                        return v
                    
                    v.append((x + 2, y))
                    v += check_vertical(board, piece, x + 2, y, checked=checked + v, hop=True)
                    v += check_horizontal(board, piece, x + 2, y, checked=checked + v, hop=True)
                    v += check_diagonal(board, piece, x + 2, y, checked=checked + v, hop=True)

    return v

def check_horizontal(board, piece, x, y, checked = [], hop = False):
    h = []

    if y > 0:
        if(board[x][y - 1] == 0):
            if hop:
                return []
            
            h.append((x, y - 1))
        else:
            if y > 1:
                if(board[x][y - 2] == 0):
                    if ((x, y - 2) in checked):
                        return h
                    
                    h.append((x, y - 2))
                    h += check_horizontal(board, piece, x, y - 2, checked=checked + h, hop=True)
                    h += check_vertical(board, piece, x, y - 2, checked=checked + h, hop=True)
                    h += check_diagonal(board, piece, x, y - 2, checked=checked + h, hop=True)

    if y < 9:
        if(board[x][y + 1] == 0):
            if hop:
                return []

            h.append((x, y + 1))
        else:
            if y < 8:
                if(board[x][y + 2] == 0):
                    if ((x, y + 2) in checked):
                        return h

                    h.append((x, y + 2))
                    h += check_horizontal(board, piece, x, y + 2, checked=checked + h, hop=True)
                    h += check_vertical(board, piece, x, y + 2, checked=checked + h, hop=True)
                    h += check_diagonal(board, piece, x, y + 2, checked=checked + h, hop=True)

    return h

def check_diagonal(board, piece, x, y, checked = [], hop=False):
    d = []

    if x > 0:
        if y > 0:
            if(board[x - 1][y - 1] == 0):
                if hop:
                    return d

                d.append((x - 1, y - 1))
                
            else:
                if x > 1:
                    if y > 1:
                        if(board[x - 2][y - 2] == 0):
                            if((x - 2, y - 2) in checked):
                                return d
                            
                            d.append((x - 2, y - 2))
                            d += check_horizontal(board, piece, x - 2, y - 2, checked=checked + d, hop=True)
                            d += check_vertical(board, piece, x - 2, y - 2, checked=checked + d, hop=True)
                            d += check_diagonal(board, piece, x - 2, y - 2, checked=checked + d, hop=True)
        
        if y < 9:
            if(board[x - 1][y + 1] == 0):
                if hop:
                    return d
                
                d.append((x - 1, y + 1))
            else:
                if x > 1:
                    if y < 8:
                        if(board[x - 2][y + 2] == 0):
                            if((x - 2, y + 2) in checked):
                                return d

                            d.append((x - 2, y + 2))
                            d += check_horizontal(board, piece, x - 2, y + 2, checked=checked + d, hop=True)
                            d += check_vertical(board, piece, x - 2, y + 2, checked=checked + d, hop=True)
                            d += check_diagonal(board, piece, x - 2, y + 2, checked=checked + d, hop=True)
    
    if x < 9:
        if y > 0:
            if(board[x + 1][y - 1] == 0):
                if hop:
                    return d

                d.append((x + 1, y - 1))
            else:
                if x < 8:
                    if y > 1:
                        if(board[x + 2][y - 2] == 0):
                            if((x + 2, y - 2) in checked):
                                return d

                            d.append((x + 2, y - 2))
                            d += check_horizontal(board, piece, x + 2, y - 2, checked=checked + d, hop=True)
                            d += check_vertical(board, piece, x + 2, y - 2, checked=checked + d, hop=True)
                            d += check_diagonal(board, piece, x + 2, y - 2, checked=checked + d, hop=True)
        
        if y < 9:
            if(board[x + 1][y + 1] == 0):
                if hop:
                    return d

                d.append((x + 1, y + 1))
            else:
                if x < 8:
                    if y < 8:
                        if(board[x + 2][y + 2] == 0):
                            if((x + 2, y + 2) in checked):
                                return d

                            d.append((x + 2, y + 2))
                            d += check_horizontal(board, piece, x + 2, y + 2, checked=checked + d, hop=True)
                            d += check_vertical(board, piece, x + 2, y + 2, checked=checked + d, hop=True)
                            d += check_diagonal(board, piece, x + 2, y + 2, checked=checked + d, hop=True)
    
    return d

# root_board = copy.deepcopy(board)
# root_node = Node(root_board, 1, None, None, None)

# check_possible_moves(board, 1, root_node)

# for node in states:
#     states.remove(node)
#     check_possible_moves(node.board_status, ((node.level + 1) % 2) + 1, node)