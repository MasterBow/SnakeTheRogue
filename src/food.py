# food.py
"""
Módulo de Comida.

Define la clase `Food`, un objeto pasivo que:
- Existe en una posición aleatoria.
- Sabe cómo dibujarse a sí mismo.
"""

import pygame
import random
import config as c

class Food:
    """Comida que la serpiente puede comer para crecer."""
    
    def __init__(self):
        """Inicializa la comida en una posición aleatoria del mundo."""
        x = random.randint(0, c.WORLD_WIDTH - c.SNAKE_SIZE)
        y = random.randint(0, c.WORLD_HEIGHT - c.SNAKE_SIZE)
        self.rect = pygame.Rect(x, y, c.SNAKE_SIZE, c.SNAKE_SIZE)

    def draw(self, surface, camera):
        """Dibuja la comida (relativa a la cámara)."""
        pygame.draw.rect(surface, c.BLUE, camera.apply(self.rect))
