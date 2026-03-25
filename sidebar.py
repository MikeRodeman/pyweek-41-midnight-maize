import pygame
from constants import *

class Sidebar:
    def __init__(self):
        # Start where the maze ends at the right.
        self.rect = pygame.Rect(MAZE_WIDTH, 0, SIDEBAR_WIDTH, LOGICAL_SCREEN_HEIGHT)
    
    def draw(self, surface):
        pygame.draw.rect(surface, SIDEBAR_COLOR, self.rect)