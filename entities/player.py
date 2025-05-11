"""
Player class for Space Invaders game.
"""

import pygame
import math
import random
import sys
sys.path.append('/Users/tooru/Desktop/claude_test/space_invaders')
from constants import *
from entities.projectiles import Laser

class Player:
    """Player's spaceship."""
    
    def __init__(self, x: float, y: float):
        """
        Initialize the player at the given position.
        
        Args:
            x, y: Starting position (center of the ship)
        """
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20
        self.speed = 300  # Pixels per second
        self.color = NEON_CYAN
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, 
                               self.width, self.height)
        self.shoot_cooldown = 0.25  # Seconds
        self.last_shot_time = 0
        self.lasers = []
        self.lives = 3
        self.is_hit = False
        self.hit_timer = 0
        self.hit_duration = 0.3  # Seconds
        self.shake_amount = 0
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 2.0  # Seconds
    
    def update(self, dt: float, current_time: float, keys: dict):
        """
        Update player position and state.
        
        Args:
            dt: Time delta in seconds
            current_time: Current game time
            keys: Dictionary of key states
        """
        # Movement
        if (keys.get(pygame.K_LEFT, False) or keys.get(pygame.K_a, False)) and self.x > self.width // 2:
            self.x -= self.speed * dt
        if (keys.get(pygame.K_RIGHT, False) or keys.get(pygame.K_d, False)) and self.x < WIDTH - self.width // 2:
            self.x += self.speed * dt
        
        # Update rectangle position
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2
        
        # Update lasers
        for laser in self.lasers[:]:
            laser.update(dt)
            if not laser.active:
                self.lasers.remove(laser)
        
        # Handle hit state
        if self.is_hit:
            self.hit_timer -= dt
            if self.hit_timer <= 0:
                self.is_hit = False
                self.shake_amount = 0
            else:
                # Screen shake effect
                self.shake_amount = 5 * (self.hit_timer / self.hit_duration)
        
        # Handle invincibility after hit
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
    
    def shoot(self, current_time: float) -> bool:
        """
        Try to shoot a laser if cooldown has passed.
        
        Args:
            current_time: Current game time
            
        Returns:
            bool: True if shot was fired, False otherwise
        """
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.lasers.append(Laser(self.x, self.y - self.height // 2))
            self.last_shot_time = current_time
            return True
        return False
    
    def hit(self):
        """Handle player being hit by enemy laser."""
        if not self.invincible:
            self.lives -= 1
            self.is_hit = True
            self.hit_timer = self.hit_duration
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            return True
        return False
    
    def draw(self, surface: pygame.Surface, current_time: float):
        """
        Draw the player ship to the given surface.
        
        Args:
            surface: Surface to draw on
            current_time: Current game time for visual effects
        """
        # Skip drawing every other frame if invincible (blinking effect)
        if self.invincible and int(current_time * 10) % 2 == 0:
            return
        
        # Base ship shape (triangle)
        ship_points = [
            (self.x, self.y - self.height // 2),
            (self.x - self.width // 2, self.y + self.height // 2),
            (self.x + self.width // 2, self.y + self.height // 2)
        ]
        
        # Screen shake if hit
        if self.is_hit:
            shake_x = random.uniform(-self.shake_amount, self.shake_amount)
            shake_y = random.uniform(-self.shake_amount, self.shake_amount)
            ship_points = [(x + shake_x, y + shake_y) for x, y in ship_points]
        
        pygame.draw.polygon(surface, self.color, ship_points)
        
        # Engine glow (pulsing)
        engine_pulse = (math.sin(current_time * 10) + 1) / 4 + 0.5
        engine_width = self.width // 3
        engine_height = self.height // 3
        
        engine_points = [
            (self.x - engine_width // 2, self.y + self.height // 2),
            (self.x + engine_width // 2, self.y + self.height // 2),
            (self.x, self.y + self.height // 2 + engine_height * engine_pulse)
        ]
        
        if self.is_hit:
            shake_x = random.uniform(-self.shake_amount, self.shake_amount)
            shake_y = random.uniform(-self.shake_amount, self.shake_amount)
            engine_points = [(x + shake_x, y + shake_y) for x, y in engine_points]
        
        pygame.draw.polygon(surface, NEON_YELLOW, engine_points)
        
        # Draw a glow effect around the ship
        if not self.is_hit:
            s = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
            glow_points = [
                (5, 5),
                (5 + self.width, 5),
                (5 + self.width // 2, 5 + self.height)
            ]
            pygame.draw.polygon(s, (*self.color[:3], 100), glow_points)
            surface.blit(s, (self.x - self.width // 2 - 5, self.y - self.height // 2 - 5))
            
    def draw_lasers(self, surface: pygame.Surface):
        """Draw all active player lasers."""
        for laser in self.lasers:
            laser.draw(surface)
