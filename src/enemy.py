# enemy.py
"""
Módulo del Enemigo.
Define diferentes tipos de enemigos que persiguen al jugador.
"""

import pygame
import random
import config as c

class Enemy:
    """Controla a un enemigo con IA de persecución básica."""
    
    def __init__(self):
        """Inicializa al enemigo con un tipo aleatorio y estadísticas de movimiento."""
        
        # Elegir tipo de enemigo
        rand_val = random.random()
        
        if rand_val < 0.6:
            self.type = "normal"
            self.color = c.RED
            self.max_hp = 20
            self.size = c.SNAKE_SIZE
            self.score_value = 50
            self.speed = 3 # Velocidad moderada
        elif rand_val < 0.8:
            self.type = "tank"
            self.color = c.DARK_BLUE
            self.max_hp = 50
            self.size = int(c.SNAKE_SIZE * 1.5)
            self.score_value = 100
            self.speed = 1.5 # Lento pero resistente
        else:
            self.type = "fast"
            self.color = c.YELLOW
            self.max_hp = 10
            self.size = int(c.SNAKE_SIZE * 0.8)
            self.score_value = 75
            self.speed = 5 # Muy rápido
        
        self.hp = self.max_hp

        # Posición aleatoria en el mundo
        x = random.randint(0, c.WORLD_WIDTH - self.size)
        y = random.randint(0, c.WORLD_HEIGHT - self.size)
        self.rect = pygame.Rect(x, y, self.size, self.size)
        
        # Usamos un Vector2 para la posición para permitir movimiento decimal suave
        self.pos = pygame.Vector2(x, y)

    def move(self, target_rect):
        """
        Mueve al enemigo hacia el objetivo (la serpiente).
        target_rect: El pygame.Rect del objetivo a perseguir.
        """
        # Centro del enemigo y centro del objetivo
        enemy_center = pygame.Vector2(self.rect.center)
        target_center = pygame.Vector2(target_rect.center)
        
        # Vector de dirección (Objetivo - Enemigo)
        direction = target_center - enemy_center
        
        # Si la distancia es mayor a 0, normalizamos y movemos
        if direction.length() > 0:
            direction = direction.normalize()
            
            # Actualizamos la posición decimal
            self.pos += direction * self.speed
            
            # Actualizamos el rectángulo de colisión (enteros)
            self.rect.x = int(self.pos.x)
            self.rect.y = int(self.pos.y)

    def draw(self, surface, camera):
        """Dibuja el enemigo y su barra de vida."""
        
        body_rect = camera.apply(self.rect)
        pygame.draw.rect(surface, self.color, body_rect)
        
        # Borde para resaltar
        pygame.draw.rect(surface, c.BLACK, body_rect, 1)
        
        # --- Barra de Vida ---
        if self.hp < self.max_hp:
            hp_bar_bg = pygame.Rect(body_rect.left, body_rect.top - 7, self.rect.width, 5)
            pygame.draw.rect(surface, c.HP_BAR_BG, hp_bar_bg)
            
            hp_percent = self.hp / self.max_hp
            hp_bar_width = int(self.rect.width * hp_percent)
            hp_bar_fill = pygame.Rect(body_rect.left, body_rect.top - 7, hp_bar_width, 5)
            pygame.draw.rect(surface, c.GREEN, hp_bar_fill)