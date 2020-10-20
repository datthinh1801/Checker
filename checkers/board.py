import pygame
from .constants import WHITE, BLACK, ROWS, COLS, SQUARE_SIZE
from .piece import Piece


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
        left = piece.col - 1
        right = piece.col + 1
        up = piece.row - 1
        down = piece.row + 1

        # if piece.color == BLACK:
        #     moves.update(self._move_left(up, max(up - 2, -1), -1, left, piece.color))
        #     moves.update(self._move_right(up, max(up - 2, -1), -1, right, piece.color))
        # else:
        #     moves.update(self._move_left(down, min(down + 2, ROWS), 1, left, piece.color))
        #     moves.update(self._move_right(down, min(down + 2, ROWS), 1, right, piece.color))

        moves.update(self._move_left(up, max(up - 2, -1), -1, left, piece.color))
        moves.update(self._move_right(up, max(up - 2, -1), -1, right, piece.color))
        moves.update(self._move_left(down, min(down + 2, ROWS), 1, left, piece.color))
        moves.update(self._move_right(down, min(down + 2, ROWS), 1, right, piece.color))
        return moves

    def _move_left(self, start, stop, step, col, color, skipped_pieces=[]):
        """
        Check if the selected piece can move to (row, col) position diagonally.

        :param start: starts checking from start row.
        :param stop: stops checking when reaches this stop row.
        :param step: +1 if move up, and -1 if move down.
        :param col: column to start checking.
        :param color: color of the selected piece.
        :param skipped_pieces: store stacked skipped pieces.
        :return: valid moves.
        """
        moves = {}
        last_selected = []

        for row in range(start, stop, step):
            if col < 0:
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

                # If we've jumped over some pieces (skipped_pieces) and
                # jumped over a piece (last_selected) in this diagonal line,
                # then this is a valid move.
                if skipped_pieces and last_selected:
                    moves[(row, col)] = skipped_pieces + last_selected
                # If we've jumped over some pieces (skipped_pieces) but
                # not jumped over any piece (last_selected) in this diagonal line,
                # then this is an invalid move.
                elif skipped_pieces:
                    break
                # If we've not jumped over any pieces any where.
                else:
                    moves[(row, col)] = last_selected
                    break

                # If a piece is jumped over.
                if last_selected:
                    # In case moving up, we just check 3 rows upwards or until reach the edge.
                    if step == -1:
                        stop = max(row - 3, -1)
                    # In case moving down, we just check 3 rows downwards or until reach the edge.
                    else:
                        stop = min(row + 3, ROWS)

                    # Recursive calls for multiple jumps.
                    moves.update(self._move_left(row + step, stop, step, col - 1, color, skipped_pieces=last_selected))
                    moves.update(self._move_right(row + step, stop, step, col + 1, color, skipped_pieces=last_selected))
                    break
            col -= 1
        return moves

    def _move_right(self, start, stop, step, col, color, skipped_pieces=[]):
        """
        Check if the selected piece can move to (row, col) position diagonally.
        :param start: starts checking at start row.
        :param stop: stops checking at stop row.
        :param step: +1 if move up, and -1 if move down.
        :param col: column to start checking.
        :param color: color of the selected piece.
        :param skipped_pieces: store stacked skipped pieces.
        :return: valid moves.
        """
        moves = {}
        last_selected = []

        for row in range(start, stop, step):
            if col >= COLS:
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
                # If we've jumped over some pieces (skipped_pieces) and
                # jumped over a piece (last_selected) in this diagonal line,
                # then this is a valid move.
                if skipped_pieces and last_selected:
                    moves[(row, col)] = skipped_pieces + last_selected
                # If we've jumped over some pieces (skipped_pieces) but
                # not jumped over any piece (last_selected) in this diagonal line,
                # then this is an invalid move.
                elif skipped_pieces:
                    break
                # If we've not jumped over any pieces any where.
                else:
                    moves[(row, col)] = last_selected
                    break

                # If a piece is jumped over.
                if last_selected:
                    # In case moving up, we just check 3 rows upwards or until reach the edge.
                    if step == -1:
                        stop = max(row - 3, -1)
                    # In case moving down, we just check 3 rows downwards or until reach the edge.
                    else:
                        stop = min(row + 3, ROWS)

                    # Recursive calls for multiple jumps.
                    moves.update(self._move_left(row + step, stop, step, col - 1, color, skipped_pieces=last_selected))
                    moves.update(self._move_right(row + step, stop, step, col + 1, color, skipped_pieces=last_selected))
                    break
            col += 1

        return moves
