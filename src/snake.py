# snake.py

import pygame
import config as c

class Snake:
    """Controla la serpiente: movimiento, crecimiento, HP y dinero."""
    def __init__(self):
        # La serpiente empieza en el centro del mundo
        self.start_pos = (c.WORLD_WIDTH // 2, c.WORLD_HEIGHT // 2)
        self.reset()

    def reset(self):
        """Reinicia la serpiente a su estado inicial."""
        self.body = [pygame.Rect(self.start_pos[0], self.start_pos[1], c.SNAKE_SIZE, c.SNAKE_SIZE)]
        self.direction = pygame.Vector2(0, 0)
        self.max_hp = 100
        self.hp = self.max_hp
        self.money = 25
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

    def draw(self, surface, camera):
        """Dibuja la serpiente en la pantalla."""
        for segment in self.body:
            pygame.draw.rect(surface, c.GREEN, camera.apply(segment))
