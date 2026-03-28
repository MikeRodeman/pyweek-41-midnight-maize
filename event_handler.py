import pygame
import sys
from constants import *

class EventHandler:
    def __init__(self, game):
        self.game = game

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                current_state = self.game.state

                if current_state == GameState.PLAYING:
                    self.handle_playing(event)
                elif current_state == GameState.START_MENU:
                    self.handle_start_menu(event)
                elif current_state == GameState.PAUSED_MENU:
                    self.handle_paused_menu(event)
                elif current_state == GameState.STORY_SCREEN:
                    self.handle_story_screen(event)
                elif current_state == GameState.CONTROLS_SCREEN:
                    self.handle_controls_screen(event)
                elif current_state == GameState.ENTER_SEED_SCREEN:
                    self.handle_enter_seed(event)
                elif current_state == GameState.CURRENT_SEED_SCREEN:
                    self.handle_current_seed(event)

    def handle_playing(self, event):
        if event.key == pygame.K_SPACE:
            glow_stick = self.game.player.drop_glow_stick()
            if glow_stick:
                self.game.glow_stick_sprites.add(glow_stick)
                self.game.glow_sticks_dropped += 1
                
                # Grace period check so the player can drop glow sticks at
                # beginning of game without immediately being chased down:
                if (self.game.elapsed_ticks / 1000 > GRACE_PERIOD) or (self.game.glow_sticks_dropped > GRACE_GLOW_STICKS_AMOUNT):
                    self.game.scarecrow.investigate_glow_stick(glow_stick.grid_position)
                    
        elif event.key == pygame.K_ESCAPE:
            self.game.change_state(GameState.PAUSED_MENU)

    def handle_start_menu(self, event):
        if event.key == pygame.K_s:
            self.game.new_game() # Generate new random map
            self.game.state_stack = [GameState.PLAYING] # Clear stack and play
        elif event.key == pygame.K_e:
            self.game.change_state(GameState.ENTER_SEED_SCREEN)
        elif event.key == pygame.K_t:
            self.game.menus.current_story_page = 0
            self.game.change_state(GameState.STORY_SCREEN)
        elif event.key == pygame.K_c:
            self.game.change_state(GameState.CONTROLS_SCREEN)
        elif event.key == pygame.K_q:
            self.game.running = False

    def handle_paused_menu(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.go_back() # Pop pause menu, resume playing
        elif event.key == pygame.K_r:
            self.game.new_game(self.game.maze.seed) # Restart current map
            self.game.state_stack = [GameState.PLAYING]
        elif event.key == pygame.K_n:
            self.game.new_game() # Start new map
            self.game.state_stack = [GameState.PLAYING]
        elif event.key == pygame.K_v:
            self.game.change_state(GameState.CURRENT_SEED_SCREEN)
        elif event.key == pygame.K_q:
            self.game.state_stack = [GameState.START_MENU] # Nuke stack, go to main menu

    def handle_story_screen(self, event):
        if event.key == pygame.K_SPACE:
            self.game.menus.current_story_page += 1
            if self.game.menus.current_story_page >= len(self.game.menus.story_pages):
                self.game.menus.current_story_page = 0
                self.game.go_back() # Go back to whatever menu we came from
        elif event.key == pygame.K_BACKSPACE:
            self.game.go_back()

    def handle_controls_screen(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.game.go_back()

    def handle_enter_seed(self, event):
        if event.key == pygame.K_RETURN:
            # Start game with custom seed
            seed_to_use = self.game.menus.seed_input_text if self.game.menus.seed_input_text else None
            self.game.new_game(seed_to_use)
            self.game.state_stack = [GameState.PLAYING]
            self.game.menus.seed_input_text = "" # Clear input for next time
        elif event.key == pygame.K_BACKSPACE:
            if len(self.game.menus.seed_input_text) > 0:
                self.game.menus.seed_input_text = self.game.menus.seed_input_text[:-1]
            else:
                self.game.go_back() # Exit if box is empty
        else:
            # Type alphanumeric chars (max 12)
            if len(self.game.menus.seed_input_text) < 12 and event.unicode.isalnum():
                self.game.menus.seed_input_text += event.unicode

    def handle_current_seed(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.game.go_back()