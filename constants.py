# Grid size is a prime number to
# ensure the starting window size
# doesn't clip the edge of the screen:
GRID_SIZE = 19 # A 19x19 grid.
TILE_SIZE = 16

MAZE_HEIGHT = GRID_SIZE * TILE_SIZE
MAZE_WIDTH = GRID_SIZE * TILE_SIZE
SIDEBAR_WIDTH = 4 * TILE_SIZE

LOGICAL_SCREEN_WIDTH = MAZE_WIDTH + SIDEBAR_WIDTH
LOGICAL_SCREEN_HEIGHT = MAZE_HEIGHT

FPS = 60

# Colors:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SIDEBAR_COLOR = (30, 30, 30)

# Bitmask constants for walls. Similar to Linux file permissions.
N = 1  # 0001 (North/Top)
S = 2  # 0010 (South/Bottom)
W = 4  # 0100 (West/Left)
E = 8  # 1000 (East/Right)