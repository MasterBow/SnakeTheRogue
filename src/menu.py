# menu.py
"""
Clase Menu para manejar listas de opciones seleccionables.
"""
import pygame
import config as c

class Menu:
    def __init__(self, x, y, options):
        """
        x, y: Posición central del menú.
        options: Lista de strings ["Opcion 1", "Opcion 2"]
        """
        self.x = x
        self.y = y
        self.options = options
        self.selected_index = 0
        self.font = pygame.font.Font(None, 50)
        self.active = True

    def draw(self, surface):
        """Dibuja las opciones, resaltando la seleccionada."""
        for i, option in enumerate(self.options):
            color = c.YELLOW if i == self.selected_index else c.WHITE
            
            # Si estamos en la opción de volumen, mostramos el valor actual
            text_str = option
            if "Volumen" in option:
                vol_percent = int(c.MASTER_VOLUME * 100)
                text_str = f"{option}: {vol_percent}%"

            text_surf = self.font.render(text_str, True, color)
            rect = text_surf.get_rect(center=(self.x, self.y + i * 60))
            surface.blit(text_surf, rect)

    def handle_input(self, event):
        """Maneja la navegación (Arriba/Abajo/Enter). Devuelve la opción elegida o None."""
        if not self.active:
            return None

        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            return self.options[self.selected_index]
        
        # Manejo especial para volumen (Izquierda/Derecha)
        current_opt = self.options[self.selected_index]
        if "Volumen" in current_opt:
            if event.key == pygame.K_LEFT:
                c.MASTER_VOLUME = max(0.0, c.MASTER_VOLUME - 0.1)
            elif event.key == pygame.K_RIGHT:
                c.MASTER_VOLUME = min(1.0, c.MASTER_VOLUME + 0.1)
                
        return None