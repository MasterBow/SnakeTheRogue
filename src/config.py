# config.py
"""
Archivo de Configuración Central.
"""

import pygame 

# --- Dimensiones ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000

# --- Colores (como objetos pygame.Color) ---
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(211, 47, 47)
GREEN = pygame.Color(76, 175, 80)
BLUE = pygame.Color(33, 150, 243)
YELLOW = pygame.Color(255, 235, 59)
PURPLE = pygame.Color(156, 39, 176)
ORANGE = pygame.Color(255, 152, 0)
GRAY = pygame.Color(100, 100, 100)
DARK_BLUE = pygame.Color(0, 0, 139) # Color para el Tanque

# --- Colores Pre-calculados ---
HP_BAR_BG = RED.lerp(BLACK, 0.5)

# --- Configuración del Juego ---
FPS = 60
LOGIC_FPS = 15
SNAKE_SIZE = 20

# --- Configuración de Audio ---
MASTER_VOLUME = 0.5