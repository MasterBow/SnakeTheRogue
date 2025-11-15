# main.py

import pygame
import sys
import random

# --- Constantes y Configuración Inicial ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (211, 47, 47)
GREEN = (76, 175, 80)
BLUE = (33, 150, 243)
YELLOW = (255, 235, 59)
PURPLE = (156, 39, 176)
ORANGE = (255, 152, 0)

SNAKE_SIZE = 20
SNAKE_SPEED = 10

# --- Paso 1: Clases Base del Juego ---

class Snake:
    """Controla la serpiente: movimiento, crecimiento, HP y dinero."""
    def __init__(self):
        # La serpiente empieza en el centro del mundo
        self.start_pos = (WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
        self.reset()

    def reset(self):
        """Reinicia la serpiente a su estado inicial."""
        self.body = [pygame.Rect(self.start_pos[0], self.start_pos[1], SNAKE_SIZE, SNAKE_SIZE)]
        self.direction = pygame.Vector2(0, 0)
        self.max_hp = 100
        self.hp = self.max_hp
        self.money = 25
        self.segments_to_add = 0

    def move(self):
        """Mueve la serpiente y maneja el crecimiento."""
        if self.direction.length() == 0:
            return
        
        # Copia la cabeza y la mueve en la nueva dirección
        head = self.body[0].copy()
        head.move_ip(self.direction.x * SNAKE_SIZE, self.direction.y * SNAKE_SIZE)
        
        # Añade la nueva cabeza al principio del cuerpo
        self.body.insert(0, head)
        
        # Maneja el crecimiento
        if self.segments_to_add > 0:
            self.segments_to_add -= 1
        else:
            # Si no está creciendo, elimina el último segmento
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
            # Dibuja cada segmento relativo a la cámara
            pygame.draw.rect(surface, GREEN, camera.apply(segment))


class Enemy:
    """Controla a un enemigo simple."""
    def __init__(self):
        # Posición aleatoria en el mundo, lejos del centro para no aparecer encima del jugador
        x = random.randint(0, WORLD_WIDTH - SNAKE_SIZE)
        y = random.randint(0, WORLD_HEIGHT - SNAKE_SIZE)
        self.rect = pygame.Rect(x, y, SNAKE_SIZE, SNAKE_SIZE)
        self.hp = 20

    def draw(self, surface, camera):
        """Dibuja el enemigo relativo a la cámara."""
        pygame.draw.rect(surface, RED, camera.apply(self.rect))

class Food:
    """Comida que la serpiente puede comer para crecer."""
    def __init__(self):
        # Posición aleatoria en el mundo
        x = random.randint(0, WORLD_WIDTH - SNAKE_SIZE)
        y = random.randint(0, WORLD_HEIGHT - SNAKE_SIZE)
        self.rect = pygame.Rect(x, y, SNAKE_SIZE, SNAKE_SIZE)

    def draw(self, surface, camera):
        """Dibuja la comida relativa a la cámara."""
        pygame.draw.rect(surface, BLUE, camera.apply(self.rect))

# --- Paso 3: Clases de Tienda y Cámara ---

class Shop:
    """La tienda donde el jugador puede comprar mejoras."""
    def __init__(self):
        # La tienda está en el centro del mundo
        self.rect = pygame.Rect(WORLD_WIDTH // 2 - 50, WORLD_HEIGHT // 2 - 50, 100, 100)
        self.items = {
            "health_potion": {"cost": 15, "description": "Restaura 50 HP (H)"},
        }

    def draw(self, surface, camera):
        """Dibuja la tienda relativa a la cámara."""
        pygame.draw.rect(surface, PURPLE, camera.apply(self.rect))
        font = pygame.font.Font(None, 24)
        text = font.render("Tienda", True, WHITE)
        text_rect = text.get_rect(center=camera.apply(self.rect).center)
        surface.blit(text, text_rect)

class Camera:
    """Sigue al jugador y gestiona las coordenadas del mundo vs. pantalla."""
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity_rect):
        """Convierte coordenadas del mundo a coordenadas de pantalla."""
        return entity_rect.move(-self.camera.left, -self.camera.top)

    def update(self, target_rect):
        """Actualiza la posición de la cámara para centrarse en el objetivo."""
        x = -target_rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target_rect.centery + int(SCREEN_HEIGHT / 2)

        # Limita el scroll a los bordes del mundo
        x = min(0, x)  # Borde izquierdo
        y = min(0, y)  # Borde superior
        x = max(-(self.width - SCREEN_WIDTH), x)   # Borde derecho
        y = max(-(self.height - SCREEN_HEIGHT), y) # Borde inferior
        
        self.camera = pygame.Rect(x, y, self.width, self.height)

# --- Clase Principal del Juego ---

class Game:
    """Orquesta todo el juego: bucle, estados, eventos y renderizado."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake con Esteroides")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        
        # Inicializa el estado del juego
        self.state = 'main_menu' # Posibles estados: 'main_menu', 'playing', 'shop', 'game_over'
        self.setup_game()

    def setup_game(self):
        """Configura o resetea las entidades del juego."""
        self.snake = Snake()
        self.enemies = [Enemy() for _ in range(15)]
        self.foods = [Food() for _ in range(20)]
        self.shop = Shop()
        self.camera = Camera(WORLD_WIDTH, WORLD_HEIGHT)

    def run(self):
        """Bucle principal del juego que gestiona los estados."""
        while True:
            self.events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(15) # Controla la velocidad del juego

    def events(self):
        """Maneja todas las entradas del usuario."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # --- Eventos según el estado del juego ---
            if self.state == 'main_menu':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = 'playing'
                    self.snake.direction = pygame.Vector2(1, 0) # Inicia el movimiento
            
            elif self.state == 'playing':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction.y == 0:
                        self.snake.direction = pygame.Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and self.snake.direction.y == 0:
                        self.snake.direction = pygame.Vector2(0, 1)
                    elif event.key == pygame.K_LEFT and self.snake.direction.x == 0:
                        self.snake.direction = pygame.Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT and self.snake.direction.x == 0:
                        self.snake.direction = pygame.Vector2(1, 0)
                    # Lógica para entrar a la tienda
                    elif event.key == pygame.K_e and self.snake.get_head().colliderect(self.shop.rect):
                        self.state = 'shop'

            elif self.state == 'shop':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'playing'
                    # Comprar poción de vida con la tecla 'H'
                    elif event.key == pygame.K_h:
                        potion_cost = self.shop.items["health_potion"]["cost"]
                        if self.snake.money >= potion_cost:
                            self.snake.money -= potion_cost
                            self.snake.hp = min(self.snake.max_hp, self.snake.hp + 50)
            
            elif self.state == 'game_over':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.setup_game() # Reinicia el juego
                    self.state = 'main_menu'

    def update(self):
        """Actualiza la lógica del juego (movimiento, colisiones)."""
        if self.state != 'playing':
            return # No actualiza nada si no estamos jugando

        self.snake.move()
        self.camera.update(self.snake.get_head())

        # Colisiones con la comida
        head = self.snake.get_head()
        for food in self.foods[:]:
            if head.colliderect(food.rect):
                self.foods.remove(food)
                self.snake.grow()
                self.foods.append(Food()) # Añade nueva comida
                break
        
        # Colisiones con enemigos
        for enemy in self.enemies[:]:
            if head.colliderect(enemy.rect):
                self.snake.take_damage(20)
                self.enemies.remove(enemy)
                self.enemies.append(Enemy()) # Reaparece en otro lugar
                self.snake.money += 5 # Gana dinero
                break
        
        # Colisiones con bordes del mundo
        if not (0 <= head.x < WORLD_WIDTH and 0 <= head.y < WORLD_HEIGHT):
            self.snake.take_damage(100) # Morir al chocar con el borde

        # Colisión consigo misma
        for segment in self.snake.body[1:]:
            if head.colliderect(segment):
                self.snake.take_damage(100)
                break
        
        # Verificar si el juego terminó
        if self.snake.hp <= 0:
            self.state = 'game_over'

    def draw(self):
        """Dibuja todo en la pantalla según el estado."""
        self.screen.fill(BLACK)
        
        if self.state == 'main_menu':
            self._draw_text("Snake con Esteroides", self.font_large, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            self._draw_text("Presiona ENTER para comenzar", self.font_small, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self._draw_text("Muévete con las flechas", self.font_small, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3)

        elif self.state == 'playing':
            self._draw_world()
            self._draw_hud()

        elif self.state == 'shop':
            self._draw_world() # Dibuja el mundo de fondo
            self._draw_shop_menu()

        elif self.state == 'game_over':
            self._draw_text("Game Over", self.font_large, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            self._draw_text("Presiona ENTER para volver al menú", self.font_small, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def _draw_world(self):
        """Dibuja todos los objetos del juego relativos a la cámara."""
        self.shop.draw(self.screen, self.camera)
        for food in self.foods:
            food.draw(self.screen, self.camera)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)
        self.snake.draw(self.screen, self.camera)

    def _draw_hud(self):
        """Dibuja la interfaz de usuario (HP, dinero)."""
        # Barra de vida
        hp_text = self.font_small.render(f"HP: {self.snake.hp} / {self.snake.max_hp}", True, WHITE)
        self.screen.blit(hp_text, (10, 10))
        # Dinero
        money_text = self.font_small.render(f"Dinero: ${self.snake.money}", True, YELLOW)
        self.screen.blit(money_text, (10, 50))
        # Mensaje de la tienda
        if self.snake.get_head().colliderect(self.shop.rect):
            shop_prompt = self.font_small.render("Presiona [E] para entrar a la tienda", True, PURPLE)
            self.screen.blit(shop_prompt, (SCREEN_WIDTH / 2 - shop_prompt.get_width() / 2, SCREEN_HEIGHT - 50))


    def _draw_shop_menu(self):
        """Dibuja la interfaz de la tienda."""
        # Dibuja un panel semitransparente
        panel = pygame.Surface((SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        self.screen.blit(panel, (100, 100))
        
        self._draw_text("Tienda", self.font_large, PURPLE, SCREEN_WIDTH / 2, 150)
        self._draw_text(f"Dinero actual: ${self.snake.money}", self.font_small, YELLOW, SCREEN_WIDTH / 2, 220)
        
        # Muestra los ítems
        item_y_pos = 300
        for item_key, item_data in self.shop.items.items():
            desc = item_data["description"]
            cost = item_data["cost"]
            item_text = f"{desc} - Costo: {cost}"
            self._draw_text(item_text, self.font_small, WHITE, SCREEN_WIDTH / 2, item_y_pos)
            item_y_pos += 40

        self._draw_text("Presiona ESC para salir", self.font_small, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150)

    def _draw_text(self, text, font, color, x, y):
        """Función auxiliar para dibujar texto centrado."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

# --- Ejecución del Juego ---
if __name__ == '__main__':
    game = Game()
    game.run()
