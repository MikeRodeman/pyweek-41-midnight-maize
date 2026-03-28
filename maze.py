import pygame
import random
import collections
from constants import *

class Maze:
    def __init__(self, seed=None):
        # The maze is described with a 2D list of integers between 0 and 15.
        # The integers represent the walls of each cell in the grid, like
        # how Linux file permission numbers work. It's called a 4-bit bitmask.
        #
        # 1 (0001) = North, 2 (0010) = East, 4 (0100) = South, 8 (1000) = West.
        self.grid = [[15 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # If no player doesn't give a seed, generate a random one:
        if not seed:
            self.seed = str(random.randint(1000000, 9999999))
        else:
            self.seed = str(seed)

        self.rng = random.Random(self.seed)

        # The bit values for the directions, with their dx and dy:
        self.directions = [(N, 0, -1), (S, 0, 1), (W, -1, 0), (E, 1, 0)]

        # When we knock a wall down in a cell to carve a path to another cell,
        # we also need to knock the wall down in that other cell:
        self.opposite = {N: S, S: N, W: E, E: W}

        self.generate()
        self.find_starting_positions()
        self.create_wall_rects()
    
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
    
    def find_starting_positions(self):
        # The player starts somewhere completely random:
        player_x = self.rng.randint(0, GRID_SIZE - 1)
        player_y = self.rng.randint(0, GRID_SIZE - 1)
        self.player_starting_position = (player_x, player_y)

        # Use breadth-first search to find the furthest cell from the
        # player. This will be the position of the lookout tower.

        # Keep track of the cells we need to check with their distances
        # from the player:
        queue = collections.deque([(self.player_starting_position, 0)])

        # Keep track of the cells we've visited already:
        visited = {self.player_starting_position}

        # Keep track of the furthest cell we find:
        furthest_cell_from_player = self.player_starting_position
        max_distance_from_player = 0

        # Use a dictionary to keep track of the distance between
        # the player and every cell:
        self.distances_from_player = {self.player_starting_position: 0}

        # Breadth-first search "flooding" the grid until no cells left:
        while queue:
            # Pop the oldest cell from the front of the queue:
            current_cell, current_distance_from_player = queue.popleft()
            current_x, current_y = current_cell

            # Keep track of furthest found so far:
            if current_distance_from_player > max_distance_from_player:
                max_distance_from_player = current_distance_from_player
                furthest_cell_from_player = current_cell
            
            # The wall data for the current cell:
            current_walls = self.grid[current_y][current_x]

            # Look in all 4 directions (N, E, S, W):
            for direction_bit, dx, dy in self.directions:

                # Do bitwise AND. If it's not 0, then that means there
                # isn't a wall in that direction, which means the path
                # is open in that direction:
                if not (current_walls & direction_bit):
                    neighbor_x = current_x + dx
                    neighbor_y = current_y + dy
                    neighbor_cell = (neighbor_x, neighbor_y)

                    # If we haven't visited/flooded into this
                    # cell already, move into it:
                    if neighbor_cell not in visited:
                        visited.add(neighbor_cell)
                        neighbor_distance = current_distance_from_player + 1

                        # Keep track of distance in order to calculate scarecrow starting position:
                        self.distances_from_player[neighbor_cell] = neighbor_distance

                        # Add to the back of the queue to check it later:
                        queue.append((neighbor_cell, neighbor_distance))
        
        # The lookout tower is positioned at the furthest cell:
        self.lookout_tower_position = furthest_cell_from_player

        # The scarecrow needs to span somewhere in the "middle" of the path
        # between the player and the lookout tower:
        min_scarecrow_distance_from_player = max_distance_from_player * 0.30
        max_scarecrow_distance_from_player = max_distance_from_player * 0.70

        #Find all the cells satisfying this requirement:
        possible_scarecrow_starting_positions = []
        
        for cell, distance_from_player in self.distances_from_player.items():
            if min_scarecrow_distance_from_player <= distance_from_player <= max_scarecrow_distance_from_player:
                possible_scarecrow_starting_positions.append(cell)
        
        # Randomly pick one of the possible cells for the scarecrow's starting position:
        # (The conditional is a future-proof for custom tiny grid sizes where mid-range
        # positions might not exist.)
        if possible_scarecrow_starting_positions:
            self.scarecrow_starting_position = self.rng.choice(possible_scarecrow_starting_positions)
        else:
            self.scarecrow_starting_position = furthest_cell_from_player
    
    def create_wall_rects(self):
        # Make dictionary to track the wall rects each grid cell has:
        self.wall_rects = collections.defaultdict(list)
        thickness = 4

        # Make 4 large rects for the borders:
        north_border = pygame.Rect(0, 0, MAZE_WIDTH, thickness // 2)
        south_border = pygame.Rect(0, MAZE_HEIGHT - thickness // 2, MAZE_WIDTH, thickness // 2)
        west_border = pygame.Rect(0, 0, thickness // 2, MAZE_HEIGHT)
        east_border = pygame.Rect(MAZE_WIDTH - thickness // 2, 0, thickness // 2, MAZE_HEIGHT)

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if y == 0:
                    self.wall_rects[(x, y)].append(north_border)
                elif y == GRID_SIZE - 1:
                    self.wall_rects[(x, y)].append(south_border)
                
                if x == 0:
                    self.wall_rects[(x, y)].append(west_border)
                elif x == GRID_SIZE - 1:
                    self.wall_rects[(x, y)].append(east_border)

                # Get the wall bitmask for the current cell:
                walls_bitmask = self.grid[y][x]

                # Coordinates of the cell corners:
                left_x = x * TILE_SIZE
                top_y = y * TILE_SIZE

                # We only need to check the South and East walls for each cell, because the
                # North and West walls will be the South and West walls for a neighboring cell:
                if walls_bitmask & S:
                    self.wall_rects[(x, y)].append(pygame.Rect(left_x, top_y + TILE_SIZE - thickness // 2, TILE_SIZE, thickness))
                if walls_bitmask & E:
                    self.wall_rects[(x, y)].append(pygame.Rect(left_x + TILE_SIZE - thickness // 2, top_y, thickness, TILE_SIZE))

    def draw(self, surface):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                # Get the wall bitmask for the current cell:
                walls_bitmask = self.grid[y][x]

                # Coordinates of the cell corners:
                left_x = x * TILE_SIZE
                top_y = y * TILE_SIZE
                right_x = left_x + TILE_SIZE
                bottom_y = top_y + TILE_SIZE

                # We only need to check the South and East walls for each cell, because the
                # North and West walls will be the South and West walls for a neighboring cell:
                if walls_bitmask & S or y == GRID_SIZE - 1:

                    # Correct for 0-indexing mismatch on the last pixel.
                    # A window N pixels wide has indices 0 to N - 1, not N:
                    draw_y = min(bottom_y, MAZE_HEIGHT - 1)
                    pygame.draw.line(surface, WHITE, (left_x, draw_y), (right_x, draw_y))
                if walls_bitmask & E or x == GRID_SIZE - 1:
                    draw_x = min(right_x, MAZE_WIDTH - 1)
                    pygame.draw.line(surface, WHITE, (draw_x, top_y), (draw_x, bottom_y))

                # Draw the North and West borders:
                if y == 0: # North
                    pygame.draw.line(surface, WHITE, (left_x, top_y), (right_x, top_y))
                if x == 0: # West
                    pygame.draw.line(surface, WHITE, (left_x, top_y), (left_x, bottom_y))
