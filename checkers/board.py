import pygame
from .constants import WHITE, BLACK, ROWS, COLS, SQUARE_SIZE
from .piece import Piece
from copy import deepcopy


class Board:
    def __init__(self):
        """Initialize the Board."""
        # The self.board represents checkers on the board.
        self.board = []

        # The number of checkers left.
        self.black_left = self.white_left = 12

        self.create_board()

    def draw_squares(self, win):
        """Draw atomic squares of the Board."""
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        """Initialize the actual Board without pieces."""
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def move(self, piece, row, col):
        """Move a Piece."""
        if piece is not None:
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][
                piece.col]
            piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def draw(self, win):
        """Draw all the squares and pieces."""
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(win)

    def remove_piece(self, row, col):
        """Remove a defeated piece from board and return it."""
        self.board[row][col] = None

    def get_valid_moves(self, piece):
        # The 'moves' arg stores pos (x, y) as keys, and the piece over which it jumps,
        # or None for an empty square as values.
        moves = {}
        row = piece.row
        col = piece.col

        # Get valid left-up moves.
        moves.update(self._move_left(row - 1, max(row - 3, -1), -1, col - 1, piece.color))

        # Get valid right-up moves.
        moves.update(self._move_right(row - 1, max(row - 3, -1), -1, col + 1, piece.color))

        # Get valid left-down moves.
        moves.update(self._move_left(row + 1, min(row + 3, ROWS), 1, col - 1, piece.color))

        # Get valid right-down moves.
        moves.update(self._move_right(row + 1, min(row + 3, ROWS), 1, col + 1, piece.color))

        return moves

    def _move_left(self, start, stop, step, col, color, jumped_pieces=None):
        """
        Check if the selected piece can move to (row, col) position diagonally.

        :param start: starts checking from start row.
        :param stop: stops checking when reaches this stop row.
        :param step: -1 if move up, and +1 if move down.
        :param col: column to start checking.
        :param color: color of the selected piece.
        :param jumped_pieces: store stacked skipped pieces.
        :return: valid moves.
        """
        moves = {}
        last_selected = []
        if jumped_pieces is None:
            jumped_pieces = []

        for row in range(start, stop, step):
            if col < 0:
                break

            if (row, col) in map(lambda p: (p.row, p.col), jumped_pieces):
                break

            # Select the piece located at (row, col).
            piece = self.get_piece(row, col)

            # If a checker is selected.
            if piece:
                # If the selected piece is of the same Team,
                # then this is an invalid move.
                if piece.color == color:
                    break
                else:
                    # If we've already jumped over another piece in this diagonal line,
                    # then this is an invalid move.
                    if last_selected:
                        break
                    # If we've not jumped any pieces before,
                    # then we can jump over this piece.
                    else:
                        last_selected = [piece]
            # Else the piece is available.
            else:
                # If we've jumped over some pieces (jumped_pieces)
                if jumped_pieces:
                    # And we can jump over another piece, then this is a valid move.
                    if last_selected:
                        moves[(row, col)] = jumped_pieces + last_selected
                    # and we cannot jump over any piece, then this is an invalid move.
                    else:
                        break
                # If we've never jumped over any piece
                else:
                    # And we can jump over a piece, then this is a valid move.
                    if last_selected:
                        moves[(row, col)] = last_selected
                    # And we can move to a blank piece without jumping, then this is also a valid move,
                    # but we can only move ONCE in this diagonal line.
                    else:
                        moves[(row, col)] = None
                        break

                # If a piece is jumped over.
                if last_selected:
                    # Recursive calls for multiple jumps.
                    # Accumulate jumped_pieces for further recursive calls.
                    jumped_pieces += last_selected
                    # Move left up.
                    moves.update(
                        self._move_left(row - 1, max(row - 3, -1), -1, col - 1, color, jumped_pieces))
                    # Move right up.
                    moves.update(
                        self._move_right(row - 1, max(row - 3, -1), -1, col + 1, color, jumped_pieces))
                    # Move left down.
                    moves.update(
                        self._move_left(row + 1, min(row + 3, ROWS), 1, col - 1, color, jumped_pieces))
                    # Move right down.
                    moves.update(
                        self._move_right(row + 1, min(row + 3, ROWS), 1, col + 1, color, jumped_pieces))
                    break
            col -= 1
        return moves

    def _move_right(self, start, stop, step, col, color, jumped_pieces=None):
        """
        Check if the selected piece can move to (row, col) position diagonally.
        :param start: starts checking at start row.
        :param stop: stops checking at stop row.
        :param step: -1 if move up, and +1 if move down.
        :param col: column to start checking.
        :param color: color of the selected piece.
        :param jumped_pieces: store stacked skipped pieces.
        :return: valid moves.
        """
        moves = {}
        last_selected = []
        if jumped_pieces is None:
            jumped_pieces = []

        for row in range(start, stop, step):
            if col >= COLS:
                break

            # If we've already jumped over this piece in previous call, then break.
            if (row, col) in map(lambda p: (p.row, p.col), jumped_pieces):
                break

            piece = self.get_piece(row, col)

            # If a checker is selected.
            if piece:
                # If the selected piece is of the same Team,
                # then this is an invalid move.
                if piece.color == color:
                    break
                else:
                    # If we've already jumped over another piece in this diagonal line,
                    # then this is an invalid move.
                    if last_selected:
                        break
                    # If we've not jumped any pieces before,
                    # then we can jump over this piece.
                    else:
                        last_selected = [piece]
            # Else the piece is available.
            else:
                # If we've jumped over some pieces (jumped_pieces)
                if jumped_pieces:
                    # And we can jump over another piece, then this is a valid move.
                    if last_selected:
                        moves[(row, col)] = jumped_pieces + last_selected
                    # and we cannot jump over any piece, then this is an invalid move.
                    else:
                        break
                # If we've never jumped over any piece
                else:
                    # And we can jump over a piece, then this is a valid move.
                    if last_selected:
                        moves[(row, col)] = last_selected
                    # And we can move to a blank piece without jumping, then this is also a valid move,
                    # but we can only move ONCE in this diagonal line.
                    else:
                        moves[(row, col)] = None
                        break

                # If a piece is jumped over.
                if last_selected:
                    # Recursive calls for multiple jumps.
                    # Accumulate jumped_pieces for further recursive jumps.
                    jumped_pieces += last_selected
                    # Move left up.
                    moves.update(self._move_left(row - 1, max(row - 3, -1), -1, col - 1, color, jumped_pieces))
                    # Move right up.
                    moves.update(self._move_right(row - 1, max(row - 3, -1), -1, col + 1, color, jumped_pieces))
                    # Move left down.
                    moves.update(self._move_left(row + 1, min(row + 3, ROWS), 1, col - 1, color, jumped_pieces))
                    # Move right down.
                    moves.update(self._move_right(row + 1, min(row + 3, ROWS), 1, col + 1, color, jumped_pieces))
                    break
            col += 1
        return moves
