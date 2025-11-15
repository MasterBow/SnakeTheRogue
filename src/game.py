# game.py

import pygame
import sys
import config as c
from snake import Snake
from enemy import Enemy
from food import Food
from shop import Shop
from camera import Camera

class Game:
    """Orquesta todo el juego: bucle, estados, eventos y renderizado."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
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
        self.camera = Camera(c.WORLD_WIDTH, c.WORLD_HEIGHT)

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
                    elif event.key == pygame.K_e and self.snake.get_head().colliderect(self.shop.rect):
                        self.state = 'shop'

            elif self.state == 'shop':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'playing'
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
            return 

        self.snake.move()
        self.camera.update(self.snake.get_head())

        head = self.snake.get_head()
        for food in self.foods[:]:
            if head.colliderect(food.rect):
                self.foods.remove(food)
                self.snake.grow()
                self.foods.append(Food())
                break
        
        for enemy in self.enemies[:]:
            if head.colliderect(enemy.rect):
                self.snake.take_damage(20)
                self.enemies.remove(enemy)
                self.enemies.append(Enemy())
                self.snake.money += 5
                break
        
        if not (0 <= head.x < c.WORLD_WIDTH and 0 <= head.y < c.WORLD_HEIGHT):
            self.snake.take_damage(100)

        for segment in self.snake.body[1:]:
            if head.colliderect(segment):
                self.snake.take_damage(100)
                break
        
        if self.snake.hp <= 0:
            self.state = 'game_over'

    def draw(self):
        """Dibuja todo en la pantalla según el estado."""
        self.screen.fill(c.BLACK)
        
        if self.state == 'main_menu':
            self._draw_text("Snake con Esteroides", self.font_large, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 3)
            self._draw_text("Presiona ENTER para comenzar", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2)
            self._draw_text("Muévete con las flechas", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT * 2 / 3)

        elif self.state == 'playing':
            self._draw_world()
            self._draw_hud()

        elif self.state == 'shop':
            self._draw_world()
            self._draw_shop_menu()

        elif self.state == 'game_over':
            self._draw_text("Game Over", self.font_large, c.RED, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 3)
            self._draw_text("Presiona ENTER para volver al menú", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2)

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
        hp_text = self.font_small.render(f"HP: {self.snake.hp} / {self.snake.max_hp}", True, c.WHITE)
        self.screen.blit(hp_text, (10, 10))
        money_text = self.font_small.render(f"Dinero: ${self.snake.money}", True, c.YELLOW)
        self.screen.blit(money_text, (10, 50))
        if self.snake.get_head().colliderect(self.shop.rect):
            shop_prompt = self.font_small.render("Presiona [E] para entrar a la tienda", True, c.PURPLE)
            self.screen.blit(shop_prompt, (c.SCREEN_WIDTH / 2 - shop_prompt.get_width() / 2, c.SCREEN_HEIGHT - 50))

    def _draw_shop_menu(self):
        """Dibuja la interfaz de la tienda."""
        panel = pygame.Surface((c.SCREEN_WIDTH - 200, c.SCREEN_HEIGHT - 200), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        self.screen.blit(panel, (100, 100))
        
        self._draw_text("Tienda", self.font_large, c.PURPLE, c.SCREEN_WIDTH / 2, 150)
        self._draw_text(f"Dinero actual: ${self.snake.money}", self.font_small, c.YELLOW, c.SCREEN_WIDTH / 2, 220)
        
        item_y_pos = 300
        for item_key, item_data in self.shop.items.items():
            desc = item_data["description"]
            cost = item_data["cost"]
            item_text = f"{desc} - Costo: {cost}"
            self._draw_text(item_text, self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, item_y_pos)
            item_y_pos += 40

        self._draw_text("Presiona ESC para salir", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT - 150)

    def _draw_text(self, text, font, color, x, y):
        """Función auxiliar para dibujar texto centrado."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
