# projectile.py
##Practica 3 terminada. 
"""
Módulo del Proyectil (Bala).

Define la clase `Projectile`, un objeto simple que:
- Nace en una posición y con una dirección.
- Tiene estadísticas (daño, velocidad).
- Sabe cómo moverse a sí mismo en línea recta.
"""

import pygame
import config as c

class Projectile:
    """Define un proyectil disparado por la serpiente."""
    
    def __init__(self, x, y, direction_vector, damage, speed):
        """
        Inicializa el proyectil.
        x, y: Posición inicial (centro)
        direction_vector: Vector2 de la serpiente (ej. (0, -1) para arriba)
        damage, speed: Estadísticas heredadas de la serpiente
        """
        self.size = 8
        self.rect = pygame.Rect(x - self.size // 2, y - self.size // 2, self.size, self.size)
        self.damage = damage
        
        # Normaliza el vector (longitud 1) y luego lo multiplica por la velocidad
        # Esto asegura que las balas diagonales no sean más rápidas
        self.direction = direction_vector.normalize() * speed

    def move(self):
        """Mueve el proyectil basado en su vector de dirección."""
        self.rect.move_ip(self.direction.x, self.direction.y)

    def draw(self, surface, camera):
        """Dibuja el proyectil (relativo a la cámara)."""
        pygame.draw.rect(surface, c.ORANGE, camera.apply(self.rect))
