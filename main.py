import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE
from checkers.game import Game


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
