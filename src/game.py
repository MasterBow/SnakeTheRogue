# game.py
"""
El Módulo "Game" (El Cerebro/Orquestador).

Contiene la clase principal `Game` que:
- Inicializa Pygame y la base de datos.
- Contiene el bucle principal del juego (`run`).
- Implementa una máquina de estados (`self.state`) para manejar menús, juego, etc.
- Gestiona los eventos de usuario (`events`).
- Gestiona la lógica (actualizaciones, colisiones) a un ritmo fijo (`update`).
- Gestiona el renderizado (dibujado) a 60 FPS (`draw`).
"""

import pygame
import sys
import config as c
from snake import Snake
from enemy import Enemy
from food import Food
from shop import Shop
from camera import Camera
from projectile import Projectile
import database  # Importa nuestro módulo de base de datos

class Game:
    """Orquesta todo el juego: bucle, estados, eventos y renderizado."""
    
    def __init__(self):
        """Inicializa Pygame, la pantalla, el reloj y la base de datos."""
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake con Esteroides")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        
        # Se asegura de que el archivo .db y las tablas existan al inicio
        database.create_tables()
        
        # Inicializa el estado del juego
        self.state = 'main_menu' 
        
        # Configura las entidades del juego
        self.setup_game()
        
        # --- Lógica de Timestep Fijo ---
        # Intervalo de tiempo entre ticks de lógica (ej. 1/15 = 0.066 segundos)
        self.logic_interval = 1.0 / c.LOGIC_FPS
        self.logic_timer = 0.0 # Acumulador de tiempo

    def setup_game(self):
        """
        Configura o resetea las entidades del juego.
        Llamado al inicio y al reiniciar desde "Game Over".
        """
        # Snake() ahora cargará automáticamente los datos de la DB
        self.snake = Snake() 
        self.enemies = [Enemy() for _ in range(15)]
        self.foods = [Food() for _ in range(20)]
        self.shop = Shop()
        self.camera = Camera(c.WORLD_WIDTH, c.WORLD_HEIGHT)
        self.projectiles = [] # Lista para almacenar balas activas

    def run(self):
        """
        Bucle principal del juego.
        Implementa un timestep fijo para separar la lógica del renderizado.
        """
        while True:
            # --- Nuevo Bucle de Timestep Fijo ---
            
            # 1. Calcular Delta Time (dt)
            # .tick(c.FPS) limita el renderizado a 60 FPS
            dt_ms = self.clock.tick(c.FPS)
            # Convertimos ms a segundos (ej. 16.6ms -> 0.0166s)
            dt_seconds = dt_ms / 1000.0
            
            # 2. Acumular tiempo para la lógica
            self.logic_timer += dt_seconds
            
            # 3. Manejar eventos (Input)
            # Se ejecuta cada frame (60 FPS) para respuesta instantánea
            self.events()

            # 4. Correr la Lógica (Update) en su propio ritmo (15 FPS)
            # Si ha pasado suficiente tiempo, corre un tick de lógica
            if self.logic_timer >= self.logic_interval:
                self.update() # <-- Aquí se mueve la serpiente
                self.logic_timer -= self.logic_interval # Resetea el temporizador
            
            # 5. Dibujar (Render)
            # Se ejecuta cada frame (60 FPS) para fluidez visual
            self.draw()
            pygame.display.flip()

    def events(self):
        """Maneja todas las entradas del usuario (teclado, ratón) basado en el estado."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # ¡Guardar el progreso antes de salir!
                print("Cerrando y guardando datos...")
                # Solo guardamos el dinero y las stats al salir
                self.snake.save_stats() 
                pygame.quit()
                sys.exit()
            
            # --- Eventos según el estado del juego ---
            if self.state == 'main_menu':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = 'playing'
                    self.snake.direction = pygame.Vector2(1, 0) # Inicia el movimiento
            
            elif self.state == 'playing':
                if event.type == pygame.KEYDOWN:
                    # Movimiento
                    if event.key == pygame.K_UP and self.snake.direction.y == 0:
                        self.snake.direction = pygame.Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and self.snake.direction.y == 0:
                        self.snake.direction = pygame.Vector2(0, 1)
                    elif event.key == pygame.K_LEFT and self.snake.direction.x == 0:
                        self.snake.direction = pygame.Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT and self.snake.direction.x == 0:
                        self.snake.direction = pygame.Vector2(1, 0)
                    # Acciones
                    elif event.key == pygame.K_e and self.snake.get_head().colliderect(self.shop.rect):
                        self.state = 'shop' # Entrar a la tienda
                    elif event.key == pygame.K_SPACE:
                        new_projectile = self.snake.shoot() # Intentar disparar
                        if new_projectile:
                            self.projectiles.append(new_projectile)

            elif self.state == 'shop':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'playing' # Salir de la tienda
                    # Comprar Poción (temporal)
                    elif event.key == pygame.K_h:
                        potion_cost = self.shop.items["health_potion"]["cost"]
                        if self.snake.money >= potion_cost:
                            self.snake.money -= potion_cost
                            self.snake.hp = min(self.snake.max_hp, self.snake.hp + 50)
                    # Comprar Mejora (permanente)
                    elif event.key == pygame.K_u: 
                        item_cost = self.shop.items["hp_upgrade"]["cost"]
                        if self.snake.money >= item_cost:
                            self.snake.money -= item_cost
                            self.snake.max_hp += 10
                            self.snake.hp = self.snake.max_hp # Curar al máximo
                            print(f"¡Mejora comprada! Max HP ahora es {self.snake.max_hp}")
                            
                            # --- ¡¡AQUÍ ESTÁ EL ARREGLO!! ---
                            # Guardamos inmediatamente la mejora permanente en la DB.
                            self.snake.save_stats()
                            # --- FIN DEL ARREGLO ---
            
            elif self.state == 'game_over':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # --- LÓGICA DE MUERTE (ROGUE-LIKE) ---
                    # Al morir, *no* guardamos el dinero de la sesión.
                    # Simplemente reiniciamos, lo que recarga
                    # las stats permanentes (HP Max) y el dinero base.
                    self.setup_game() 
                    self.state = 'main_menu'

    def update(self):
        """Actualiza toda la lógica del juego (movimiento, colisiones). Se ejecuta a 15 FPS."""
        if self.state != 'playing':
            return # No actualiza nada si no estamos jugando

        # Mover entidades
        self.snake.move()
        self.camera.update(self.snake.get_head()) # La cámara sigue a la serpiente

        head = self.snake.get_head()
        
        # --- Lógica de Proyectiles ---
        for projectile in self.projectiles[:]: # [:] para iterar sobre una copia
            projectile.move()
            
            # Eliminar proyectil si sale del mundo
            if not (0 <= projectile.rect.x < c.WORLD_WIDTH and 0 <= projectile.rect.y < c.WORLD_HEIGHT):
                self.projectiles.remove(projectile)
                continue 

            # Comprobar colisión de proyectil con enemigos
            hit_an_enemy = False
            for enemy in self.enemies[:]:
                if projectile.rect.colliderect(enemy.rect):
                    enemy.hp -= projectile.damage
                    hit_an_enemy = True
                    
                    if enemy.hp <= 0: # Enemigo murió
                        self.enemies.remove(enemy)
                        self.enemies.append(Enemy()) # Reaparece en otro lugar
                        self.snake.money += 5
                    
                    break # El proyectil solo golpea a un enemigo
            
            if hit_an_enemy:
                self.projectiles.remove(projectile)
        
        # --- Lógica de Colisiones de la Serpiente ---
        
        # Con comida
        for food in self.foods[:]:
            if head.colliderect(food.rect):
                self.foods.remove(food)
                self.snake.grow()
                self.foods.append(Food()) # Añade nueva comida
                break
        
        # Con enemigos (chocar)
        for enemy in self.enemies[:]:
            if head.colliderect(enemy.rect):
                self.snake.take_damage(20) # La serpiente recibe daño
                break
        
        # Con bordes del mundo
        if not (0 <= head.x < c.WORLD_WIDTH and 0 <= head.y < c.WORLD_HEIGHT):
            self.snake.take_damage(100) # Morir al chocar

        # Con su propio cuerpo
        for segment in self.snake.body[1:]:
            if head.colliderect(segment):
                self.snake.take_damage(100)
                break
        
        # --- Comprobar Muerte ---
        if self.snake.hp <= 0:
            self.state = 'game_over'

    def draw(self):
        """Dibuja todo en la pantalla según el estado. Se ejecuta a 60 FPS."""
        self.screen.fill(c.BLACK)
        
        if self.state == 'main_menu':
            self._draw_text("Snake con Esteroides", self.font_large, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 3)
            self._draw_text("Presiona ENTER para comenzar", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2)
            self._draw_text("Muévete con las flechas", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT * 2 / 3)

        elif self.state == 'playing':
            self._draw_world()
            self._draw_hud()

        elif self.state == 'shop':
            self._draw_world() # Dibuja el mundo de fondo
            self._draw_shop_menu() # Dibuja el menú de la tienda encima

        elif self.state == 'game_over':
            self._draw_text("Game Over", self.font_large, c.RED, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 3)
            self._draw_text("Presiona ENTER para volver al menú", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2)

    def _draw_world(self):
        """Dibuja todos los objetos del juego (relativos a la cámara)."""
        # El orden de dibujado importa (de atrás hacia adelante)
        self.shop.draw(self.screen, self.camera)
        
        for food in self.foods:
            food.draw(self.screen, self.camera)
            
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)
            
        for projectile in self.projectiles:
            projectile.draw(self.screen, self.camera)
            
        self.snake.draw(self.screen, self.camera)

    def _draw_hud(self):
        """Dibuja la interfaz de usuario (HP, dinero) en la pantalla."""
        # Barra de vida
        hp_text = self.font_small.render(f"HP: {self.snake.hp} / {self.snake.max_hp}", True, c.WHITE)
        self.screen.blit(hp_text, (10, 10))
        # Dinero
        money_text = self.font_small.render(f"Dinero: ${self.snake.money}", True, c.YELLOW)
        self.screen.blit(money_text, (10, 50))
        
        # Mensaje de la tienda (si está cerca)
        if self.snake.get_head().colliderect(self.shop.rect):
            shop_prompt = self.font_small.render("Presiona [E] para entrar a la tienda", True, c.PURPLE)
            self.screen.blit(shop_prompt, (c.SCREEN_WIDTH / 2 - shop_prompt.get_width() / 2, c.SCREEN_HEIGHT - 50))

    def _draw_shop_menu(self):
        """Dibuja la interfaz de la tienda."""
        # Dibuja un panel semitransparente
        panel = pygame.Surface((c.SCREEN_WIDTH - 200, c.SCREEN_HEIGHT - 200), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        self.screen.blit(panel, (100, 100))
        
        # Dibuja los textos
        self._draw_text("Tienda", self.font_large, c.PURPLE, c.SCREEN_WIDTH / 2, 150)
        self._draw_text(f"Dinero actual: ${self.snake.money}", self.font_small, c.YELLOW, c.SCREEN_WIDTH / 2, 220)
        
        # Itera sobre los ítems y los muestra
        item_y_pos = 300
        for item_key, item_data in self.shop.items.items():
            desc = item_data["description"]
            cost = item_data["cost"]
            item_text = f"{desc} - Costo: {cost}"
            self._draw_text(item_text, self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, item_y_pos)
            item_y_pos += 40

        self._draw_text("Presiona ESC para salir", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT - 150)

    # --- ¡¡AQUÍ ESTÁ EL ARREGLO!! ---
    # Cambiado de 'self.text' a 'self, text'
    def _draw_text(self, text, font, color, x, y):
        """Función auxiliar para dibujar texto centrado en (x, y)."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
