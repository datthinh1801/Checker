import pygame
from .constants import BLACK, WHITE, ROWS, COLS, SQUARE_SIZE
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
        """Initialize the actual Board."""
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move(self, piece, row, col):
        """Move a Piece."""
        if piece != 0:
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
                if piece != 0:
                    piece.draw(win)

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        up = piece.row - 1
        down = piece.row + 1
        row = piece.row
