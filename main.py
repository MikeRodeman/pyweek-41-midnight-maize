import pygame
import sys
from constants import *
from maze import Maze
from sidebar import Sidebar
from player import Player
from scarecrow import *
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

        self.character_sprites = pygame.sprite.Group()

        self.player = Player(self.maze.player_starting_position)
        self.lookout_tower = LookoutTower(self.maze.lookout_tower_position)
        self.scarecrow = Scarecrow(self.maze.scarecrow_starting_position)

        self.character_sprites.add(self.lookout_tower)
        self.character_sprites.add(self.scarecrow)
        self.character_sprites.add(self.player)

        self.glow_stick_sprites = pygame.sprite.Group()
        self.glow_sticks_dropped = 0
        self.start_ticks = pygame.time.get_ticks() # Get start time in ms
        self.grace_period_over = False

        # Instead of drawing the maze from scratch on every frame,
        # create a Surface to put the maze on, and you can just
        # blit the surface to the screen:
        self.background_surface = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT))
        self.background_surface.fill(BLACK) # TODO: I think this can be deleted once we make tiles

        # Draw the maze on the surface:
        self.maze.draw(self.background_surface)
    
    def check_grace_period(self):
        if self.grace_period_over:
            return True

        seconds_passed = (pygame.time.get_ticks() - self.start_ticks) / 1000

        if seconds_passed >= 15 or self.glow_sticks_dropped >= 5:
            self.grace_period_over = True
            self.scarecrow.state = ScarecrowState.WANDER
        
        return self.grace_period_over
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    glow_stick = self.player.drop_glow_stick()

                    self.glow_stick_sprites.add(glow_stick)
                    self.glow_sticks_dropped += 1

                    self.scarecrow.investigate_glow_stick(glow_stick.grid_position)
    
    def draw_screen(self):
        self.screen.blit(self.background_surface, (0, 0))

        self.sidebar.draw(self.screen, self.player)

        self.character_sprites.draw(self.screen)
        self.glow_stick_sprites.draw(self.screen)
        
        pygame.display.flip()

    def update(self):
        self.character_sprites.update(self.maze)

        if self.player.hitbox_rect.colliderect(self.scarecrow.hitbox_rect):
            print("THE SCARECROW GOT YOU!")
            self.new_game()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw_screen()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":

    game = Game()
    game.run()