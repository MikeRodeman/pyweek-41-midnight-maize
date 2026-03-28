import pygame
import sys
from constants import *
from maze import Maze
from sidebar import Sidebar
from player import Player
from scarecrow import *
from lookout_tower import LookoutTower
from menus import *
from event_handler import EventHandler

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (LOGICAL_SCREEN_WIDTH, LOGICAL_SCREEN_HEIGHT),
            pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption("Midnight Maize")
        self.clock = pygame.time.Clock()

        # Stack to keep track of the game state:
        self.state_stack = [GameState.START_MENU]
        
        self.large_font = pygame.font.Font(LARGE_FONT_PATH, 32)
        self.small_font = pygame.font.Font(SMALL_FONT_PATH, 16)

        # The ground:
        self.ground_img = pygame.image.load("ground.png").convert()

        # The nightfall surface that goes over the maze:
        self.nightfall = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT))
        
        # This causes magenta to act like green in a green screen.
        # It will appear transparent. This is for the circular cutouts
        # in the nightfall surface:
        self.nightfall.set_colorkey((255, 0, 255)) 
        
        self.menus = MenuManager(self.large_font, self.small_font)

        self.event_handler = EventHandler(self)

        self.new_game()
        self.running = True
    
    @property
    def state(self):
        """Always returns the current active state (top of stack)."""
        return self.state_stack[-1]

    def change_state(self, new_state):
        self.state_stack.append(new_state)

    def go_back(self):
        if len(self.state_stack) > 1:
            self.state_stack.pop()
    
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
        self.elapsed_ticks = 0

        # Record when this specific game started.
        # Used in pause screen to keep time paused:
        self.last_frame_ticks = pygame.time.get_ticks()

        # Instead of drawing the maze from scratch on every frame,
        # create a Surface to put the maze on, and you can just
        # blit the surface to the screen:
        self.background_surface = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT))
        self.background_surface.blit(self.ground_img, (0, 0))

        # Draw the maze on top of the surface:
        self.maze.draw(self.background_surface)
        
    def handle_events(self):
        self.event_handler.process_events()
    
    def draw_screen(self):
        # Always draw the game world in the background (except start menu):
        if self.state != GameState.START_MENU:
            self.screen.blit(self.background_surface, (0, 0))
            self.character_sprites.draw(self.screen)
            self.glow_stick_sprites.draw(self.screen)

            # Fill the nightfall surface with a really dark blue:
            self.nightfall.fill((5, 5, 12))

            # Cut out a hole in the nightfall for the player.
            # Magenta acts as green in a green screen:
            pygame.draw.circle(self.nightfall, (255, 0, 255), self.player.rect.center, PLAYER_LIGHT_RADIUS)

            # Also cut out holes in the nightfall for the glow sticks:
            for glow_stick_sprite in self.glow_stick_sprites:
                pygame.draw.circle(self.nightfall, (255, 0, 255), glow_stick_sprite.rect.center, GLOW_STICK_LIGHT_RADIUS)

            # Draw the nightfall over the maze:
            self.screen.blit(self.nightfall, (0, 0))

            # Draw sidebar after nightfall is drawn so it stays on top:
            self.sidebar.draw(self.screen, self.player, self.elapsed_ticks)

        # Route the drawing based on the active state:
        if self.state == GameState.START_MENU:
            self.menus.draw_start_menu(self.screen)
        elif self.state == GameState.PAUSED_MENU:
            self.menus.draw_paused_menu(self.screen)
        elif self.state == GameState.STORY_SCREEN:
            self.menus.draw_story_screen(self.screen)
        elif self.state == GameState.CONTROLS_SCREEN:
            self.menus.draw_controls_screen(self.screen)
        elif self.state == GameState.ENTER_SEED_SCREEN:
            self.menus.draw_enter_seed_screen(self.screen)
        elif self.state == GameState.CURRENT_SEED_SCREEN:
            self.menus.draw_current_seed_screen(self.screen, self.maze.seed)
        elif self.state == GameState.RESULTS_SCREEN:
            self.menus.draw_results_screen(
                self.screen, 
                self.last_result_won, 
                self.last_result_time_string, 
                self.last_result_sticks_used, 
                self.last_result_sticks_left, 
                self.maze.seed
            )

        pygame.display.flip()

    def update(self):
        # Calculate how much time has passed since last loop:
        current_ticks = pygame.time.get_ticks()
        delta_time = current_ticks - self.last_frame_ticks

        # Always update the last frame ticks, otherwise after
        # unpausing, the time will include all the paused time:
        self.last_frame_ticks = current_ticks

        if self.state == GameState.PLAYING:
            self.elapsed_ticks += delta_time

            self.glow_stick_sprites.update()
            self.player.update(self.maze)
            self.scarecrow.update(self.maze, self.player)

            # Lose condition:
            if self.player.hitbox_rect.colliderect(self.scarecrow.hitbox_rect):
                self.show_results(False)
            
            # Win condition:
            if self.player.hitbox_rect.colliderect(self.lookout_tower.rect):
                self.show_results(True)
    
    def show_results(self, won):
        # Calculate final stats:
        total_seconds = self.elapsed_ticks / 1000 # Seconds
        minutes = int(total_seconds / 60)
        seconds = total_seconds - minutes * 60

        if minutes > 0:
            time_string = f"{minutes} minutes, {seconds:.2f} seconds"
        else:
            time_string = f"{seconds:.2f} seconds"

        # Save stats to the game object so results menu can read them:
        self.last_result_won = won
        self.last_result_time_string = time_string
        self.last_result_sticks_used = self.player.glow_sticks_used
        self.last_result_sticks_left = self.player.glow_sticks_left

        # Clear everything before in the state stack so the player
        # can't "unpause" a finished game:
        self.state_stack = [GameState.RESULTS_SCREEN]

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