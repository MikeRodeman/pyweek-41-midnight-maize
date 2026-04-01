import pygame
from constants import *

class GlowStick(pygame.sprite.Sprite):
    def __init__(self, pixel_position):
        super().__init__()

        # Pixel art:
        self.image = pygame.image.load("glow_stick.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = pixel_position

        self.grid_x = pixel_position[0] // TILE_SIZE
        self.grid_y = pixel_position[1] // TILE_SIZE
        self.grid_position = (self.grid_x, self.grid_y)