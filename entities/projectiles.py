"""
Projectile classes for Space Invaders game.
"""

import pygame
import math
import random
import sys
sys.path.append('/Users/tooru/Desktop/claude_test/space_invaders')
from constants import *

class Laser:
    """Player's laser projectile."""
    
    def __init__(self, x: float, y: float, speed: float = 500):
        """
        Initialize a laser at the given position.
        
        Args:
            x, y: Starting position (center of the laser)
            speed: Upward speed in pixels per second
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 3
        self.height = 15
        self.color = NEON_GREEN
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, 
                               self.width, self.height)
        self.active = True
    
    def update(self, dt: float):
        """
        Move the laser upward.
        
        Args:
            dt: Time delta in seconds
        """
        self.y -= self.speed * dt
        self.rect.y = self.y - self.height // 2
        
        # Deactivate if off screen
        if self.y < -self.height:
            self.active = False
    
    def draw(self, surface: pygame.Surface):
        """Draw the laser to the given surface."""
        # Base rectangle
        pygame.draw.rect(surface, self.color, 
                        (self.x - self.width // 2, self.y - self.height // 2, 
                         self.width, self.height))
        
        # Glow effect
        s = pygame.Surface((self.width + 6, self.height + 6), pygame.SRCALPHA)
        pygame.draw.rect(s, (*self.color[:3], 100), 
                        (3, 3, self.width, self.height))
        surface.blit(s, (self.x - self.width // 2 - 3, self.y - self.height // 2 - 3))

class AlienLaser:
    """Enemy alien's laser projectile."""
    
    def __init__(self, x: float, y: float, speed: float = 300):
        """
        Initialize an alien laser at the given position.
        
        Args:
            x, y: Starting position (center of the laser)
            speed: Downward speed in pixels per second
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 5
        self.height = 10
        self.color = NEON_PINK
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, 
                               self.width, self.height)
        self.active = True
        self.time_offset = random.random() * 10  # For color pulsing
    
    def update(self, dt: float, current_time: float):
        """
        Move the laser downward.
        
        Args:
            dt: Time delta in seconds
            current_time: Current game time for visual effects
        """
        self.y += self.speed * dt
        self.rect.y = self.y - self.height // 2
        
        # Deactivate if off screen
        if self.y > HEIGHT + self.height:
            self.active = False
    
    def draw(self, surface: pygame.Surface, current_time: float):
        """
        Draw the laser to the given surface.
        
        Args:
            surface: Surface to draw on
            current_time: Current game time for visual effects
        """
        # Pulsing effect
        pulse = (math.sin(current_time * 10 + self.time_offset) + 1) / 2
        
        # Create a slightly wavy shape
        wave_offset = math.sin(current_time * 15 + self.time_offset) * 2
        
        points = [
            (self.x - self.width // 2 + wave_offset, self.y - self.height // 2),
            (self.x + self.width // 2 + wave_offset, self.y - self.height // 2),
            (self.x, self.y + self.height // 2)
        ]
        
        # Base shape
        pygame.draw.polygon(surface, self.color, points)
        
        # Glow effect
        s = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        glow_points = [
            (5 + wave_offset, 5),
            (5 + self.width + wave_offset, 5),
            (5 + self.width // 2, 5 + self.height)
        ]
        glow_alpha = int(100 + 50 * pulse)
        pygame.draw.polygon(s, (*self.color[:3], glow_alpha), glow_points)
        surface.blit(s, (self.x - self.width // 2 - 5, self.y - self.height // 2 - 5))
