# camera.py
"""
Módulo de la Cámara.

Define la clase `Camera`, que gestiona la vista del jugador
en un mundo más grande que la pantalla.
"""

import pygame
import config as c

class Camera:
    """
    Sigue a un objeto (el jugador) y convierte las coordenadas
    del "Mundo" a coordenadas de "Pantalla".
    """
    
    def __init__(self, world_width, world_height):
        """Inicializa la cámara con el tamaño del mundo."""
        # self.camera es un Rect que representa la "vista" (ej. 800x600)
        # Su posición (topleft) será negativa, indicando el desfase
        self.camera = pygame.Rect(0, 0, world_width, world_height)
        self.width = world_width
        self.height = world_height

    def apply(self, entity_rect):
        """
        Convierte un Rect del "Mundo" a un Rect de "Pantalla".
        Ej: Serpiente en (1000, 800) -> Dibuja en (400, 300)
        """
        # Suma el desfase (negativo) de la cámara a la posición de la entidad
        return entity_rect.move(self.camera.left, self.camera.top)

    def update(self, target_rect):
        """
        Actualiza la posición de la cámara para centrarse en el 'target' (la serpiente).
        """
        # Calcula la posición ideal para centrar al 'target' en la pantalla
        x = -target_rect.centerx + int(c.SCREEN_WIDTH / 2)
        y = -target_rect.centery + int(c.SCREEN_HEIGHT / 2)

        # Limita el scroll a los bordes del mundo (para no ver "fuera del mapa")
        x = min(0, x)  # Borde izquierdo
        y = min(0, y)  # Borde superior
        x = max(-(self.width - c.SCREEN_WIDTH), x)   # Borde derecho
        y = max(-(self.height - c.SCREEN_HEIGHT), y) # Borde inferior
        
        # Actualiza la posición de la cámara
        self.camera = pygame.Rect(x, y, self.width, self.height)
