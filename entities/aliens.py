"""
Alien enemy classes for Space Invaders game.
"""

import pygame
import random
import math
import sys
sys.path.append('/Users/tooru/Desktop/claude_test/space_invaders')
from constants import *
from entities.projectiles import AlienLaser

class Alien:
    """Enemy alien ship."""
    
    def __init__(self, x: float, y: float, alien_type: int, row: int, col: int):
        """
        Initialize an alien at the given position.
        
        Args:
            x, y: Starting position (center of the alien)
            alien_type: Type of alien (0, 1, 2 for different designs)
            row, col: Grid position for reference
        """
        self.x = x
        self.y = y
        self.type = alien_type
        self.row = row
        self.col = col
        
        # Different sizes and colors based on type
        if alien_type == 0:  # Top row, smallest
            self.width = 24
            self.height = 24
            self.color = NEON_PINK
            self.points = 30
        elif alien_type == 1:  # Middle rows
            self.width = 28
            self.height = 28
            self.color = NEON_YELLOW
            self.points = 20
        else:  # Bottom rows, largest
            self.width = 32
            self.height = 32
            self.color = NEON_CYAN
            self.points = 10
        
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, 
                               self.width, self.height)
        self.active = True
        
        # For animation
        self.anim_state = 0
        self.anim_timer = 0
        self.anim_period = 0.5  # Seconds per frame
    
    def update(self, dt: float, current_time: float, offset_x: float, offset_y: float):
        """
        Update alien position and animation state.
        
        Args:
            dt: Time delta in seconds
            current_time: Current game time
            offset_x, offset_y: Position offsets for the entire fleet
        """
        # Update animation state
        self.anim_timer += dt
        if self.anim_timer >= self.anim_period:
            self.anim_timer -= self.anim_period
            self.anim_state = (self.anim_state + 1) % 2
        
        # Update position with fleet offset plus a slight bob motion
        bob_y = math.sin(current_time * 2 + self.col * 0.3) * 5
        self.x = self.col * 50 + 100 + offset_x
        self.y = self.row * 50 + 80 + offset_y + bob_y
        
        # Update rectangle position
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2
    
    def draw(self, surface: pygame.Surface, current_time: float):
        """
        Draw the alien to the given surface.
        
        Args:
            surface: Surface to draw on
            current_time: Current game time for visual effects
        """
        if not self.active:
            return
        
        # Base shape changes with animation state
        if self.type == 0:  # Top row - circular with antennas
            # Main body
            pygame.draw.circle(surface, self.color, (self.x, self.y), self.width // 2)
            
            # Antennas
            antenna_spread = self.width * 0.4
            if self.anim_state == 0:
                antenna_height = self.height * 0.5
            else:
                antenna_height = self.height * 0.4
            
            pygame.draw.line(surface, self.color, 
                           (self.x - antenna_spread, self.y), 
                           (self.x - antenna_spread, self.y - antenna_height), 2)
            pygame.draw.line(surface, self.color, 
                           (self.x + antenna_spread, self.y), 
                           (self.x + antenna_spread, self.y - antenna_height), 2)
            
            # Eyes
            eye_spread = self.width * 0.25
            pygame.draw.circle(surface, BLACK, 
                              (self.x - eye_spread, self.y - self.height * 0.1), 
                              self.width * 0.1)
            pygame.draw.circle(surface, BLACK, 
                              (self.x + eye_spread, self.y - self.height * 0.1), 
                              self.width * 0.1)
        
        elif self.type == 1:  # Middle rows - square with limbs
            # Main body
            pygame.draw.rect(surface, self.color, 
                           (self.x - self.width // 2, self.y - self.height // 2, 
                            self.width, self.height))
            
            # Limbs
            limb_width = self.width * 0.6
            limb_height = self.height * 0.2
            
            if self.anim_state == 0:
                limb_angle = 30  # Degrees
            else:
                limb_angle = -30
            
            # Convert limb_angle to radians
            limb_rad = math.radians(limb_angle)
            
            # Left limb coordinates
            x1 = self.x - self.width // 2
            y1 = self.y
            x2 = x1 - limb_width * math.cos(limb_rad)
            y2 = y1 + limb_width * math.sin(limb_rad)
            
            # Right limb coordinates
            x3 = self.x + self.width // 2
            y3 = self.y
            x4 = x3 + limb_width * math.cos(limb_rad)
            y4 = y3 + limb_width * math.sin(limb_rad)
            
            pygame.draw.line(surface, self.color, (x1, y1), (x2, y2), 3)
            pygame.draw.line(surface, self.color, (x3, y3), (x4, y4), 3)
            
            # Eyes
            eye_spread = self.width * 0.25
            pygame.draw.circle(surface, BLACK, 
                              (self.x - eye_spread, self.y - self.height * 0.2), 
                              self.width * 0.1)
            pygame.draw.circle(surface, BLACK, 
                              (self.x + eye_spread, self.y - self.height * 0.2), 
                              self.width * 0.1)
        
        else:  # Bottom rows - octagon
            # For the octagon, calculate 8 points around the center
            points = []
            for i in range(8):
                angle = math.pi / 8 + i * math.pi / 4
                if self.anim_state == 0:
                    radius = self.width * 0.5
                else:
                    # Slightly pulsing radius
                    radius = self.width * 0.45
                
                px = self.x + radius * math.cos(angle)
                py = self.y + radius * math.sin(angle)
                points.append((px, py))
            
            pygame.draw.polygon(surface, self.color, points)
            
            # Eyes
            eye_spread = self.width * 0.25
            pygame.draw.circle(surface, BLACK, 
                              (self.x - eye_spread, self.y - self.height * 0.1), 
                              self.width * 0.1)
            pygame.draw.circle(surface, BLACK, 
                              (self.x + eye_spread, self.y - self.height * 0.1), 
                              self.width * 0.1)
        
        # Add a glow effect for all types
        s = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        
        # Glow effect shape follows main body shape
        if self.type == 0:  # Circle
            pygame.draw.circle(s, (*self.color[:3], 100), 
                              (self.width // 2 + 5, self.height // 2 + 5), 
                              self.width // 2 + 3)
        elif self.type == 1:  # Square
            pygame.draw.rect(s, (*self.color[:3], 100), 
                            (5, 5, self.width, self.height), 
                            border_radius=3)
        else:  # Octagon
            glow_points = []
            for i in range(8):
                angle = math.pi / 8 + i * math.pi / 4
                radius = self.width * 0.5 + 3
                px = self.width // 2 + 5 + radius * math.cos(angle)
                py = self.height // 2 + 5 + radius * math.sin(angle)
                glow_points.append((px, py))
            
            pygame.draw.polygon(s, (*self.color[:3], 100), glow_points)
        
        surface.blit(s, (self.x - self.width // 2 - 5, self.y - self.height // 2 - 5))


class AlienFleet:
    """Manages a grid of aliens."""
    
    def __init__(self, rows: int = 5, cols: int = 11):
        """
        Initialize a fleet of aliens in a grid pattern.
        
        Args:
            rows: Number of rows in the fleet
            cols: Number of columns in the fleet
        """
        self.rows = rows
        self.cols = cols
        self.aliens = []
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 30  # Horizontal speed in pixels per second
        self.descent_step = 20  # Pixels to move down when hitting edge
        self.offset_x = 0
        self.offset_y = 0
        self.move_timer = 0
        self.move_interval = 0.02  # Seconds per movement step
        self.aliens_destroyed = 0
        self.lasers = []
        self.shoot_timer = 0
        self.shoot_interval = 1.0  # Seconds between alien shots
        self.shoot_chance = 0.3  # Probability of an alien shooting per interval
        self.difficulty_factor = 1.0
        
        # Initialize the fleet
        self.create_fleet()
    
    def create_fleet(self):
        """Create the initial grid of aliens."""
        self.aliens = []
        self.offset_x = 0
        self.offset_y = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                # Determine alien type (0 = top row, 1 = middle rows, 2 = bottom rows)
                if row == 0:
                    alien_type = 0
                elif row < 3:
                    alien_type = 1
                else:
                    alien_type = 2
                
                # Create alien at grid position
                x = col * 50 + 100
                y = row * 50 + 80
                alien = Alien(x, y, alien_type, row, col)
                self.aliens.append(alien)
    
    def update(self, dt: float, current_time: float):
        """
        Update fleet position and state.
        
        Args:
            dt: Time delta in seconds
            current_time: Current game time
        """
        # Only move at specific intervals for that classic step motion
        self.move_timer += dt
        
        if self.move_timer >= self.move_interval:
            self.move_timer -= self.move_interval
            
            # Move horizontally
            self.offset_x += self.direction * self.speed * self.move_interval
            
            # Check if fleet has reached screen edge
            if self.aliens:  # Only check if there are aliens left
                leftmost_x = min(alien.x for alien in self.aliens if alien.active)
                rightmost_x = max(alien.x for alien in self.aliens if alien.active)
                
                if rightmost_x >= WIDTH - 30 and self.direction > 0:
                    self.direction = -1
                    self.offset_y += self.descent_step
                elif leftmost_x <= 30 and self.direction < 0:
                    self.direction = 1
                    self.offset_y += self.descent_step
        
        # Update all active aliens
        for alien in self.aliens:
            if alien.active:
                alien.update(dt, current_time, self.offset_x, self.offset_y)
        
        # Update alien lasers
        for laser in self.lasers[:]:
            laser.update(dt, current_time)
            if not laser.active:
                self.lasers.remove(laser)
        
        # Try to shoot
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            self.try_shoot(current_time)
        
        # Adjust difficulty based on remaining aliens
        active_aliens = sum(1 for alien in self.aliens if alien.active)
        if active_aliens > 0:
            self.difficulty_factor = 1.0 + (1.0 - active_aliens / (self.rows * self.cols)) * 0.5
            
            # Speed up as fewer aliens remain
            self.move_interval = max(0.01, 0.02 / self.difficulty_factor)
            self.shoot_interval = max(0.3, 1.0 / self.difficulty_factor)
    
    def try_shoot(self, current_time: float):
        """
        Try to have a random alien shoot.
        
        Args:
            current_time: Current game time
        """
        # Get all active aliens
        active_aliens = [alien for alien in self.aliens if alien.active]
        if not active_aliens:
            return
        
        # Adjust shoot chance based on difficulty
        adjusted_chance = self.shoot_chance * self.difficulty_factor
        
        # Randomly decide whether to shoot
        if random.random() < adjusted_chance:
            # Select a random alien from bottom rows when possible
            # (aliens that don't have other aliens below them)
            bottom_aliens = {}
            
            # For each column, find the bottom-most active alien
            for alien in active_aliens:
                col = alien.col
                if col not in bottom_aliens or alien.row > bottom_aliens[col].row:
                    bottom_aliens[col] = alien
            
            if bottom_aliens:
                # Randomly select one of the bottom aliens
                shooter = random.choice(list(bottom_aliens.values()))
                self.lasers.append(AlienLaser(shooter.x, shooter.y + shooter.height // 2))
    
    def check_collision(self, laser):
        """
        Check if a player laser collides with any alien.
        
        Args:
            laser: Player laser to check against
            
        Returns:
            Alien: The alien that was hit, or None if no collision
        """
        for alien in self.aliens:
            if alien.active and laser.rect.colliderect(alien.rect):
                return alien
        return None
    
    def draw(self, surface: pygame.Surface, current_time: float):
        """
        Draw all active aliens and their lasers.
        
        Args:
            surface: Surface to draw on
            current_time: Current game time for visual effects
        """
        # Draw aliens
        for alien in self.aliens:
            if alien.active:
                alien.draw(surface, current_time)
        
        # Draw lasers
        for laser in self.lasers:
            laser.draw(surface, current_time)
    
    def reset(self):
        """Reset the alien fleet to initial state."""
        self.create_fleet()
        self.lasers = []
        self.aliens_destroyed = 0
        self.difficulty_factor = 1.0
        self.shoot_timer = 0
        self.move_timer = 0
    
    def all_destroyed(self):
        """Check if all aliens have been destroyed."""
        return all(not alien.active for alien in self.aliens)
