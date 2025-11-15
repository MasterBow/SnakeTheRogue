# enemy.py
"""
Módulo del Enemigo.

Define la clase `Enemy`, que controla:
- Su posición y tamaño (rect).
- Su estado (HP y Max HP).
- Cómo dibujarse a sí mismo, incluyendo su barra de vida.
"""

import pygame
import random
import config as c

class Enemy:
    """Controla a un enemigo simple."""
    
    def __init__(self):
        """Inicializa al enemigo en una posición aleatoria."""
        # Posición aleatoria en el mundo
        x = random.randint(0, c.WORLD_WIDTH - c.SNAKE_SIZE)
        y = random.randint(0, c.WORLD_HEIGHT - c.SNAKE_SIZE)
        self.rect = pygame.Rect(x, y, c.SNAKE_SIZE, c.SNAKE_SIZE)
        
        # Estadísticas del enemigo
        self.max_hp = 20
        self.hp = self.max_hp

    def draw(self, surface, camera):
        """Dibuja el enemigo y su barra de vida (relativos a la cámara)."""
        
        # Dibuja el cuerpo del enemigo (convertido a coordenadas de pantalla)
        body_rect = camera.apply(self.rect)
        pygame.draw.rect(surface, c.RED, body_rect)
        
        # --- Dibuja la Barra de Vida (solo si está herido) ---
        if self.hp < self.max_hp:
            # Fondo de la barra de vida (rojo oscuro)
            hp_bar_bg = pygame.Rect(body_rect.left, body_rect.top - 7, self.rect.width, 5)
            pygame.draw.rect(surface, c.RED.lerp(c.BLACK, 0.5), hp_bar_bg)
            
            # Vida actual (verde)
            hp_percent = self.hp / self.max_hp
            hp_bar_width = int(self.rect.width * hp_percent)
            hp_bar_fill = pygame.Rect(body_rect.left, body_rect.top - 7, hp_bar_width, 5)
            pygame.draw.rect(surface, c.GREEN, hp_bar_fill)
