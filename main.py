import pygame
import sys
from constants import *
from maze import Maze
from sidebar import Sidebar

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (LOGICAL_SCREEN_WIDTH, LOGICAL_SCREEN_HEIGHT),
            pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("Midnight Maize")
        self.clock = pygame.time.Clock()

        self.new_game("PyWeek41")

        self.running = True
    
    def new_game(self, specific_seed=None):
        self.maze = Maze(specific_seed)
        self.sidebar = Sidebar()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def draw_screen(self):
        self.screen.fill(BLACK)

        self.maze.draw(self.screen)
        self.sidebar.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_screen()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":

    game = Game()
    game.run()