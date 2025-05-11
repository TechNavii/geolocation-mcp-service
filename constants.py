"""
Constants used throughout the Space Invaders game.
"""

# Screen dimensions
WIDTH = 800
HEIGHT = 600
FPS = 60

# Game states
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    HIGH_SCORE = 3
    PAUSED = 4

# Neon color palette
NEON_PINK = (255, 60, 172)      # #FF3CAC
NEON_BLUE = (46, 49, 146)       # #2E3192
NEON_CYAN = (75, 203, 252)      # #4BCBFC
NEON_YELLOW = (249, 248, 113)   # #F9F871
NEON_GREEN = (57, 255, 20)      # Custom neon green
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
