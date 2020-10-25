import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from checkers.game import Game
from minimax.algorithm import minimax


class Checker:
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    def __init__(self):
        pygame.display.set_caption('Checkers')
        self.active = True
        self.clock = pygame.time.Clock()
        self.game = Game(self.WIN)

    def _get_row_col_from_mouse(self, pos):
        x, y = pos
        # x ~ column
        # y ~ row
        return y // SQUARE_SIZE, x // SQUARE_SIZE

    def run(self):

        while self.active:
            self.clock.tick(self.FPS)

            if self.game.turn == WHITE:
                value, new_board = minimax(self.game.get_board(), 3, True, self.game)
                self.game.ai_move(new_board)

            winner = self.game.get_winner()
            if winner is not None:
                print(winner)
                self.active = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the row number and column number of the clicked position.
                    row, col = self._get_row_col_from_mouse(pygame.mouse.get_pos())
                    self.game.select(row, col)

                self.game.update()

        pygame.quit()


game = Checker()
game.run()
