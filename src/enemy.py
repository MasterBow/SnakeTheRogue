# enemy.py

import pygame
import random
import config as c

class Enemy:
    """Controla a un enemigo simple."""
    def __init__(self):
        # Posición aleatoria en el mundo
        x = random.randint(0, c.WORLD_WIDTH - c.SNAKE_SIZE)
        y = random.randint(0, c.WORLD_HEIGHT - c.SNAKE_SIZE)
        self.rect = pygame.Rect(x, y, c.SNAKE_SIZE, c.SNAKE_SIZE)
        self.hp = 20

    def draw(self, surface, camera):
        """Dibuja el enemigo relativo a la cámara."""
        pygame.draw.rect(surface, c.RED, camera.apply(self.rect))
