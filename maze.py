import pygame
import random
from constants import *

class Maze:
    def __init__(self, seed_value=None):
        # The maze is described with a 2D list of integers between 0 and 15.
        # The integers represent the walls of each cell in the grid, like
        # how Linux file permission numbers work. It's called a 4-bit bitmask.
        #
        # 1 (0001) = North, 2 (0010) = East, 4 (0100) = South, 8 (1000) = West.
        self.grid = [[15 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # If no player doesn't give a seed, generate a random one:
        if not seed_value:
            self.seed_value = str(random.randint(1000000, 9999999))
        else:
            self.seed_value = str(seed_value)

        self.rng = random.Random(self.seed_value)

        # The bit values for the directions, with their dx and dy:
        self.directions = [(N, 0, -1), (E, 1, 0), (S, 0, 1), (W, -1, 0)]

        # When we knock a wall down in a cell to carve a path to another cell,
        # we also need to knock the wall down in that other cell:
        self.opposite = {N: S, S: N, E: W, W: E}

        self.generate()
    
    def generate(self):
        # Pick random starting point for the generation:
        start_x = self.rng.randint(0, GRID_SIZE - 1)
        start_y = self.rng.randint(0, GRID_SIZE - 1)
        start_cell = (start_x, start_y)

        # Start a ball of yarn to keep track of the current path we're on:
        stack = [start_cell]

        # Keep track of the grid cells we've visited already:
        visited = {start_cell}

        # If the length of our yarn is more than 0, that means we're
        # still able to either continue ahead to new unvisited cells,
        # or backtrack to skipped unvisited cells:
        while stack:
            current_x, current_y = stack[-1]

            unvisited_neighbors = []

            # Check all 4 directions (North, East, South, West):
            for direction_bit, dx, dy in self.directions:
                neighbor_x = current_x + dx
                neighbor_y = current_y + dy
            
                is_inside_grid = 0 <= neighbor_x < GRID_SIZE and 0 <= neighbor_y < GRID_SIZE

                if is_inside_grid and (neighbor_x, neighbor_y) not in visited:
                    unvisited_neighbors.append((direction_bit, neighbor_x, neighbor_y))
            
            if unvisited_neighbors:
                # Pick a random unvisited neighboring cell:
                chosen_direction, neighbor_x, neighbor_y = self.rng.choice(unvisited_neighbors)

                # "Break" the wall connecting the current cell to the new cell. Since we're using a
                # bitmask, we can do this by just subtracting the number representing that direction:
                self.grid[current_y][current_x] -= chosen_direction

                # We also need to break the corresponding wall facing towards us in the new cell:
                self.grid[neighbor_y][neighbor_x] -= self.opposite[chosen_direction]

                # Keep track of the new cell as visited:
                visited.add((neighbor_x, neighbor_y))

                # Lay down our yarn more:
                stack.append((neighbor_x, neighbor_y))
            
            else:
                # If none of the neighbors are unvisited, that means we hit a dead end.
                # Pick up our yarn and backtrack:
                stack.pop()

    def draw(self, surface):
        # Draw a skeleton of the path of the maze:
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                center_x = x * TILE_SIZE + TILE_SIZE // 2
                center_y = y * TILE_SIZE + TILE_SIZE // 2

                pygame.draw.circle(surface, WHITE, (center_x, center_y), 3)

                val = self.grid[y][x]

                if not (val & E):
                    neighbor_center_x = (x + 1) * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.line(surface, WHITE, (center_x, center_y), (neighbor_center_x, center_y))
                
                if not (val & S):
                    neighbor_center_y = (y + 1) * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.line(surface, WHITE, (center_x, center_y), (center_x, neighbor_center_y))