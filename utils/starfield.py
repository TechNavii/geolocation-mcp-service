"""
Starfield background with parallax effect for Space Invaders.
"""

import pygame
import random
import math

class Star:
    """A background star for the parallax starfield."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize with random position and depth."""
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.depth = random.uniform(0.1, 1.0)  # Closer to 1 = closer to viewer
        self.brightness = int(self.depth * 255)
        self.size = self.depth * 3
        self.speed = self.depth * 30  # Parallax speed
    
    def update(self, dt: float, screen_width: int, screen_height: int):
        """
        Move the star based on its depth.
        
        Args:
            dt: Time delta in seconds
        """
        # Move down based on depth (parallax effect)
        self.y += self.speed * dt
        
        # If star moves off-screen, reset it at the top
        if self.y > screen_height:
            self.y = 0
            self.x = random.randint(0, screen_width)
    
    def draw(self, surface: pygame.Surface):
        """Draw the star to the given surface."""
        alpha = min(255, self.brightness)
        color = (min(255, int(200 + self.depth * 55)), 
                min(255, int(200 + self.depth * 55)), 
                min(255, int(200 + self.depth * 55)), 
                alpha)
        
        # Create a small surface with per-pixel alpha
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Draw the star with a soft glow
        pygame.draw.circle(s, color, (self.size, self.size), self.size)
        
        # Blit the star surface to the main surface
        surface.blit(s, (self.x - self.size, self.y - self.size))

class Starfield:
    """Background starfield with parallax effect."""
    
    def __init__(self, screen_width: int, screen_height: int, star_count: int = 100):
        """Initialize the starfield with random stars."""
        self.stars = [Star(screen_width, screen_height) for _ in range(star_count)]
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def update(self, dt: float):
        """Update all stars' positions."""
        for star in self.stars:
            star.update(dt, self.screen_width, self.screen_height)
    
    def draw(self, surface: pygame.Surface):
        """Draw all stars to the given surface."""
        for star in self.stars:
            star.draw(surface)
