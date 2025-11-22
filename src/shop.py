# shop.py
"""
Módulo de la Tienda.

Define la clase `Shop`, un objeto pasivo que:
- Existe en una posición fija (el centro).
- Contiene un diccionario de ítems a la venta.
- Sabe cómo dibujarse a sí mismo.
- 'Game' lo usa como un "trigger" para cambiar de estado.
"""

import pygame
import config as c

class Shop:
    """La tienda donde el jugador puede comprar mejoras."""
    
    def __init__(self):
        """Inicializa la tienda en el centro del mundo y define sus ítems."""
        self.rect = pygame.Rect(c.WORLD_WIDTH // 2 - 50, c.WORLD_HEIGHT // 2 - 50, 100, 100)
        
        # Diccionario de ítems (fácil de ampliar)
        self.items = {
            "health_potion": {
                "key": "H",
                "cost": 15, 
                "description": "[H] Poción (+50 HP)"
            },
            "hp_upgrade": {
                "key": "U",
                "cost": 100, 
                "description": "[U] Max HP (+10)"
            },
            "damage_upgrade": {
                "key": "D",
                "cost": 75, 
                "description": "[D] Daño (+5)"
            },
            "speed_upgrade": {
                "key": "A",
                "cost": 120, 
                "description": "[A] Vel. Ataque (Rapid Fire)"
            }
        }

    def draw(self, surface, camera):
        """Dibuja la tienda y su etiqueta (relativos a la cámara)."""
        pygame.draw.rect(surface, c.PURPLE, camera.apply(self.rect))
        
        # Dibuja la etiqueta "Tienda"
        font = pygame.font.Font(None, 24)
        text = font.render("Tienda", True, c.WHITE)
        text_rect = text.get_rect(center=camera.apply(self.rect).center)
        surface.blit(text, text_rect)