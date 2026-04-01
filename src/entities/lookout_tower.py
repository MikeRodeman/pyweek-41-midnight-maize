import pygame
from constants import *

class LookoutTower(pygame.sprite.Sprite):
    def __init__(self, position):
        # Call parent constructor:
        super().__init__()

        # Pixel art:
        self.image = pygame.image.load("lookout_tower.png").convert_alpha()

        # Set position:
        self.pos_x = position[0] * TILE_SIZE + TILE_SIZE // 2
        self.pos_y = position[1] * TILE_SIZE + TILE_SIZE // 2
        
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.pos_x), int(self.pos_y))
