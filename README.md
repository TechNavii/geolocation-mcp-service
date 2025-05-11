# Space Invaders Reimagined

A modern take on the classic Space Invaders game using Python and Pygame. This version features neon aesthetics, procedural animation, and particle effects - all generated entirely in code without external assets.

## Features

- **Pure Code Generation**: All graphics are drawn with Pygame shapes - no external sprites or images
- **Neon Visual Style**: Vibrant color palette (#FF3CAC, #2E3192, #4BCBFC, #F9F871)
- **Parallax Starfield**: Dynamic star background with depth-based movement
- **Particle Effects**: Explosions, impacts, and other visual flourishes
- **Procedural Animation**: Smooth, varied movements for all game elements
- **Screen Shake**: Adds impact when the player gets hit
- **Increasing Difficulty**: Aliens speed up as their numbers decrease
- **Level Progression**: With escalating challenges

## Requirements

- Python 3.x
- Pygame

## Installation

1. Ensure you have Python 3.x installed
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Clone or download this repository

## How to Play

Run the game with:

```bash
python main.py
```

### Controls

- **←** or **A**: Move left
- **→** or **D**: Move right
- **SPACE**: Shoot (in game) / Start (menu) / Resume (pause)
- **ESC**: Pause (in game) / Quit (menu/pause)

## Game Structure

The code is organized into modular components:

- `main.py`: Core game loop and state management
- `constants.py`: Game constants and configuration
- `entities/`
  - `player.py`: Player ship and controls
  - `aliens.py`: Alien enemies and fleet management
  - `projectiles.py`: Lasers and projectiles
- `utils/`
  - `particles.py`: Particle system for effects
  - `starfield.py`: Background starfield with parallax

## Implementation Details

- All graphics are procedurally drawn using pygame.draw.*
- No external assets (images, sounds, fonts) are used
- Ship and alien designs use basic shapes with glow effects
- Animation uses mathematical easing functions
- Collision detection uses pygame.Rect for efficiency
# test_remote_agent
