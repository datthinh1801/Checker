import pygame
from .board import Board
from .constants import WHITE, DARK_RED
from .constants import BLUE, SQUARE_SIZE


class Game:
    def __init__(self, win):
        """Initialize the Game."""
        # What piece is selected
        self._init()
        self.win = win

    def update(self):
        """Up date game's surface."""
        self.board.draw(self.win)
        self.draw_valid_moves()
        pygame.display.update()

    def _init(self):
        """Set initial values for dynamic attributes."""
        self.selected = None
        self.board = Board()
        self.turn = DARK_RED
        self.valid_moves = {}

    def reset(self):
        """Reset attributes."""
        self._init()

    def select(self, row, col):
        """Select a piece."""
        if self.selected is not None:
            # If a piece has already been selected, then try to move that piece to (row, col).
            result = self._move(row, col)

            # If cannot move the selected piece to (row, col),
            # then try to select the piece at (row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        else:
            # If there is no selected pieced, then try to select the piece at (row, col).
            piece = self.board.get_piece(row, col)

            # If the selected piece is in its turn, select that piece and find its valid moves.
            if piece is not None and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
            return False

    def _move(self, row, col):
        """Move the selected piece in to the (row, col) square."""
        piece = self.board.get_piece(row, col)
        if self.selected is not None and piece is None and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            if self.valid_moves[(row, col)] is not None:
                self.board.remove_pieces(self.valid_moves[(row, col)])
            self.change_turn()
            return True
        return False

    def change_turn(self):
        """Change turn."""
        if self.turn == WHITE:
            self.turn = DARK_RED
        else:
            self.turn = WHITE

        self.valid_moves = {}
        self.selected = None

    def draw_valid_moves(self):
        """Draw valid moves."""
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                               SQUARE_SIZE // 8)

    def get_winner(self):
        """Get the winner if any."""
        return self.board.get_winner()

    def get_board(self):
        """Get the board."""
        return self.board

    def ai_move(self, board):
        """Update the current board with a new board containing AI's move."""
        self.board = board
        self.change_turn()