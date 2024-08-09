"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)

    if x_count == o_count:
        return 'X'
    else:
        return 'O'
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == None:
                possible_actions.add((i,j))

    return possible_actions
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if i < 0 or i > 2 or j < 0 or j > 2:
        raise IndexError("Invalid action: Fuera de lugar")
    
    if board[i][j] is not None:
        raise ValueError("Invalid action: La celda esta ocupada")
    
    new_board = [row.copy() for row in board] # Hacemos un nuevo board

    player_to_play = player(board) # Devuelve el jugador que va a jugar

    new_board[i][j] = player_to_play

    return new_board
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    resultado = None

    #Comprobamos por columnas

    for j in range(len(board[0])):
        if board[0][j] == board[1][j] == board[2][j] != None and resultado == None:
            if board[0][j] == X:
                resultado = X
            else:
                resultado = O
            # print(board[0][j], board[1][j], board[2][j])

    #Si todavia sigue siendo falso seguimos comprobando ahora por filas

    if resultado == None:
        for i in range(len(board)):
            if board[i][0] == board[i][1] == board[i][2] != None and resultado == None:
                if board[i][0] == X:
                    resultado = X
                else:
                    resultado = O
                # print(board[i][0], board[i][1], board[i][2])

    #Si todavia sigue siendo falso seguimos comprobando ahora por diagonales

    if board[0][0] == board[1][1] == board[2][2] != None and resultado == None:
        if board[0][0] == X:
            resultado = X
        else:
            resultado = O
    if board[0][2] == board[1][1] == board[2][0] != None and resultado == None:
        if board[0][2] == X:
            resultado = X
        else:
            resultado = O
            
    return resultado 

    #raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) == X or winner(board) == O:
        return True
    
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    if x_count + o_count == 9:
        return True

    return False
    #raise NotImplementedError


def utility(board):
    """
    Returns One if X has won the game, Minus One if O has won, Cero otherwise.
    """

    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    elif player(board) == X:
        plays = []
        for action in actions(board):
            x = [min_value(result(board,action)),action]
            plays.append(x)
            print(x)
        print("-----------")
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]
    
    elif player(board) == O:
            plays = []
            for action in actions(board):
                x = [max_value(result(board,action)),action]
                plays.append(x)
                print(x)
            print("-----------")
            return sorted(plays, key=lambda x: x[0])[0][1]

def max_value(state):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, min_value(result(state, action)))
    return v


def min_value(state):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, max_value(result(state, action)))
    return v