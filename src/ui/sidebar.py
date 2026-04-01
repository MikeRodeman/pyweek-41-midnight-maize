import pygame
import os
from constants import *
from player import *

class Sidebar:
    def __init__(self):
        # Start where the maze ends at the right.
        self.rect = pygame.Rect(MAZE_WIDTH, 0, SIDEBAR_WIDTH, LOGICAL_SCREEN_HEIGHT)

        if os.path.exists(SMALL_FONT_PATH):
            self.font = pygame.font.Font(SMALL_FONT_PATH, 16)
        else:
            # Fallback
            self.font = pygame.font.SysFont(None, 16)
    
    def draw(self, surface, player, elapsed_ticks):
        # Draw background:
        pygame.draw.rect(surface, SIDEBAR_COLOR, self.rect)

        # Stamina info:
        stamina_text = f"STAMINA: {int(player.stamina)}%"
        stamina_color = (255, 50, 50) if player.is_exhausted else WHITE
        stamina_surface = self.font.render(stamina_text, False, stamina_color)
        surface.blit(stamina_surface, (self.rect.x + 5, 20))

        # Glow sticks info:
        glow_sticks_text = f"GLOW STICKS: {player.glow_sticks_left}"
        glow_sticks_color = WHITE
        glow_sticks_surface = self.font.render(glow_sticks_text, False, glow_sticks_color)
        surface.blit(glow_sticks_surface, (self.rect.x + 5, 50))

        # Time info:
        total_seconds = elapsed_ticks / 1000
        minutes = int(total_seconds / 60)
        seconds = total_seconds - minutes * 60

        if minutes > 0:
            time_text = f"TIME: {minutes} m, {seconds:.2f} s"
        else:
            time_text = f"TIME: {seconds:.2f} s"

        time_surface = self.font.render(time_text, False, WHITE)
        surface.blit(time_surface, (self.rect.x + 5, 80))

        pause_text = "[ESC] PAUSE"
        pause_text_surface = self.font.render(pause_text, False, WHITE)
        surface.blit(pause_text_surface, (self.rect.x + 5, 140))