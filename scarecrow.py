import pygame
import random
from constants import *
from astar import *
from enum import Enum

class ScarecrowState(Enum):
    DORMANT = 0
    WANDER = 1
    INVESTIGATE = 2
    CHASE = 3
class Scarecrow(pygame.sprite.Sprite):
    def __init__(self, starting_position):
        # Call parent constructor:
        super().__init__()

        # Make Surface to put pixel art on:
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

        # Draw pixel art on the Surface:
        # TODO: Replace with pixel art:
        pygame.draw.circle(self.image, (255, 50, 50), (TILE_SIZE // 2, TILE_SIZE // 2), 6)

        self.rect = self.image.get_rect()

        # Set starting position:
        self.pos_x = starting_position[0] * TILE_SIZE + TILE_SIZE // 2
        self.pos_y = starting_position[1] * TILE_SIZE + TILE_SIZE // 2

        # Smaller rect for hitbox:
        self.hitbox_rect = pygame.Rect(0, 0, 8, 8)
        self.hitbox_rect.center = (int(self.pos_x), int(self.pos_y))
        
        # Line up the center of the visual rect with the center of the hitbox rect:
        self.rect.center = self.hitbox_rect.center

        self.speed = SCARECROW_SPEED
        self.state = ScarecrowState.WANDER

        # Logical position and movement on the grid:
        self.current_grid_cell = starting_position
        self.target_grid_cell = starting_position
        self.path = []

        # Memory so scarecrow doesn't backtrack randomly:
        self.opposite_directions = {N: S, S: N, W: E, E: W}
        self.last_direction_moved = None

        self.target_glow_stick_position = None
        self.target_player_position = None
    
    def update(self, maze):
        # The legs - physically move:
        self.move_to_adjacent_cell_center()

        # The brain - calculate path to follow:
        if self.current_grid_cell == self.target_grid_cell:
            self.follow_path(maze)
    
    def move_to_adjacent_cell_center(self):
        """The Legs: Move rect center from current cell to the exact center of adjacent cell."""
        target_pixel_x = self.target_grid_cell[0] * TILE_SIZE + TILE_SIZE // 2
        target_pixel_y = self.target_grid_cell[1] * TILE_SIZE + TILE_SIZE // 2

        # Use min/max to make sure we land exactly on the center without overshooting:
        if self.pos_x < target_pixel_x:
            self.pos_x = min(self.pos_x + self.speed, target_pixel_x)
        elif self.pos_x > target_pixel_x:
            self.pos_x = max(self.pos_x - self.speed, target_pixel_x)
        
        if self.pos_y < target_pixel_y:
            self.pos_y = min(self.pos_y + self.speed, target_pixel_y)
        elif self.pos_y > target_pixel_y:
            self.pos_y = max(self.pos_y - self.speed, target_pixel_y)

        # Sync rects:
        self.hitbox_rect.center = (int(self.pos_x), int(self.pos_y))
        self.rect.center = self.hitbox_rect.center

        # Update current cell if arrived:
        if self.pos_x == target_pixel_x and self.pos_y == target_pixel_y:
            self.current_grid_cell = self.target_grid_cell
    
    def follow_path(self, maze):
        """The Manager: Feed the next cell to the Legs."""
        # If path is empty, ask the Brain for new path:
        if not self.path:
            self.calculate_path(maze)

        # Pop the first step and make it the target:
        if self.path:
            self.target_grid_cell = self.path.pop(0)
    
    def calculate_path(self, maze):
        """The Brain: Calculate path to follow based on current state."""

        # Active chase, player in sight:
        if self.state == ScarecrowState.CHASE and self.target_player_position:
            self.speed = SCARECROW_CHASE_SPEED
            self.path = calculate_astar(maze.grid, self.current_grid_cell, self.target_player_position)
        
        # Investigate new glow stick:
        elif self.state == ScarecrowState.INVESTIGATE and self.target_glow_stick_position:
            self.speed = SCARECROW_RUN_SPEED
            self.path = calculate_astar(maze.grid, self.current_grid_cell, self.target_glow_stick_position)

            # Go back to wandering after finding glow stick:
            if self.current_grid_cell == self.target_glow_stick_position:
                self.state = ScarecrowState.WANDER
                self.target_glow_stick_position = None # Clear memory
        
        # Wandering:
        elif self.state == ScarecrowState.WANDER:
            self.speed = SCARECROW_SPEED
            
            next_cell = self.calculate_wander_move(maze)
            if next_cell:
                self.path.append(next_cell)

    def calculate_wander_move(self, maze):
        current_grid_x, current_grid_y = self.current_grid_cell
        walls_bitmask = maze.grid[current_grid_y][current_grid_x]

        valid_moves = []
        if not (walls_bitmask & N): valid_moves.append((N, current_grid_x, current_grid_y - 1))
        if not (walls_bitmask & S): valid_moves.append((S, current_grid_x, current_grid_y + 1))
        if not (walls_bitmask & W): valid_moves.append((W, current_grid_x - 1, current_grid_y))
        if not (walls_bitmask & E): valid_moves.append((E, current_grid_x + 1, current_grid_y))

        # No random backtracking, only if dead-end is reached:
        if len(valid_moves) > 1 and self.last_direction_moved:
            last_direction = self.opposite_directions[self.last_direction_moved]

            valid_moves = [move for move in valid_moves if move[0] != last_direction]
        
        # Pick next cell to move to:
        if valid_moves:
            chosen_direction, next_x, next_y = random.choice(valid_moves)
            self.last_direction_moved = chosen_direction
            
            return (next_x, next_y)
        
        return None

    def investigate_glow_stick(self, grid_position):
        """Called by main.py when a glow stick is dropped."""
        
        self.state = ScarecrowState.INVESTIGATE
        self.target_glow_stick_position = grid_position
        self.path.clear() # Stop whatever we're doing to go investigate.