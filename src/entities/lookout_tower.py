import pygame

import src.core.constants as c
from src.core.custom_types import Coordinate

class LookoutTower(pygame.sprite.Sprite):
    def __init__(self, grid_position: Coordinate) -> None:
        # Call parent constructor:
        super().__init__()

        # Pixel art:
        self.image = pygame.image.load(c.GRAPHICS_DIR / "lookout_tower.png").convert_alpha()

        # Set position:
        self.pos_x = grid_position[0] * c.TILE_SIZE + c.TILE_SIZE // 2
        self.pos_y = grid_position[1] * c.TILE_SIZE + c.TILE_SIZE // 2
        
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.pos_x), int(self.pos_y))
