import pygame
from .constants import BLACK, WHITE, ROWS, COLS, SQUARE_SIZE
from .piece import Piece


class Board:
    def __init__(self):
        """Initialize the Board."""
        # The self.board represents checkers on the board.
        self.board = []
        self.selected_piece = None

        # The number of checkers left.
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0

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

    def draw(self, win):
        """Draw all the squares and pieces."""
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
