from .constants import WHITE, SQUARE_SIZE, GREY
import pygame


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        """Initialize a piece."""
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        if self.color == WHITE:
            # If piece if WHITE, it is located at the bottom of the Board,
            # So it needs to move down.
            self.direction = 1
        else:
            self.direction = -1

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        """Calculate the position of Piece based on the row and col it is in."""
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.King = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    def __repr__(self):
        return str(self.color)
