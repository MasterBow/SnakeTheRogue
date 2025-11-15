# snake.py

import pygame
import config as c
from projectile import Projectile  # <-- Importa la nueva clase

class Snake:
    """Controla la serpiente: movimiento, crecimiento, HP y dinero."""
    def __init__(self):
        # __init__ solo llama a reset() para configurar todo
        self.reset()

    def reset(self):
        """Reinicia la serpiente a su estado inicial."""
        
        # --- CORRECCIÓN APLICADA AQUÍ ---
        # 1. Define 'start_pos' ANTES de usarlo.
        # 2. Usa 'WORLD_WIDTH' y 'WORLD_HEIGHT' del archivo config.
        self.start_pos = (c.WORLD_WIDTH // 2, c.WORLD_HEIGHT // 2)

        # Ahora crea el cuerpo usando 'start_pos'
        self.body = [pygame.Rect(self.start_pos[0], self.start_pos[1], c.SNAKE_SIZE, c.SNAKE_SIZE)]
        self.direction = pygame.Vector2(0, 0)
        
        # --- NUEVAS ESTADÍSTICAS ---
        self.max_hp = 100
        self.hp = self.max_hp
        self.money = 25
        self.attack_damage = 10       # Daño por disparo
        self.attack_speed = 500       # Cooldown de disparo en milisegundos (2 disparos/seg)
        self.projectile_speed = 15    # Píxeles por frame que viaja la bala
        self.last_shot_time = 0       # Para controlar el cooldown
        # --- FIN DE ESTADÍSTICAS ---
        
        self.segments_to_add = 0

    def move(self):
        """Mueve la serpiente y maneja el crecimiento."""
        if self.direction.length() == 0:
            return
        
        head = self.body[0].copy()
        head.move_ip(self.direction.x * c.SNAKE_SIZE, self.direction.y * c.SNAKE_SIZE)
        
        self.body.insert(0, head)
        
        if self.segments_to_add > 0:
            self.segments_to_add -= 1
        else:
            self.body.pop()

    def grow(self):
        """Marca que la serpiente debe crecer en el próximo movimiento."""
        self.segments_to_add += 3

    def take_damage(self, amount):
        """Reduce el HP de la serpiente."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def get_head(self):
        """Devuelve el rectángulo de la cabeza."""
        return self.body[0]

    # --- MÉTODO NUEVO ---
    def shoot(self):
        """Crea y devuelve un proyectil si el cooldown lo permite."""
        
        # No disparar si está quieto
        if self.direction.length() == 0:
            return None
            
        # Comprobar cooldown
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.attack_speed:
            self.last_shot_time = current_time
            
            # El proyectil sale de la cabeza de la serpiente
            head = self.get_head()
            
            # Crear el proyectil usando las estadísticas de la serpiente
            new_projectile = Projectile(
                head.centerx, 
                head.centery, 
                self.direction.copy(), 
                self.attack_damage, 
                self.projectile_speed
            )
            return new_projectile
            
        return None # Cooldown activo

    def draw(self, surface, camera):
        """Dibuja la serpiente en la pantalla."""
        for segment in self.body:
            pygame.draw.rect(surface, c.GREEN, camera.apply(segment))
