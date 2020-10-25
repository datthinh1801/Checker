from copy import deepcopy
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def minimax(board, depth, max_player, game):
    """
    Implement the minimax algorithm.
    This assumes that the WHITE player is AI.
    :param board: the current board in the algorithm.
    :param depth: the depth of the decision-making tree of the algorithm.
    :param max_player: if True, we're the maximizing player; otherwise, minimizing.
    :param game: the game object.
    :return: new board containing new movements.
    """
    if depth == 0 or board.get_winner() is not None:
        return board.evaluate(), board

    if max_player is True:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(board, WHITE, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(board, BLACK, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move


def simulate_moves(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove_pieces(skip)

    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_moves(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves
