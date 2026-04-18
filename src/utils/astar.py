import heapq

import src.core.constants as c
from src.core.custom_types import Coordinate

def calculate_astar(
    maze_grid: list[list[int]],
    start_cell: Coordinate,
    goal_cell: Coordinate
    ) -> list[Coordinate]:
    
    # Keep track of cells we've seen but haven't explored yet:
    to_visit_list: list[Coordinate] = []

    # Store tuples: (priority_score, (x, y))
    heapq.heappush(to_visit_list, (0, start_cell))

    # A dictionary to keep track of our path:
    # trail_map[current cell] = where we came from
    trail_map: dict[Coordinate, Coordinate] = {}

    # How far we've traveled from start to current cell:
    steps_so_far: dict[Coordinate, int] = {start_cell: 0}

    # Priority score combining steps so far with a distance guess heuristic:
    total_priority_score: dict[Coordinate, int] = {start_cell: get_manhattan_distance(start_cell, goal_cell)}

    while to_visit_list:
        current_cell = heapq.heappop(to_visit_list)[1]

        # Reached target:
        if current_cell == goal_cell:
            return reconstruct_path(trail_map, current_cell)
    
        # Get the walls in the current cell:
        current_x, current_y = current_cell
        walls_bitmask = maze_grid[current_y][current_x]

        # Check each direction:
        for direction, dx, dy in [(c.N, 0, -1), (c.S, 0, 1), (c.W, -1, 0), (c.E, 1, 0)]:
            if not (walls_bitmask & direction):
                neighbor = (current_x + dx, current_y + dy)

                # Each step in the maze costs 1 unit of distance:
                tentative_steps = steps_so_far[current_cell] + 1

                # If this is a new cell or a faster way to reach a known cell:
                if neighbor not in steps_so_far or tentative_steps < steps_so_far[neighbor]:
                    # Keep track of our trail:
                    trail_map[neighbor] = current_cell

                    # Update:
                    steps_so_far[neighbor] = tentative_steps

                    # Calculate heuristic guess:
                    distance_guess = get_manhattan_distance(neighbor, goal_cell)

                    # The priority score that's actually used to calculate path:
                    priority_score = tentative_steps + distance_guess
                    total_priority_score[neighbor] = priority_score

                    # Add to our to visit list:
                    heapq.heappush(to_visit_list, (priority_score, neighbor))
    
    return [] # Means scarecrow is trapped somehow

def get_manhattan_distance(cell_a: Coordinate, cell_b: Coordinate) -> int:
    return abs(cell_a[0] - cell_b[0]) + abs(cell_a[1] - cell_b[1])

def reconstruct_path(
    trail_map: dict[Coordinate, Coordinate],
    current_cell: Coordinate
    ) -> list[Coordinate]:
    
    path = []
    while current_cell in trail_map:
        path.append(current_cell)
        current_cell = trail_map[current_cell]
    
    path.reverse() # Reverse so it goes from start to goal

    return path