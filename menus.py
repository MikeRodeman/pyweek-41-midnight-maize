import pygame
from constants import *

class MenuManager:
    def __init__(self, big_font, small_font):
        self.big_font = big_font
        self.small_font = small_font
        
        self.overlay = pygame.Surface((LOGICAL_SCREEN_WIDTH, LOGICAL_SCREEN_HEIGHT))
        # self.overlay.set_alpha(100)
        self.overlay.fill(BLACK)
        
        self.seed_input_text = ""
        
        self.current_story_page = 0
        self.story_pages = STORY_PAGES

    def draw_text_centered(self, screen, text, font, y_position, color=WHITE):
        surface = font.render(text, False, color)
        x_position = (LOGICAL_SCREEN_WIDTH // 2) - (surface.get_width() // 2)
        screen.blit(surface, (x_position, y_position))

    def draw_start_menu(self, screen):
        screen.fill(BLACK)
        self.draw_text_centered(screen, "MIDNIGHT MAIZE", self.big_font, 50, (255, 50, 50))
        
        options = [
            "[S] START NEW GAME",
            "[E] ENTER CUSTOM SEED",
            "[T] READ THE STORY",
            "[C] VIEW CONTROLS",
            "[Q] QUIT TO DESKTOP"
        ]
        for i, option in enumerate(options):
            self.draw_text_centered(screen, option, self.small_font, 120 + (i * 30))

    def draw_paused_menu(self, screen):
        screen.blit(self.overlay, (0, 0)) # Dim the maze
        self.draw_text_centered(screen, "PAUSED", self.big_font, 60)
        
        options = [
            "[ESC] RESUME",
            "[R] RESTART CURRENT MAP",
            "[N] START NEW RANDOM MAP",
            "[V] VIEW CURRENT SEED",
            "[Q] QUIT TO MAIN MENU"
        ]
        for i, option in enumerate(options):
            self.draw_text_centered(screen, option, self.small_font, 130 + (i * 25))

    def draw_story_screen(self, screen):
        self.draw_overlay(screen)
        self.draw_text_centered(screen, "THE TALE", self.big_font, 50)
        
        # Draw current page
        p_text = self.story_pages[self.current_story_page]
        self.draw_text_centered(screen, p_text, self.small_font, 120)
        
        footer = f"PAGE {self.current_story_page + 1} OF {len(self.story_pages)}"
        self.draw_text_centered(screen, footer, self.small_font, 180, (150, 150, 150))
        self.draw_text_centered(screen, "[SPACE] NEXT   [BACKSPACE] BACK", self.small_font, 220)

    def draw_controls_screen(self, screen):
        self.draw_overlay(screen)
        self.draw_text_centered(screen, "HOW TO SURVIVE", self.big_font, 40)
        
        controls = [
            "WASD / ARROWS : MOVE",
            "SHIFT : SPRINT (DRAINS STAMINA)",
            "SPACE : DROP GLOW STICK",
            "ESC : PAUSE / MENU",
            "",
            "OBJECTIVE: FIND THE YELLOW TOWER",
            f"SCARECROW WAKES AFTER {GRACE_PERIOD}s OR {GRACE_GLOW_STICKS_AMOUNT} STICKS DROPPED",
            "",
            "[BACKSPACE] RETURN"
        ]
        for i, line in enumerate(controls):
            self.draw_text_centered(screen, line, self.small_font, 90 + (i * 20))

    def draw_enter_seed_screen(self, screen):
        self.draw_overlay(screen)
        self.draw_text_centered(screen, "TYPE CUSTOM SEED", self.big_font, 60)
        
        # Draw the box for typing
        box_rect = pygame.Rect(LOGICAL_SCREEN_WIDTH//2 - 100, 120, 200, 30)
        pygame.draw.rect(screen, WHITE, box_rect, 2)
        
        # Render the current input string
        input_surface = self.small_font.render(self.seed_input_text + "_", False, (50, 255, 50))
        screen.blit(input_surface, (box_rect.x + 5, box_rect.y + 7))
        
        self.draw_text_centered(screen, "[ENTER] CONFIRM   [BACKSPACE] CANCEL", self.small_font, 180)

    def draw_current_seed_screen(self, screen, current_seed):
        self.draw_overlay(screen)
        self.draw_text_centered(screen, "MAP DATA", self.big_font, 70)
        self.draw_text_centered(screen, f"SEED: {current_seed}", self.small_font, 130, (255, 255, 100))
        self.draw_text_centered(screen, "SHARE THIS WITH FRIENDS", self.small_font, 160)
        self.draw_text_centered(screen, "[BACKSPACE] RETURN", self.small_font, 210)

    def draw_overlay(self, screen):
        screen.blit(self.overlay, (0, 0))