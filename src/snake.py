# snake.py
"""
Módulo de la Serpiente (El Jugador).
Incluye sonido de disparo y de comer generados proceduralmente.
Sistema de Niveles RPG implementado.
"""

import pygame
import config as c
from projectile import Projectile
import database 
import math
import array

class Snake:
    """Controla la serpiente: movimiento, stats, sonido sintético y niveles."""
    
    def __init__(self):
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
            
        # --- Generar Sonidos (Sintéticos) ---
        self.shoot_sound = None
        self.eat_sound = None
        try:
            self.shoot_sound = self._generate_shoot_sound()
            self.eat_sound = self._generate_eat_sound()
        except Exception as e:
            print(f"Advertencia: No se pudo generar el audio. Error: {e}")

        self.reset()

    def _generate_shoot_sound(self):
        """Genera un 'pew' (onda cuadrada)"""
        sample_rate = 44100
        duration = 0.12
        frequency = 800
        n_samples = int(sample_rate * duration)
        amplitude = 3000
        buf = array.array("h")
        for i in range(n_samples):
            t = i / sample_rate
            value = amplitude if math.sin(2 * math.pi * frequency * t) >= 0 else -amplitude
            decay = 1.0 - (i / n_samples)
            buf.append(int(value * decay))
        return pygame.mixer.Sound(buffer=buf)

    def _generate_eat_sound(self):
        """Genera un 'bloop' (onda senoidal) para comer."""
        sample_rate = 44100
        duration = 0.1 
        frequency = 400 # Tono más grave y suave
        n_samples = int(sample_rate * duration)
        amplitude = 4000 
        buf = array.array("h")
        for i in range(n_samples):
            t = i / sample_rate
            # Onda Senoidal (más suave que la cuadrada)
            value = int(amplitude * math.sin(2 * math.pi * frequency * t))
            buf.append(value)
        return pygame.mixer.Sound(buffer=buf)

    def reset(self):
        """Reinicia la serpiente."""
        self.start_pos = (c.WORLD_WIDTH // 2, c.WORLD_HEIGHT // 2)
        self.body = [pygame.Rect(self.start_pos[0], self.start_pos[1], c.SNAKE_SIZE, c.SNAKE_SIZE)]
        self.direction = pygame.Vector2(0, 0) 
        
        # Stats base
        self.max_hp = 100
        self.hp = 100
        self.money = 0
        self.attack_damage = 10
        self.attack_speed = 500
        self.projectile_speed = 15
        self.last_shot_time = 0 
        
        database.load_player_data(self)
        
        self.segments_to_add = 0
        
        self.score = 0
        self.last_score_time = pygame.time.get_ticks()
        self.decay_counter = 0
        
        # --- SISTEMA DE NIVELES ---
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 50 # XP necesaria para el primer nivel

    def move(self):
        if self.direction.length() == 0:
            return 
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_score_time > 10000:
            self.decay_counter += 1
            if self.decay_counter >= 5:
                if self.score > 0:
                    self.score -= 1
                self.decay_counter = 0

        head = self.body[0].copy()
        head.move_ip(self.direction.x * c.SNAKE_SIZE, self.direction.y * c.SNAKE_SIZE)
        
        self.body.insert(0, head) 
        
        if self.segments_to_add > 0:
            self.segments_to_add -= 1 
        else:
            self.body.pop() 

    def grow(self):
        """Hace crecer a la serpiente, reproduce sonido y añade XP."""
        self.segments_to_add += 3
        
        # Sonido
        if self.eat_sound:
            self.eat_sound.set_volume(c.MASTER_VOLUME)
            self.eat_sound.play()
            
        # Ganar XP (Cada comida da 10 XP)
        self.gain_xp(10)

    def gain_xp(self, amount):
        """Añade XP y gestiona la subida de nivel."""
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """Sube de nivel y mejora estadísticas un 5%."""
        self.level += 1
        self.xp -= self.xp_to_next_level
        # Cada nivel cuesta un 20% más de XP que el anterior
        self.xp_to_next_level = int(self.xp_to_next_level * 1.2)
        
        # --- MEJORAS DE STATS (+5%) ---
        self.max_hp = int(self.max_hp * 1.05)
        self.hp = self.max_hp # ¡Curación completa al subir de nivel!
        self.attack_damage = int(self.attack_damage * 1.05)
        
        # Velocidad de ataque (Reduce el delay, min 50ms)
        self.attack_speed = max(50, int(self.attack_speed * 0.95))
        
        print(f"¡NIVEL UP! Nivel {self.level}. HP: {self.max_hp}, Daño: {self.attack_damage}")

    def add_score(self, amount):
        self.score += amount
        self.last_score_time = pygame.time.get_ticks()

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def get_head(self):
        return self.body[0]

    def shoot(self):
        if self.direction.length() == 0:
            return None
            
        current_time = pygame.time.get_ticks() 
        if current_time - self.last_shot_time > self.attack_speed:
            self.last_shot_time = current_time
            head = self.get_head()
            
            new_projectile = Projectile(
                head.centerx, 
                head.centery, 
                self.direction.copy(), 
                self.attack_damage, 
                self.projectile_speed
            )
            
            if self.shoot_sound:
                self.shoot_sound.set_volume(c.MASTER_VOLUME)
                self.shoot_sound.play()
            
            return new_projectile
        return None 

    def save_stats(self):
        database.save_player_data(self)

    def draw(self, surface, camera):
        for segment in self.body:
            pygame.draw.rect(surface, c.GREEN, camera.apply(segment))