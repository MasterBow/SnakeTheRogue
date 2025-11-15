# camera.py

import pygame
import config as c

class Camera:
    """Sigue al jugador y gestiona las coordenadas del mundo vs. pantalla."""
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity_rect):
        """Convierte coordenadas del mundo a coordenadas de pantalla."""
        # ▼▼▼ ESTA ES LA LÍNEA CORRECTA ▼▼▼
        return entity_rect.move(self.camera.left, self.camera.top)

    def update(self, target_rect):
        """Actualiza la posición de la cámara para centrarse en el objetivo."""
        x = -target_rect.centerx + int(c.SCREEN_WIDTH / 2)
        y = -target_rect.centery + int(c.SCREEN_HEIGHT / 2)

        # Limita el scroll a los bordes del mundo
        x = min(0, x)  # Borde izquierdo
        y = min(0, y)  # Borde superior
        x = max(-(self.width - c.SCREEN_WIDTH), x)   # Borde derecho
        y = max(-(self.height - c.SCREEN_HEIGHT), y) # Borde inferior
        
        self.camera = pygame.Rect(x, y, self.width, self.height)
