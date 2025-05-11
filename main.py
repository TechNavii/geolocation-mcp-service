#!/usr/bin/env python3
"""
Space Invaders Reimagined
A modern take on the classic Space Invaders game using Python and Pygame.
All graphics are generated procedurally - no external assets used.

Controls:
    ← / A      move left
    → / D      move right
    Space      shoot
    Esc        quit
"""

import pygame
import sys
import time
import random
import math

# Import game modules
from constants import *
from utils.particles import ParticleSystem
from utils.starfield import Starfield
from entities.player import Player
from entities.aliens import AlienFleet

class Game:
    """Main game class that manages the game state and logic."""
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        pygame.display.set_caption("Space Invaders Reimagined")
        
        # Set up the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Create game objects
        self.starfield = Starfield(WIDTH, HEIGHT, 150)
        self.player = Player(WIDTH // 2, HEIGHT - 50)
        self.alien_fleet = AlienFleet()
        self.particle_system = ParticleSystem()
        
        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.game_over_timer = 0
        self.game_over_delay = 3.0  # Seconds to wait before returning to menu
        
        # Create fonts
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Time tracking
        self.current_time = 0
        self.last_time = time.time()
        self.dt = 0  # Delta time in seconds
        
        # Key states
        self.keys = {}
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            # Calculate delta time
            self.current_time = time.time()
            self.dt = self.current_time - self.last_time
            self.last_time = self.current_time
            
            # Cap delta time to prevent large jumps
            self.dt = min(self.dt, 0.05)
            
            # Process input
            self.handle_input()
            
            # Update game state
            self.update()
            
            # Render
            self.render()
            
            # Cap frame rate
            self.clock.tick(FPS)
    
    def handle_input(self):
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                # Store key state
                self.keys[event.key] = True
                
                # Handle key presses
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    else:
                        pygame.quit()
                        sys.exit()
                
                elif event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.start_game()
                    elif self.state == GameState.GAME_OVER:
                        self.state = GameState.MENU
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.PLAYING:
                        self.player.shoot(self.current_time)
            
            elif event.type == pygame.KEYUP:
                # Update key state
                self.keys[event.key] = False
    
    def update(self):
        """Update game state based on current game mode."""
        # Always update starfield for background effect
        self.starfield.update(self.dt)
        
        if self.state == GameState.PLAYING:
            # Update player
            self.player.update(self.dt, self.current_time, self.keys)
            
            # Update alien fleet
            self.alien_fleet.update(self.dt, self.current_time)
            
            # Update particles
            self.particle_system.update(self.dt)
            
            # Check collisions
            self.check_collisions()
            
            # Check game over conditions
            self.check_game_over()
            
            # Check level completion
            if self.alien_fleet.all_destroyed():
                self.level += 1
                self.alien_fleet.reset()
                # Increase difficulty with each level
                self.alien_fleet.speed += 5
                self.alien_fleet.shoot_chance += 0.05
        
        elif self.state == GameState.GAME_OVER:
            # Update game over timer
            self.game_over_timer += self.dt
            
            if self.game_over_timer >= self.game_over_delay:
                self.state = GameState.MENU
                self.game_over_timer = 0
            
            # Still update particles for visual effect
            self.particle_system.update(self.dt)
    
    def check_collisions(self):
        """Check all possible collisions."""
        # Player lasers vs aliens
        for laser in self.player.lasers[:]:
            alien = self.alien_fleet.check_collision(laser)
            if alien:
                # Remove laser
                laser.active = False
                self.player.lasers.remove(laser)
                
                # Deactivate alien
                alien.active = False
                self.alien_fleet.aliens_destroyed += 1
                
                # Add score based on alien type
                self.score += alien.points
                
                # Create explosion effect
                self.particle_system.add_explosion(alien.x, alien.y, alien.color, 30, 4.0)
        
        # Alien lasers vs player
        for laser in self.alien_fleet.lasers[:]:
            if laser.active and self.player.rect.colliderect(laser.rect):
                # Player hit!
                if self.player.hit():
                    laser.active = False
                    self.alien_fleet.lasers.remove(laser)
                    
                    # Create impact effect
                    self.particle_system.add_explosion(
                        self.player.x, self.player.y - self.player.height // 2, 
                        self.player.color, 20, 3.0
                    )
        
        # Aliens reaching bottom
        for alien in self.alien_fleet.aliens:
            if alien.active and alien.y + alien.height // 2 > HEIGHT - 50:
                # Game over when aliens reach the bottom
                self.game_over()
    
    def check_game_over(self):
        """Check if player has lost all lives."""
        if self.player.lives <= 0:
            self.game_over()
    
    def game_over(self):
        """Handle game over state."""
        self.state = GameState.GAME_OVER
        
        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
        
        # Create a big explosion for dramatic effect
        for _ in range(10):
            x = random.uniform(self.player.x - 50, self.player.x + 50)
            y = random.uniform(self.player.y - 50, self.player.y + 50)
            color = random.choice([NEON_PINK, NEON_YELLOW, NEON_CYAN])
            self.particle_system.add_explosion(x, y, color, 40, 5.0)
    
    def start_game(self):
        """Start a new game."""
        self.state = GameState.PLAYING
        self.score = 0
        self.level = 1
        self.player = Player(WIDTH // 2, HEIGHT - 50)
        self.alien_fleet.reset()
        self.particle_system.clear()
    
    def render(self):
        """Render the current game state."""
        # Fill the background
        self.screen.fill(BLACK)
        
        # Draw starfield
        self.starfield.draw(self.screen)
        
        # Draw game elements based on state
        if self.state == GameState.MENU:
            self.render_menu()
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            self.render_game()
            
            if self.state == GameState.PAUSED:
                self.render_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self.render_game()
            self.render_game_over()
        
        # Update the display
        pygame.display.flip()
    
    def render_menu(self):
        """Render the main menu screen."""
        # Title
        title_text = self.font_large.render("SPACE INVADERS", True, NEON_CYAN)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        
        # Create a glow effect for the title
        glow_surf = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*NEON_CYAN[:3], 100), 
                       (0, 0, title_rect.width + 20, title_rect.height + 20), 
                       border_radius=10)
        self.screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        prompt_text = self.font_medium.render("Press SPACE to Start", True, NEON_YELLOW)
        prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(prompt_text, prompt_rect)
        
        # Controls
        controls_text = [
            "Controls:",
            "← / A : Move Left",
            "→ / D : Move Right",
            "SPACE : Shoot",
            "ESC   : Pause/Quit"
        ]
        
        y_offset = HEIGHT * 0.65
        for line in controls_text:
            text = self.font_small.render(line, True, WHITE)
            rect = text.get_rect(center=(WIDTH // 2, y_offset))
            self.screen.blit(text, rect)
            y_offset += 30
        
        # High score
        if self.high_score > 0:
            high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, NEON_PINK)
            high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            self.screen.blit(high_score_text, high_score_rect)
    
    def render_game(self):
        """Render the main gameplay elements."""
        # Draw player
        self.player.draw(self.screen, self.current_time)
        self.player.draw_lasers(self.screen)
        
        # Draw alien fleet
        self.alien_fleet.draw(self.screen, self.current_time)
        
        # Draw particles
        self.particle_system.draw(self.screen)
        
        # Draw UI
        self.render_ui()
    
    def render_ui(self):
        """Render the user interface during gameplay."""
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Level
        level_text = self.font_medium.render(f"Level: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(midtop=(WIDTH // 2, 20))
        self.screen.blit(level_text, level_rect)
        
        # Lives
        lives_text = self.font_medium.render(f"Lives: {self.player.lives}", True, WHITE)
        lives_rect = lives_text.get_rect(topright=(WIDTH - 20, 20))
        self.screen.blit(lives_text, lives_rect)
    
    def render_pause_overlay(self):
        """Render the pause screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, NEON_CYAN)
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        resume_text = self.font_medium.render("Press SPACE to Resume", True, NEON_YELLOW)
        resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        self.screen.blit(resume_text, resume_rect)
        
        quit_text = self.font_medium.render("Press ESC to Quit", True, NEON_YELLOW)
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        self.screen.blit(quit_text, quit_rect)
    
    def render_game_over(self):
        """Render the game over screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, NEON_PINK)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        self.screen.blit(final_score_text, final_score_rect)
        
        # New high score notification
        if self.score == self.high_score and self.score > 0:
            high_score_text = self.font_medium.render("NEW HIGH SCORE!", True, NEON_YELLOW)
            high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
            self.screen.blit(high_score_text, high_score_rect)

def main():
    """Main entry point for the game."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
