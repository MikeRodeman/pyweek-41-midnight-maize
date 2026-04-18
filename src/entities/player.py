import pygame

import src.core.constants as c
from src.core.maze import Maze
from src.core.custom_types import Coordinate
from src.entities.glow_stick import GlowStick

class Player(pygame.sprite.Sprite):
    def __init__(self, starting_grid_position: Coordinate) -> None:
        # Call parent constructor:
        super().__init__()

        # Pixel art:
        self.image = pygame.image.load(c.GRAPHICS_DIR / "player.png").convert_alpha()

        # Make Rect for the pixel art
        self.rect = self.image.get_rect()

        # Set grid location:
        self.current_grid_position = starting_grid_position

        # Set starting position:
        self.pos_x = starting_grid_position[0] * c.TILE_SIZE + c.TILE_SIZE // 2
        self.pos_y = starting_grid_position[1] * c.TILE_SIZE + c.TILE_SIZE // 2

        # Make Rect for the hitbox, smaller than the visual rect
        # so the sprite can fit between the walls of the maze:
        self.hitbox_rect = pygame.Rect(0, 0, 8, 8)
        self.hitbox_rect.center = (int(self.pos_x), int(self.pos_y))

        # Line up the center of the visual rect with the center of the hitbox rect:
        self.rect.center = self.hitbox_rect.center
        
        self.speed = c.PLAYER_SPEED
        self.stamina = c.MAX_STAMINA
        self.is_exhausted = False

        self.glow_sticks_left = c.INITIAL_GLOW_STICKS
        self.glow_sticks_used = 0

    def update(self, maze: Maze) -> None:
        keys = pygame.key.get_pressed()

        if self.stamina <= 0:
            self.is_exhausted = True
        elif self.stamina >= 20: # Can only run again after recovering to 20%
            self.is_exhausted = False

        can_run = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and not self.is_exhausted

        # Check if any movement key is being pressed:
        is_moving = any([keys[pygame.K_UP], keys[pygame.K_w], keys[pygame.K_DOWN], 
                        keys[pygame.K_s], keys[pygame.K_LEFT], keys[pygame.K_a], 
                        keys[pygame.K_RIGHT], keys[pygame.K_d]])
        
        if can_run and is_moving:
            self.speed = c.PLAYER_RUN_SPEED
            self.stamina = max(0, self.stamina - c.STAMINA_DECAY)
        else:
            self.speed = c.PLAYER_SPEED
            self.stamina = min(c.MAX_STAMINA, self.stamina + c.STAMINA_REGEN)
        
        dx, dy = 0.0, 0.0

        if keys[pygame.K_UP] or keys[pygame.K_w]: dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += self.speed

        self.current_grid_position = (int(self.pos_x // c.TILE_SIZE), int(self.pos_y // c.TILE_SIZE))

        # Horizontal movement and collision:
        self.pos_x += dx
        self.hitbox_rect.centerx = int(self.pos_x)
        self.handle_collision(maze, "x", dx)

        #Vertical movement and collision:
        self.pos_y += dy
        self.hitbox_rect.centery = int(self.pos_y)
        self.handle_collision(maze, "y", dy)

        # Line up center of the visual rect with the center of the hitbox rect:
        self.rect.center = self.hitbox_rect.center
    
    def handle_collision(self, maze: Maze, axis: str, delta: float) -> None:
        # Instead of checking all walls, check just the walls
        # in the current cell and the 8 neighboring cells:
        wall_rects_to_check: list[pygame.Rect] = []

        grid_x, grid_y = self.current_grid_position

        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x, neighbor_y = grid_x + i, grid_y + j

                if 0 <= neighbor_x < c.GRID_SIZE and 0 <= neighbor_y < c.GRID_SIZE:
                    wall_rects = maze.wall_rects[(neighbor_x, neighbor_y)]
                    wall_rects_to_check.extend(wall_rects)
        
        # Remove any Nones in case any cells have no walls:
        wall_rects_to_check = [wall_rect for wall_rect in wall_rects_to_check if wall_rect]

        for wall_rect in wall_rects_to_check:
            if self.hitbox_rect.colliderect(wall_rect):
                # Resolve horizontal collisions:
                if axis == "x":
                    if delta > 0: self.hitbox_rect.right = wall_rect.left
                    elif delta < 0: self.hitbox_rect.left = wall_rect.right
                    self.pos_x = self.hitbox_rect.centerx

                # Resolve vertical collisions:
                if axis == "y":
                    if delta > 0: self.hitbox_rect.bottom = wall_rect.top
                    elif delta < 0: self.hitbox_rect.top = wall_rect.bottom
                    self.pos_y = self.hitbox_rect.centery

    def drop_glow_stick(self) -> GlowStick | None:
        """Create a glow stick at the player's current center if any are left."""
        if self.glow_sticks_left > 0:
            self.glow_sticks_left -= 1
            self.glow_sticks_used += 1      
            
            return GlowStick(self.rect.center)
        
        return None