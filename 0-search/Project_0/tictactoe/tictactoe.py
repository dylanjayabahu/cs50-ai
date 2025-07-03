"""
Tic Tac Toe Player
"""

import math
import copy

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

    # if diff b/w xs and os == 0, it's x turn
    # else, its o turn

    # that is, if total xs and os is even, it's x turn
    # else, its o turn

    count = 0
    for row in board:
        for cell in row:
            count += 1 if cell is not None else 0 

    return [X, O][count%2]


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                result.add((i, j))

    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    moves = actions(board)
    if action not in moves:
        raise Exception

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for row in board:
        if all([cell==X for cell in row]):
            return X
        if all([cell==O for cell in row]):
            return O
        

    r = range(3)
    
    # check cols
    for j in range(3):
        if all([board[i][j]==X for i in r]):
            return X
        if all([board[i][j]==O for i in r]):
            return O
    
    # check diagonals
    if all([board[i][i]==X for i in r]) or all([board[i][2-i]==X for i in r]):
        return X
    if all([board[i][i]==O for i in r]) or all([board[i][2-i]==O for i in r]):
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    return all([all(board[i]) for i in range(3)])


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    
    # board is assumed to be terminal
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    return max_val(board)[1] if player(board) == X else min_val(board)[1]



# Alpha: the best value that the maximizing player can guarantee so far.
# Beta: the best value that the minimizing player can guarantee so far.

def min_val(board, alpha=float("-inf"), beta=float("inf")):
    if terminal(board):
        return utility(board), None

    moves = actions(board)
    min_value = float('inf')
    min_move = None

    for move in moves:
        child_value, _ = max_val(result(board, move), alpha=alpha, beta=beta)

        if child_value < min_value:
            min_move, min_value = move, child_value

        #update the best value min player can achieve
        beta = min(min_value, beta)

        #if the best value minplayer can achieve is less than the best value max player can achieve, we can break
        # (i.e. this node is less than or equal to beta. So if alpha is bigger than beta we aren't gonna bother seraching further, 
        #  since it will only every result in something smaller
        if beta <= alpha:
            break
    
    return min_value, min_move
        

def max_val(board, alpha=float("-inf"), beta=float("inf")):
    if terminal(board):
        return utility(board), None
    
    moves = actions(board)
    max_value = float('-inf')
    max_move = None

    for move in moves:
        child_value, _ = min_val(result(board, move), alpha=alpha, beta=beta)

        if child_value > max_value:
            max_move, max_value = move, child_value

        ##update the best value max_player can achieve
        alpha = max(child_value, alpha)

        ##if at any point the best value maxplayer can achieve is greater than (or equal to) the best value minplayer can achieve, we can break
        # i.e., this node is guaranteed to be at least alpha, since we are maximizing. 
        # if alpha is already bigger or equal than beta, minplayer won't choose this branch anyways, so we don't bother checking further
        if alpha >= beta:
            break
    
    return max_value, max_move