from enum import Enum

class GameState(Enum):
    START_MENU = 0
    PLAYING = 1
    PAUSED_MENU = 2
    STORY_SCREEN = 3
    CONTROLS_SCREEN = 4
    ENTER_SEED_SCREEN = 5
    CURRENT_SEED_SCREEN = 6
    RESULTS_SCREEN = 7

# Grid size is a prime number to
# ensure the starting window size
# doesn't clip the edge of the screen:
GRID_SIZE = 19 # A 19x19 grid.
TILE_SIZE = 16

MAZE_HEIGHT = GRID_SIZE * TILE_SIZE
MAZE_WIDTH = GRID_SIZE * TILE_SIZE
SIDEBAR_WIDTH = 7 * TILE_SIZE

LOGICAL_SCREEN_WIDTH = MAZE_WIDTH + SIDEBAR_WIDTH
LOGICAL_SCREEN_HEIGHT = MAZE_HEIGHT

FPS = 60

# Colors:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SIDEBAR_COLOR = (30, 30, 30)
CORN_WALL_COLOR = (180, 160, 50)

# Bitmask constants for walls. Similar to Linux file permissions.
N = 1  # 0001 (North/Top)
S = 2  # 0010 (South/Bottom)
W = 4  # 0100 (West/Left)
E = 8  # 1000 (East/Right)

# Speed settings:
PLAYER_SPEED = 1.2
PLAYER_RUN_SPEED = 2.4

MAX_STAMINA = 100
STAMINA_DECAY = 0.5
STAMINA_REGEN = 0.25

SCARECROW_SPEED = 0.6
SCARECROW_RUN_SPEED = 1.6
SCARECROW_CHASE_SPEED = 2.0

SCARECROW_DETECTION_RADIUS = 2 * TILE_SIZE
SCARECROW_MEMORY_LENGTH = 3000 # milliseconds

INITIAL_GLOW_STICKS = 10

GRACE_PERIOD = 15
GRACE_GLOW_STICKS_AMOUNT = 5

SMALL_FONT_PATH = "m5x7.ttf"
LARGE_FONT_PATH = "m6x11.ttf"

STORY_PAGES = [
    "You were making record time at the Miller Farm's annual corn maze contest, when all of a sudden you tripped over a rogue pumpkin, and the world went to black.",
    "When you awaken, you are greeted by nightfall. Not only is it pitch black, you soon realize the map you made is useless as you keep stumbling into corn stalks.",
    "The wind suddenly stops, and an eerie sound whistles through the dry husks. A pit develops in your stomach, and you understand now that the legend is true.",
    "The Miller Farm is home to a supernatural guardian scarecrow that patrols its fields. If it finds you, you'll never see another sunrise.",
    "Your only hope of survival is to take refuge in the lookout tower, if only you can navigate through the dark labyrinth of green and yellow.",
    "It dawns on you, your backpack is full of industrial-grade, white, neon glow sticks. They are very bright, but they also attract unwanted attention.",
    "Cautiously using your glow sticks to help guide you, avoid the paranormal sentinel, and find your way to the lookout tower in the Midnight Maize."
    ]

PLAYER_LIGHT_RADIUS = TILE_SIZE * 4
GLOW_STICK_LIGHT_RADIUS = TILE_SIZE * 3