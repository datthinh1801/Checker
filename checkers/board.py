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
        piece = self.get_piece(row, col)
        self.board[row][col] = None
        return piece

    def get_valid_moves(self, piece):
        # The 'moves' arg stores pos (x, y) as keys, and the opponent piece which it jumps over,
        # or None for an empty square as values.
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        up = piece.row - 1
        down = piece.row + 1

        backup_board = deepcopy(self.board)

        self._go_left_up(up, left, piece.color, moves)
        self._go_left_down(down, left, piece.color, moves)
        self._go_right_up(up, right, piece.color, moves)
        self._go_right_down(down, right, piece.color, moves)
        return moves

    def _go_left_up(self, row, col, color, moves, skipped=[]):
        jumped = []

        if col < 0 or row < 0:
            return

        # Get the piece located at (row, col).
        piece = self.get_piece(row, col)

        # If there is a checker at (row, col).
        if piece is not None:
            # If the piece is in the same Team.
            if piece.color == color:
                # Pop the recently jumped piece if it intervenes the path.
                if jumped and jumped[-1].row == row + 1 and jumped[-1].col == col + 1:
                    jumped.pop()
            else:
                # Pop the recently jumped piece if it intervenes the path.
                if jumped and jumped[-1].row == row + 1 and jumped[-1].col == col + 1:
                    jumped.pop()
                else:
                    if piece.row > 0 and piece.col > 0:
                        jumped.append(piece)
        else:
            if jumped and jumped[-1].row == row + 1 and jumped[-1].col == col + 1:
                moves[(row - 1, col - 1)] = jumped[-1]
            else:
                moves[(row, col)] = None

        # for piece in jumped:
        #     self._go_left_down(piece.row - 1, piece.col - 1, color, moves)
        #     self._go_right_up(piece.row - 1, piece.col - 1, color, moves)

    def _go_left_down(self, row, col, color, moves):
        jumped = []

        if col < 0 or row >= ROWS:
            return

        # Get the piece located at (row, col).
        piece = self.get_piece(row, col)

        # If there is a checker at (down, left).
        if piece is not None:
            # If the piece is in the same Team.
            if piece.color == color:
                # Pop the recently jumped piece if it intervenes the path.
                if jumped and jumped[-1].row == row - 1 and jumped[-1].col == col + 1:
                    jumped.pop()
            else:
                # Pop the recently jumped piece if it intervenes the path.
                if jumped and jumped[-1].row == row - 1 and jumped[-1].col == col + 1:
                    jumped.pop()
                else:
                    if piece.row < ROWS - 1 and piece.col > 0:
                        jumped.append(piece)
        else:
            if jumped and jumped[-1].row == row - 1 and jumped[-1].col == col + 1:
                moves[(row + 1, col - 1)] = jumped[-1]
            else:
                moves[(row, col)] = None

        # for piece in jumped:
        #     self._go_left_up(piece.row + 1, piece.col - 1, color, moves)
        #     self._go_right_down(piece.row + 1, piece.col - 1, color, moves)

    def _go_right_up(self, row, col, color, moves):
        jumped = []

        if col >= COLS or row < 0:
            return

            # Get the piece located at (row, col).
        piece = self.get_piece(row, col)

        # If there is a checker at (row, col).
        if piece is not None:
            # If the piece is in the same Team.
            if piece.color == color:
                # Pop the recently jumped piece if it intervenes the path.
                if jumped and jumped[-1].row == row + 1 and jumped[-1].col == col - 1:
                    jumped.pop()
            else:
                # Pop the recently jumped piece if it intervenes the path.
                if jumped and jumped[-1].row == row + 1 and jumped[-1].col == col - 1:
                    jumped.pop()
                else:
                    if piece.row > 0 and piece.col < COLS - 1:
                        jumped.append(piece)
        else:
            if jumped and jumped[-1].row == row + 1 and jumped[-1].col == col - 1:
                moves[(row - 1, col + 1)] = jumped[-1]
            else:
                moves[(row, col)] = None

        # for piece in jumped:
        #     self._go_left_up(piece.row - 1, piece.col + 1, color, moves)
        #     self._go_right_down(piece.row - 1, piece.col + 1, color, moves)

    def _go_right_down(self, row, col, color, moves):
        jumped = []

        if col >= COLS or row >= COLS:
            return

            # Get the piece located at (row, col).
        piece = self.get_piece(row, col)

        # If there is a checker at (down, right).
        if piece is not None:
            # If the piece is in the same Team.
            if piece.color == color:
                # Pop the recently jumped piece if it intervenes the path.
                if jumped and jumped[-1].row == row - 1 and jumped[-1].col == col - 1:
                    jumped.pop()
            else:
                # Pop the recently jumped piece if it intervenes the path.
                if jumped and jumped[-1].row == row - 1 and jumped[-1].col == col - 1:
                    jumped.pop()
                else:
                    if piece.row < ROWS - 1 and piece.col < COLS - 1:
                        jumped.append(piece)
        else:
            if jumped and jumped[-1].row == row - 1 and jumped[-1].col == col - 1:
                moves[(row + 1, col + 1)] = jumped[-1]
            else:
                moves[(row, col)] = None

        # for piece in jumped:
        #     self._go_left_down(piece.row + 1, piece.col + 1, color, moves)
        #     self._go_right_up(piece.row + 1, piece.col + 1, color, moves)
