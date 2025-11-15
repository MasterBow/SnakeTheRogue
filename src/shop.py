# shop.py

import pygame
import config as c

class Shop:
    """La tienda donde el jugador puede comprar mejoras."""
    def __init__(self):
        # La tienda está en el centro del mundo
        self.rect = pygame.Rect(c.WORLD_WIDTH // 2 - 50, c.WORLD_HEIGHT // 2 - 50, 100, 100)
        self.items = {
            "health_potion": {"cost": 15, "description": "Restaura 50 HP (H)"},
        }

    def draw(self, surface, camera):
        """Dibuja la tienda relativa a la cámara."""
        pygame.draw.rect(surface, c.PURPLE, camera.apply(self.rect))
        font = pygame.font.Font(None, 24)
        text = font.render("Tienda", True, c.WHITE)
        text_rect = text.get_rect(center=camera.apply(self.rect).center)
        surface.blit(text, text_rect)
