import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
from checkers.button import PlayButton

BG_DIR = 'asset/bg.jpg'


class Checker:
    def __init__(self):
        """Initialize the main game object."""
        # Init pygame.
        pygame.init()
        pygame.display.set_caption('Checkers')
        self.FPS = 60
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))

        # Init game status attributes.
        self.active = True
        self.new_game = True
        self.clock = pygame.time.Clock()

        # Create game object.
        self.game = Game(self.win)

        # Create PLAY button.
        self.play_button = PlayButton(self.win)

        # Load background image.
        self.bg_img = pygame.transform.scale(pygame.image.load(BG_DIR), (WIDTH, HEIGHT))

    @classmethod
    def _get_row_col_from_mouse(cls, pos):
        x, y = pos
        # x ~ column
        # y ~ row
        return y // SQUARE_SIZE, x // SQUARE_SIZE

    def _check_events(self):
        """Handle key and mouse interactions."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.new_game:
                    self._check_button(mouse_pos)
                else:
                    # Get the row and column of the clicked position.
                    row, col = Checker._get_row_col_from_mouse(mouse_pos)
                    self.game.select(row, col)

    def _check_keydown_events(self, event):
        """Handle keypress events."""
        if event.key == pygame.K_q:
            self.active = False

    def _check_button(self, mouse_pos):
        """Start a new game when user click the Play button."""
        play_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_clicked:
            self.new_game = False

    def _start_new_game(self):
        """Start a new game."""
        self.win.fill((0, 0, 0))
        self.win.blit(self.bg_img, (0, 0))
        self.play_button.draw_button()
        pygame.display.flip()

    def _check_winner(self):
        """Check if there is a winner."""
        winner = self.game.get_winner()
        if winner is not None:
            print(winner)
            self.active = False

    def run(self):
        while self.active:
            self.clock.tick(self.FPS)

            if not self.new_game:
                if self.game.turn == WHITE:
                    value, new_board = minimax(self.game.get_board(), 3, True, self.game)
                    self.game.ai_move(new_board)

                self._check_winner()
                self.game.update()
            else:
                self._start_new_game()
            self._check_events()


pygame.quit()

game = Checker()
game.run()
