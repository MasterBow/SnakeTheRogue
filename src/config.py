# config.py
"""
Archivo de Configuración Central.

Almacena todas las constantes, valores fijos y "números mágicos"
del juego en un solo lugar para que sean fáciles de modificar.
"""

# --- Dimensiones ---
SCREEN_WIDTH = 800      # Ancho de la ventana visible (en píxeles)
SCREEN_HEIGHT = 600     # Alto de la ventana visible (en píxeles)
WORLD_WIDTH = 2000      # Ancho total del mundo del juego
WORLD_HEIGHT = 2000     # Alto total del mundo del juego

# --- Colores (Tuplas RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (211, 47, 47)
GREEN = (76, 175, 80)
BLUE = (33, 150, 243)
YELLOW = (255, 235, 59)
PURPLE = (156, 39, 176)
ORANGE = (255, 152, 0)

# --- Configuración del Juego ---
# Control de velocidad
FPS = 60          # FPS de renderizado (para fluidez visual)
LOGIC_FPS = 15    # FPS de la lógica (velocidad de movimiento del juego)

# Configuración de entidades
SNAKE_SIZE = 20     # Tamaño de un solo segmento de la serpiente (en píxeles)
