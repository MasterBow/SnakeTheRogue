# snake.py
"""
Módulo de la Serpiente (El Jugador).

Define la clase `Snake`, que controla:
- El cuerpo de la serpiente (lista de Rects).
- El movimiento, crecimiento y daño.
- Sus estadísticas (cargadas desde la DB).
- La lógica de disparo (cooldown).
- La comunicación con la DB para guardar/cargar.
"""

import pygame
import config as c
from projectile import Projectile
import database  # Importa el módulo de base de datos

class Snake:
    """Controla la serpiente: movimiento, crecimiento, HP, dinero y disparos."""
    
    def __init__(self):
        """Inicializa la serpiente llamando a reset."""
        self.reset()

    def reset(self):
        """
        Reinicia la serpiente a su estado inicial.
        Carga las estadísticas persistentes desde la base de datos.
        """
        
        # Posición inicial (esto no se guarda en la DB)
        self.start_pos = (c.WORLD_WIDTH // 2, c.WORLD_HEIGHT // 2)
        self.body = [pygame.Rect(self.start_pos[0], self.start_pos[1], c.SNAKE_SIZE, c.SNAKE_SIZE)]
        self.direction = pygame.Vector2(0, 0) # Vector de dirección (inicia quieta)
        
        # --- Estadísticas (valores por defecto) ---
        # Estos valores serán sobrescritos por la DB
        self.max_hp = 100
        self.hp = 100
        self.money = 0
        self.attack_damage = 10
        self.attack_speed = 500
        self.projectile_speed = 15
        self.last_shot_time = 0 # Para el cooldown
        
        # Carga los datos persistentes desde la DB
        database.load_player_data(self)
        
        self.segments_to_add = 0 # Contador para crecer

    def move(self):
        """Mueve la serpiente un paso en su dirección actual."""
        if self.direction.length() == 0:
            return # No se mueve si no tiene dirección
        
        # Lógica de "copiar cabeza, borrar cola"
        head = self.body[0].copy()
        head.move_ip(self.direction.x * c.SNAKE_SIZE, self.direction.y * c.SNAKE_SIZE)
        
        self.body.insert(0, head) # Añade la nueva cabeza
        
        if self.segments_to_add > 0:
            self.segments_to_add -= 1 # Crece (no borra la cola)
        else:
            self.body.pop() # No crece (borra la cola)

    def grow(self):
        """Marca que la serpiente debe crecer en los próximos 3 movimientos."""
        self.segments_to_add += 3

    def take_damage(self, amount):
        """Reduce el HP de la serpiente."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def get_head(self):
        """Devuelve el rectángulo de la cabeza (el primer segmento)."""
        return self.body[0]

    def shoot(self):
        """
        Intenta disparar un proyectil.
        Devuelve un objeto Projectile si tiene éxito, o None si está en cooldown.
        """
        
        # No disparar si está quieto
        if self.direction.length() == 0:
            return None
            
        # Comprobar cooldown
        current_time = pygame.time.get_ticks() # Tiempo en milisegundos
        if current_time - self.last_shot_time > self.attack_speed:
            self.last_shot_time = current_time
            
            head = self.get_head()
            
            # Crear el proyectil usando las estadísticas actuales de la serpiente
            new_projectile = Projectile(
                head.centerx, 
                head.centery, 
                self.direction.copy(), 
                self.attack_damage, 
                self.projectile_speed
            )
            return new_projectile
            
        return None # Cooldown activo, no dispara

    def save_stats(self):
        """Llama al módulo de base de datos para guardar las estadísticas."""
        database.save_player_data(self)

    def draw(self, surface, camera):
        """Dibuja cada segmento de la serpiente en la pantalla."""
        for segment in self.body:
            # camera.apply() convierte coordenadas del mundo a pantalla
            pygame.draw.rect(surface, c.GREEN, camera.apply(segment))
