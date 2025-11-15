# snake.py

import pygame
import config as c
from projectile import Projectile  # <-- Importa la nueva clase
import database
class Snake:
class Snake:
    """Controla la serpiente: movimiento, crecimiento, HP y dinero."""
    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia la serpiente cargando sus estadísticas desde la DB."""
        
        # Posición inicial (esto no se guarda en la DB)
        self.start_pos = (c.WORLD_WIDTH // 2, c.WORLD_HEIGHT // 2)
        self.body = [pygame.Rect(self.start_pos[0], self.start_pos[1], c.SNAKE_SIZE, c.SNAKE_SIZE)]
        self.direction = pygame.Vector2(0, 0)
        
        # --- LÓGICA DE ESTADÍSTICAS MODIFICADA ---
        # Estas variables ahora se llenarán desde la base de datos
        self.max_hp = 100
        self.hp = 100
        self.money = 0
        self.attack_damage = 10
        self.attack_speed = 500
        self.projectile_speed = 15
        self.last_shot_time = 0
        
        # ¡Carga los datos persistentes!
        database.load_player_data(self)

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
        # --- MÉTODO NUEVO ---
    def save_stats(self):
        """Llama al módulo de base de datos para guardar las estadísticas."""
        database.save_player_data(self)

    def draw(self, surface, camera):
        """Dibuja la serpiente en la pantalla."""
        for segment in self.body:
            pygame.draw.rect(surface, c.GREEN, camera.apply(segment))
