from checkers.constants import WHITE, DARK_GREEN
import pygame
import pygame.sysfont


class PlayButton:
    def __init__(self, win):
        self.win = win
        self.win_rect = self.win.get_rect()

        # Set properties for PLAY button.
        self.width, self.height = 200, 50
        self.button_color = DARK_GREEN

        # Initialize the 'Play' message.
        self.text_color = WHITE
        self.font = pygame.font.SysFont(None, 40)

        # Build the button and central it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.win_rect.center

        self.prepare_msg('Play')

    def prepare_msg(self, msg):
        """Turn message (msg) into a rendered image and center the text on the button."""
        self.msg_img = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.win.fill(self.button_color, self.rect)
        self.win.blit(self.msg_img, self.msg_img_rect)

    def move_button(self, x, y):
        """Move whole button to (x + x', y + y')."""
        self.rect.x += x
        self.rect.y += y
        self.msg_img_rect.x += x
        self.msg_img_rect.y += y
