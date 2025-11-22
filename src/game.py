# game.py
"""
El Módulo "Game" (El Cerebro/Orquestador).
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
import database
from menu import Menu 

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake The Rogue")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        
        database.create_tables()
        
        self.state = 'main_menu' 
        
        self.main_menu_obj = Menu(c.SCREEN_WIDTH // 2, 250, [
            "Continuar Partida", 
            "Nueva Partida", 
            "Opciones", 
            "Salir"
        ])
        
        self.options_menu_obj = Menu(c.SCREEN_WIDTH // 2, 250, [
            "Volumen", 
            "Volver"
        ])
        
        self.setup_game()
        
        self.logic_interval = 1.0 / c.LOGIC_FPS
        self.logic_timer = 0.0
        self.start_time = pygame.time.get_ticks()

    def setup_game(self):
        self.snake = Snake() 
        self.enemies = [Enemy() for _ in range(15)]
        self.foods = [Food() for _ in range(20)]
        self.shop = Shop()
        self.camera = Camera(c.WORLD_WIDTH, c.WORLD_HEIGHT)
        self.projectiles = [] 
        self.start_time = pygame.time.get_ticks()

    def get_difficulty_multiplier(self):
        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - self.start_time) / 1000.0
        difficulty_level = int(elapsed_seconds / 30) 
        extra_damage = difficulty_level * 5
        return extra_damage

    def run(self):
        while True:
            dt_ms = self.clock.tick(c.FPS)
            dt_seconds = dt_ms / 1000.0
            self.logic_timer += dt_seconds
            
            self.events()

            if self.logic_timer >= self.logic_interval:
                self.update() 
                self.logic_timer -= self.logic_interval 
            
            self.draw()
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.snake.save_stats()
                pygame.quit()
                sys.exit()
            
            if self.state == 'main_menu':
                if event.type == pygame.KEYDOWN:
                    selection = self.main_menu_obj.handle_input(event)
                    
                    if selection == "Continuar Partida":
                        self.snake.reset() 
                        self.state = 'playing'
                        self.snake.direction = pygame.Vector2(1, 0)
                        self.start_time = pygame.time.get_ticks()
                        
                    elif selection == "Nueva Partida":
                        database.reset_player_data()
                        self.setup_game()
                        self.state = 'playing'
                        self.snake.direction = pygame.Vector2(1, 0)
                        
                    elif selection == "Opciones":
                        self.state = 'options_menu'
                        
                    elif selection == "Salir":
                        pygame.quit()
                        sys.exit()

            elif self.state == 'options_menu':
                if event.type == pygame.KEYDOWN:
                    selection = self.options_menu_obj.handle_input(event)
                    if selection == "Volver" or event.key == pygame.K_ESCAPE:
                        self.state = 'main_menu'

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
                    elif event.key == pygame.K_SPACE:
                        new_projectile = self.snake.shoot() 
                        if new_projectile:
                            self.projectiles.append(new_projectile)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = 'main_menu' 

            elif self.state == 'shop':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'playing' 
                    
                    elif event.key == pygame.K_h:
                        cost = self.shop.items["health_potion"]["cost"]
                        if self.snake.money >= cost:
                            self.snake.money -= cost
                            self.snake.hp = min(self.snake.max_hp, self.snake.hp + 50)

                    elif event.key == pygame.K_u: 
                        cost = self.shop.items["hp_upgrade"]["cost"]
                        if self.snake.money >= cost:
                            self.snake.money -= cost
                            self.snake.max_hp += 10
                            self.snake.hp = self.snake.max_hp 
                            self.snake.save_stats()

                    elif event.key == pygame.K_d: 
                        cost = self.shop.items["damage_upgrade"]["cost"]
                        if self.snake.money >= cost:
                            self.snake.money -= cost
                            self.snake.attack_damage += 5
                            self.snake.save_stats()

                    elif event.key == pygame.K_a: 
                        cost = self.shop.items["speed_upgrade"]["cost"]
                        if self.snake.money >= cost:
                            self.snake.money -= cost
                            self.snake.attack_speed = max(100, self.snake.attack_speed - 50)
                            self.snake.save_stats()
            
            elif self.state == 'game_over':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.setup_game() 
                    self.state = 'main_menu'

    def update(self):
        if self.state != 'playing':
            return 

        self.snake.move()
        self.camera.update(self.snake.get_head()) 

        head = self.snake.get_head()
        
        base_damage = 20
        extra_damage = self.get_difficulty_multiplier()
        current_enemy_damage = base_damage + extra_damage

        for projectile in self.projectiles[:]: 
            projectile.move()
            if not (0 <= projectile.rect.x < c.WORLD_WIDTH and 0 <= projectile.rect.y < c.WORLD_HEIGHT):
                self.projectiles.remove(projectile)
                continue 

            hit_an_enemy = False
            for enemy in self.enemies[:]:
                if projectile.rect.colliderect(enemy.rect):
                    enemy.hp -= projectile.damage
                    hit_an_enemy = True
                    if enemy.hp <= 0: 
                        self.enemies.remove(enemy)
                        self.snake.add_score(enemy.score_value) 
                        self.snake.money += 5 
                        self.enemies.append(Enemy()) 
                    break 
            
            if hit_an_enemy:
                self.projectiles.remove(projectile)
        
        for food in self.foods[:]:
            if head.colliderect(food.rect):
                self.foods.remove(food)
                self.snake.grow() # Aquí se reproduce el sonido y se gana XP
                self.foods.append(Food()) 
                self.snake.add_score(10)
                break
        
        for enemy in self.enemies[:]:
            # 1. Mover al enemigo hacia el jugador
            enemy.move(head) 
            
            # 2. Comprobar si toca al jugador
            if head.colliderect(enemy.rect):
                self.snake.take_damage(current_enemy_damage) 
                # No 'break' aquí para permitir que múltiples enemigos golpeen si te rodean
        
        if not (0 <= head.x < c.WORLD_WIDTH and 0 <= head.y < c.WORLD_HEIGHT):
            self.snake.take_damage(100) 

        for segment in self.snake.body[1:]:
            if head.colliderect(segment):
                self.snake.take_damage(100)
                break
        
        if self.snake.hp <= 0:
            self.state = 'game_over'

    def draw(self):
        self.screen.fill(c.BLACK)
        
        if self.state == 'main_menu':
            self._draw_text("SNAKE THE ROGUE", self.font_large, c.GREEN, c.SCREEN_WIDTH / 2, 100)
            self._draw_text("Usa Flechas y Enter", self.font_small, c.GRAY, c.SCREEN_WIDTH / 2, 160)
            self.main_menu_obj.draw(self.screen)

        elif self.state == 'options_menu':
            self._draw_text("OPCIONES", self.font_large, c.BLUE, c.SCREEN_WIDTH / 2, 100)
            self._draw_text("Izquierda/Derecha para ajustar", self.font_small, c.GRAY, c.SCREEN_WIDTH / 2, 160)
            self.options_menu_obj.draw(self.screen)

        elif self.state == 'playing':
            self._draw_world()
            self._draw_hud()

        elif self.state == 'shop':
            self._draw_world() 
            self._draw_shop_menu() 

        elif self.state == 'game_over':
            self._draw_text("GAME OVER", self.font_large, c.RED, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 3)
            self._draw_text(f"Puntaje Final: {self.snake.score}", self.font_small, c.YELLOW, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 50)
            self._draw_text("Presiona ENTER para Menú", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2)

    def _draw_world(self):
        self.shop.draw(self.screen, self.camera)
        for food in self.foods:
            food.draw(self.screen, self.camera)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)
        for projectile in self.projectiles:
            projectile.draw(self.screen, self.camera)
        self.snake.draw(self.screen, self.camera)

    def _draw_hud(self):
        # --- INDICADOR DE HP Y NIVEL ---
        # Ejemplo: "HP: 100 / 100  |  Lvl: 5"
        hp_str = f"HP: {self.snake.hp} / {self.snake.max_hp}"
        lvl_str = f"Lvl: {self.snake.level}"
        
        full_status_str = f"{hp_str}   |   {lvl_str}"
        status_text = self.font_small.render(full_status_str, True, c.WHITE)
        self.screen.blit(status_text, (10, 10))
        # ------------------------------
        
        money_text = self.font_small.render(f"Dinero: ${self.snake.money}", True, c.YELLOW)
        self.screen.blit(money_text, (10, 50))
        
        extra_dmg = self.get_difficulty_multiplier()
        if extra_dmg > 0:
            diff_text = self.font_small.render(f"Peligro: +{extra_dmg} DMG", True, c.RED)
            self.screen.blit(diff_text, (10, 90))
        
        time_since_last = pygame.time.get_ticks() - self.snake.last_score_time
        score_color = c.WHITE
        score_suffix = ""
        
        if time_since_last > 8000: 
            score_color = c.RED 
            if time_since_last > 10000:
                score_suffix = " v" 
            else:
                score_suffix = " !" 

        score_text = self.font_small.render(f"Score: {self.snake.score}{score_suffix}", True, score_color)
        score_rect = score_text.get_rect(topright=(c.SCREEN_WIDTH - 20, 10))
        self.screen.blit(score_text, score_rect)
        
        if self.snake.get_head().colliderect(self.shop.rect):
            shop_prompt = self.font_small.render("Presiona [E] para entrar a la tienda", True, c.PURPLE)
            self.screen.blit(shop_prompt, (c.SCREEN_WIDTH / 2 - shop_prompt.get_width() / 2, c.SCREEN_HEIGHT - 50))

    def _draw_shop_menu(self):
        panel = pygame.Surface((c.SCREEN_WIDTH - 200, c.SCREEN_HEIGHT - 200), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        self.screen.blit(panel, (100, 100))
        
        self._draw_text("Tienda", self.font_large, c.PURPLE, c.SCREEN_WIDTH / 2, 150)
        self._draw_text(f"Dinero actual: ${self.snake.money}", self.font_small, c.YELLOW, c.SCREEN_WIDTH / 2, 220)
        
        item_y_pos = 280
        for item_key, item_data in self.shop.items.items():
            desc = item_data["description"]
            cost = item_data["cost"]
            item_text = f"{desc} - Costo: ${cost}"
            self._draw_text(item_text, self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, item_y_pos)
            item_y_pos += 50

        self._draw_text("Presiona ESC para salir", self.font_small, c.WHITE, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT - 100)

    def _draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)