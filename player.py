import pygame
from constants import *
from maze import *

class Player(pygame.sprite.Sprite):
    def __init__(self, starting_position):
        # Call parent constructor:
        pygame.sprite.Sprite.__init__(self)

        # Make Surface to put pixel art on:
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

        # Draw pixel art on the Surface:
        # TODO: Replace with pixel art:
        pygame.draw.circle(self.image, (50, 50, 255), (TILE_SIZE // 2, TILE_SIZE // 2), 6)

        # Make Rect for the pixel art
        self.rect = self.image.get_rect()

        # Set grid location:
        self.grid_location = starting_position

        # Set starting position:
        self.pos_x = starting_position[0] * TILE_SIZE + TILE_SIZE // 2
        self.pos_y = starting_position[1] * TILE_SIZE + TILE_SIZE // 2

        # Make Rect for the hitbox, smaller than the visual rect
        # so the sprite can fit between the walls of the maze:
        self.hitbox_rect = pygame.Rect(0, 0, 8, 8)
        self.hitbox_rect.center = (int(self.pos_x), int(self.pos_y))

        # Line up the center of the visual rect with the center of the hitbox rect:
        self.rect.center = self.hitbox_rect.center
        
        self.speed = 1.2 # TODO: Put in constants.py?        

    def update(self, maze):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_UP] or keys[pygame.K_w]: dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += self.speed

        self.grid_location = (int(self.pos_x // TILE_SIZE), int(self.pos_y // TILE_SIZE))

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
    
    def handle_collision(self, maze, axis, delta):
        # Instead of checking all walls, check just the walls
        # in the current cell and the 8 neighboring cells:
        wall_rects_to_check = []

        grid_x, grid_y = self.grid_location

        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x, neighbor_y = grid_x + i, grid_y + j

                if 0 <= neighbor_x < GRID_SIZE and 0 <= neighbor_y < GRID_SIZE:
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
