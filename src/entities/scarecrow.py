from enum import Enum
import random

import pygame

import src.core.constants as c
from src.entities.player import Player
from src.utils.astar import calculate_astar

class ScarecrowState(Enum):
    DORMANT = 0
    WANDER = 1
    INVESTIGATE = 2
    CHASE = 3
class Scarecrow(pygame.sprite.Sprite):
    def __init__(self, starting_position):
        # Call parent constructor:
        super().__init__()

        # Pixel art:
        self.image = pygame.image.load(c.GRAPHICS_DIR / "scarecrow.png").convert_alpha()

        self.rect = self.image.get_rect()

        # Set starting position:
        self.pos_x = starting_position[0] * c.TILE_SIZE + c.TILE_SIZE // 2
        self.pos_y = starting_position[1] * c.TILE_SIZE + c.TILE_SIZE // 2

        # Smaller rect for hitbox:
        self.hitbox_rect = pygame.Rect(0, 0, 8, 8)
        self.hitbox_rect.center = (int(self.pos_x), int(self.pos_y))
        
        # Line up the center of the visual rect with the center of the hitbox rect:
        self.rect.center = self.hitbox_rect.center

        self.speed = c.SCARECROW_SPEED
        self.state = ScarecrowState.WANDER

        # Logical position and movement on the grid:
        self.current_grid_cell = starting_position
        self.target_grid_cell = starting_position
        self.path = []

        # Memory so scarecrow doesn't backtrack randomly:
        self.opposite_directions = {c.N: c.S, c.S: c.N, c.W: c.E, c.E: c.W}
        self.last_direction_moved = None

        self.target_glow_stick_position = None
        self.target_player_position = None

        # Memory timer for chasing around corners:
        self.last_seen_player_time = 0
    
    def update(self, maze, player):
        # Always check if we can see the player:
        self.check_for_player(player, maze)

        # The legs - physically move:
        self.move_to_adjacent_cell_center()

        # The brain - calculate path to follow:
        if self.current_grid_cell == self.target_grid_cell:
            self.follow_path(maze)
    
    def move_to_adjacent_cell_center(self):
        """The Legs: Move rect center from current cell to the exact center of adjacent cell."""
        target_pixel_x = self.target_grid_cell[0] * c.TILE_SIZE + c.TILE_SIZE // 2
        target_pixel_y = self.target_grid_cell[1] * c.TILE_SIZE + c.TILE_SIZE // 2

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
            self.speed = c.SCARECROW_CHASE_SPEED
            self.path = calculate_astar(maze.grid, self.current_grid_cell, self.target_player_position)
        
        # Investigate new glow stick:
        elif self.state == ScarecrowState.INVESTIGATE and self.target_glow_stick_position:
            self.speed = c.SCARECROW_RUN_SPEED
            self.path = calculate_astar(maze.grid, self.current_grid_cell, self.target_glow_stick_position)

            # Go back to wandering after finding glow stick:
            if self.current_grid_cell == self.target_glow_stick_position:
                self.state = ScarecrowState.WANDER
                self.target_glow_stick_position = None # Clear memory
        
        # Wandering:
        elif self.state == ScarecrowState.WANDER:
            self.speed = c.SCARECROW_SPEED
            
            next_cell = self.calculate_wander_move(maze)
            if next_cell:
                self.path.append(next_cell)

    def calculate_wander_move(self, maze):
        current_grid_x, current_grid_y = self.current_grid_cell
        walls_bitmask = maze.grid[current_grid_y][current_grid_x]

        valid_moves = []
        if not (walls_bitmask & c.N): valid_moves.append((c.N, current_grid_x, current_grid_y - 1))
        if not (walls_bitmask & c.S): valid_moves.append((c.S, current_grid_x, current_grid_y + 1))
        if not (walls_bitmask & c.W): valid_moves.append((c.W, current_grid_x - 1, current_grid_y))
        if not (walls_bitmask & c.E): valid_moves.append((c.E, current_grid_x + 1, current_grid_y))

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

        # Ignore glow sticks if chasing the player:
        if self.state == ScarecrowState.CHASE:
            return
        
        self.state = ScarecrowState.INVESTIGATE
        self.target_glow_stick_position = grid_position
        self.path.clear() # Stop whatever we're doing to go investigate.
    
    def check_for_player(self, player, maze):
        # Proximity check ignoring walls:
        player_center_vector = pygame.math.Vector2(player.rect.center)
        scarecrow_center_vector = pygame.math.Vector2(self.rect.center)

        has_proximity = scarecrow_center_vector.distance_to(player_center_vector) < c.SCARECROW_DETECTION_RADIUS
        has_line_of_sight = self.has_line_of_sight(player, maze)

        can_see_player = has_proximity or has_line_of_sight

        # Logic for when player is seen:
        if can_see_player:
            # Update memory timer:
            self.last_seen_player_time = pygame.time.get_ticks()

            if self.state != ScarecrowState.CHASE:
                self.start_chase(player.current_grid_cell)

            elif self.target_player_position != player.current_grid_cell:
                # This means we're chasing, but player has moved to a new cell.
                # So update the target and clear the path so A* recalculates.
                self.target_player_position = player.current_grid_cell
                self.path.clear()

        # Logic for when player is not seen, i.e., player turned a corner,
        # OR, chase was started via proximity and not line of sight:
        else:
            if self.state == ScarecrowState.CHASE:
                # How long since player was seen:
                current_time = pygame.time.get_ticks()
                time_since_seen = current_time - self.last_seen_player_time

                # Give up if it's been too long, or if we reached the spot where the player was:
                if (time_since_seen > c.SCARECROW_MEMORY_LENGTH 
                    or self.current_grid_cell == self.target_player_position):
                    
                    self.state = ScarecrowState.WANDER
                    self.target_player_position = None
                    self.path.clear()
    
    def has_line_of_sight(self, player, maze):
        player_grid_x, player_grid_y = player.current_grid_cell
        scarecrow_grid_x, scarecrow_grid_y = self.current_grid_cell

        # (Note: Don't have to account for if they share both column
        # and row, because if they do then that means the scarecrow
        # caught the player and the game is already over.)

        # Check if in same column:
        if scarecrow_grid_x == player_grid_x:
            start, end = min(scarecrow_grid_y, player_grid_y), max(scarecrow_grid_y, player_grid_y)

            for y in range(start, end):
                # Check if there's a North/South wall blocking line of sight:
                if (maze.grid[y][scarecrow_grid_x] & c.S) or (maze.grid[y + 1][scarecrow_grid_x] & c.N):
                    return False
            
            return True
        
        # Check if in same row:
        if scarecrow_grid_y == player_grid_y:
            start, end = min(scarecrow_grid_x, player_grid_x), max(scarecrow_grid_x, player_grid_x)

            for x in range(start, end):
                # Check if there's a West/East wall blocking line of sight:
                if (maze.grid[scarecrow_grid_y][x] & c.E) or (maze.grid[scarecrow_grid_y][x + 1] & c.W):
                    return False
            
            return True
        
        return False
    
    def start_chase(self, player_grid_position):
        self.state = ScarecrowState.CHASE
        self.target_player_position = player_grid_position

        # Instantly increase speed:
        self.speed = c.SCARECROW_CHASE_SPEED

        # Clear path so A* recalculates toward the player's current spot:
        self.path.clear()
        