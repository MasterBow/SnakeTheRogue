# projectile.py

import pygame
import config as c

class Projectile:
    """Define un proyectil disparado por la serpiente."""
    
    def __init__(self, x, y, direction_vector, damage, speed):
        self.size = 8
        self.rect = pygame.Rect(x - self.size // 2, y - self.size // 2, self.size, self.size)
        self.damage = damage
        
        # Asegurarnos de que el vector de dirección esté normalizado y tenga velocidad
        self.direction = direction_vector.normalize() * speed

    def move(self):
        """Mueve el proyectil basado en su vector de dirección."""
        self.rect.move_ip(self.direction.x, self.direction.y)

    def draw(self, surface, camera):
        """Dibuja el proyectil (relativo a la cámara)."""
        pygame.draw.rect(surface, c.ORANGE, camera.apply(self.rect))
