import pygame
import sys
from constants import *
from maze import Maze
from sidebar import Sidebar
from player import Player
from scarecrow import Scarecrow
from lookout_tower import LookoutTower

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (LOGICAL_SCREEN_WIDTH, LOGICAL_SCREEN_HEIGHT),
            pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("Midnight Maize")
        self.clock = pygame.time.Clock()

        self.new_game()

        self.running = True
    
    def new_game(self, seed=None):
        self.maze = Maze(seed)
        self.sidebar = Sidebar()

        self.player = Player(self.maze.player_starting_position)
        self.lookout_tower = LookoutTower(self.maze.lookout_tower_position)
        self.scarecrow = Scarecrow(self.maze.scarecrow_starting_position)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_r:
            #         self.new_game()
    
    def draw_screen(self):
        self.screen.fill(BLACK)

        self.maze.draw(self.screen)
        self.sidebar.draw(self.screen)

        self.player.draw(self.screen)
        self.lookout_tower.draw(self.screen)
        self.scarecrow.draw(self.screen)

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