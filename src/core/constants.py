from enum import Enum
from pathlib import Path
from typing import Final

from pygame.typing import ColorLike

# --------------------------------------------------------------------------
# PATHS
# --------------------------------------------------------------------------

ROOT_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent

# Asset Folders:
GRAPHICS_DIR: Final[Path] = ROOT_DIR / "assets" / "graphics"
FONTS_DIR: Final[Path] = ROOT_DIR / "assets" / "fonts"
DATA_DIR: Final[Path] = ROOT_DIR / "assets" / "data"

# Source Folders:
CORE_DIR: Final[Path] = ROOT_DIR / "src" / "core"
ENTITIES_DIR: Final[Path] = ROOT_DIR / "src" / "entities"
UI_DIR: Final[Path] = ROOT_DIR / "src" / "ui"
UTILS_DIR: Final[Path] = ROOT_DIR / "src" / "utils"

# Specific Files:
STORY_PATH: Final[Path] = DATA_DIR / "story.txt"
SMALL_FONT_PATH: Final[Path] = FONTS_DIR / "m5x7.ttf"
LARGE_FONT_PATH: Final[Path] = FONTS_DIR / "m6x11.ttf"

# --------------------------------------------------------------------------
# GAME STATES
# --------------------------------------------------------------------------

class GameState(Enum):
    START_MENU = 0
    PLAYING = 1
    PAUSED_MENU = 2
    STORY_SCREEN = 3
    CONTROLS_SCREEN = 4
    ENTER_SEED_SCREEN = 5
    CURRENT_SEED_SCREEN = 6
    RESULTS_SCREEN = 7

# --------------------------------------------------------------------------
# GRID AND DISPLAY SETTINGS
# --------------------------------------------------------------------------

FPS: Final[int] = 60

GRID_SIZE: Final[int] = 19 # Prime number to prevent clipping on edge of screen
TILE_SIZE: Final[int] = 16

MAZE_HEIGHT: Final[int] = GRID_SIZE * TILE_SIZE
MAZE_WIDTH: Final[int] = GRID_SIZE * TILE_SIZE
SIDEBAR_WIDTH: Final[int] = 7 * TILE_SIZE

LOGICAL_SCREEN_WIDTH: Final[int] = MAZE_WIDTH + SIDEBAR_WIDTH
LOGICAL_SCREEN_HEIGHT: Final[int] = MAZE_HEIGHT

# --------------------------------------------------------------------------
# MAZE LOGIC
# --------------------------------------------------------------------------

# Bitmask constants for walls. Similar to Linux file permissions.
N: Final[int] = 1  # 0001 (North/Top)
S: Final[int] = 2  # 0010 (South/Bottom)
W: Final[int] = 4  # 0100 (West/Left)
E: Final[int] = 8  # 1000 (East/Right)

# --------------------------------------------------------------------------
# PLAYER SETTINGS
# --------------------------------------------------------------------------

# Speed:
PLAYER_SPEED: Final[float] = 1.2
PLAYER_RUN_SPEED: Final[float] = 2.4

# Stamina:
MAX_STAMINA: Final[float] = 100.0
STAMINA_DECAY: Final[float] = 0.5
STAMINA_REGEN: Final[float] = 0.25

# Glowsticks:
INITIAL_GLOW_STICKS: Final[int] = 10
GRACE_GLOW_STICKS_AMOUNT: Final[int] = 5

# --------------------------------------------------------------------------
# SCARECROW SETTINGS
# --------------------------------------------------------------------------

# Speed:
SCARECROW_SPEED: Final[float] = 0.6
SCARECROW_RUN_SPEED: Final[float] = 1.6
SCARECROW_CHASE_SPEED: Final[float] = 2.0

# Detection Logic:
SCARECROW_DETECTION_RADIUS: Final[float] = 2.0 * TILE_SIZE
SCARECROW_MEMORY_LENGTH: Final[int] = 3000 # milliseconds

# Time until chase starts:
GRACE_PERIOD: Final[int] = 15 # seconds

# --------------------------------------------------------------------------
# VISUALS AND LIGHTING
# --------------------------------------------------------------------------

# Colors:
BLACK: Final[ColorLike] = (0, 0, 0)
WHITE: Final[ColorLike] = (255, 255, 255)
SIDEBAR_COLOR: Final[ColorLike] = (30, 30, 30)
CORN_WALL_COLOR: Final[ColorLike] = (180, 160, 50)

# Light Radii:
PLAYER_LIGHT_RADIUS: Final[float] = TILE_SIZE * 4.0
GLOW_STICK_LIGHT_RADIUS: Final[float] = TILE_SIZE * 3.0

# --------------------------------------------------------------------------
# STATIC TEXT DATA
# --------------------------------------------------------------------------

STORY_PAGES: Final[list[str]] = [
    "You were making record time at the Miller Farm's annual corn maze contest, when all of a sudden you tripped over a rogue pumpkin, and the world went to black.",
    "When you awaken, you are greeted by nightfall. Not only is it pitch black, you soon realize the map you made is useless as you keep stumbling into corn stalks.",
    "The wind suddenly stops, and an eerie sound whistles through the dry husks. A pit develops in your stomach, and you understand now that the legend is true.",
    "The Miller Farm is home to a supernatural guardian scarecrow that patrols its fields. If it finds you, you'll never see another sunrise.",
    "Your only hope of survival is to take refuge in the lookout tower, if only you can navigate through the dark labyrinth of green and yellow.",
    "It dawns on you, your backpack is full of industrial-grade, white, neon glow sticks. They are very bright, but they also attract unwanted attention.",
    "Cautiously using your glow sticks to help guide you, avoid the paranormal sentinel, and find your way to the lookout tower in the Midnight Maize."
    ]
