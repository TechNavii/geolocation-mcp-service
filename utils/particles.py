"""
Particle system for visual effects in the Space Invaders game.
"""

import pygame
import random
import math
from typing import List, Tuple

class Particle:
    """Particle effect for explosions and visual feedback."""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], 
                 velocity: Tuple[float, float], size: float, lifetime: float):
        """
        Initialize a particle.
        
        Args:
            x, y: Position
            color: RGB color tuple
            velocity: (vx, vy) velocity vector
            size: Initial size in pixels
            lifetime: Maximum lifetime in seconds
        """
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.alpha = 255
    
    def update(self, dt: float) -> bool:
        """
        Update particle position and properties.
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            bool: True if particle is still alive, False if expired
        """
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        
        # Update lifetime and alpha
        self.lifetime -= dt
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        # Gradually decrease size
        self.size *= 0.97
        
        return self.lifetime > 0
    
    def draw(self, surface: pygame.Surface):
        """Draw the particle to the given surface."""
        if self.alpha <= 0:
            return
            
        # Create a surface with per-pixel alpha
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Draw the particle with alpha
        pygame.draw.circle(s, (*self.color, self.alpha), (self.size, self.size), self.size)
        
        # Blit the particle surface to the main surface
        surface.blit(s, (self.x - self.size, self.y - self.size))

class ParticleSystem:
    """Manager for particle effects."""
    
    def __init__(self):
        """Initialize an empty particle system."""
        self.particles = []
        
    def add_explosion(self, x: float, y: float, color: Tuple[int, int, int], 
                      count: int = 20, size: float = 3.0):
        """
        Create an explosion effect at the specified position.
        
        Args:
            x, y: Position
            color: Base RGB color tuple
            count: Number of particles
            size: Size of particles
        """
        for _ in range(count):
            # Randomize velocity
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Slightly vary color
            r = min(255, max(0, color[0] + random.randint(-20, 20)))
            g = min(255, max(0, color[1] + random.randint(-20, 20)))
            b = min(255, max(0, color[2] + random.randint(-20, 20)))
            
            # Randomize lifetime
            lifetime = random.uniform(0.5, 1.5)
            
            self.particles.append(Particle(x, y, (r, g, b), (vx, vy), 
                                          size * random.uniform(0.7, 1.3), lifetime))
    
    def update(self, dt: float):
        """
        Update all particles.
        
        Args:
            dt: Time delta in seconds
        """
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def draw(self, surface: pygame.Surface):
        """Draw all particles to the given surface."""
        for p in self.particles:
            p.draw(surface)
    
    def clear(self):
        """Remove all particles."""
        self.particles.clear()
