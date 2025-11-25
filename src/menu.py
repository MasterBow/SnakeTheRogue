# menu.py
##Practica 5-6 terminadas. 
"""
Clase Menu para manejar listas de opciones seleccionables.
Incluye un sprite de flecha (cursor) que rota según la dirección presionada.
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
      ##Practica 5-6 terminadas.   
        # --- SPRITE DEL CURSOR (FLECHA) ---
        # 0=Derecha, 90=Arriba, 180=Izquierda, 270=Abajo
        self.arrow_angle = 0 
        self.arrow_surf = None
        
        try:
            # 1. Cargar imagen y convertir alpha para transparencia perfecta
            original_arrow = pygame.image.load("arrow.png").convert_alpha()
            
            # 2. Escalar a un tamaño consistente (40x40 px)
            self.arrow_surf = pygame.transform.scale(original_arrow, (40, 40))
            print("Imagen 'arrow.png' cargada correctamente.")
            
        except (FileNotFoundError, pygame.error):
            print("Aviso: 'arrow.png' no encontrado. Usando cursor procedural.")
            # Fallback: Triángulo procedural apuntando a la DERECHA por defecto
            self.arrow_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            
            # Dibujar triángulo verde: [(x,y), (x,y), (x,y)]
            # Puntos: (Arriba-Izq), (Abajo-Izq), (Centro-Der)
            # Esto crea una forma de "Play" (►)
            pygame.draw.polygon(self.arrow_surf, c.GREEN, [(0, 0), (0, 40), (40, 20)])

    def draw(self, surface):
        """Dibuja las opciones y la flecha selectora."""
        for i, option in enumerate(self.options):
            # Color del texto (resaltado si está seleccionado)
            color = c.YELLOW if i == self.selected_index else c.WHITE
            
            # Texto especial para el volumen (mostramos porcentaje)
            text_str = option
            if "Volumen" in option:
                vol_percent = int(c.MASTER_VOLUME * 100)
                text_str = f"{option}: {vol_percent}%"

            text_surf = self.font.render(text_str, True, color)
            rect = text_surf.get_rect(center=(self.x, self.y + i * 60))
            surface.blit(text_surf, rect)
            
            # --- DIBUJAR FLECHA SOLO EN LA OPCIÓN SELECCIONADA ---
            if i == self.selected_index:
                # 1. Rotamos el sprite original según el ángulo actual
                # pygame.transform.rotate gira en sentido antihorario
                rotated_arrow = pygame.transform.rotate(self.arrow_surf, self.arrow_angle)
                
                # 2. Obtenemos el rect para centrar la rotación correctamente
                # La colocamos 30 px a la izquierda del texto
                arrow_rect = rotated_arrow.get_rect(midright=(rect.left - 20, rect.centery))
                
                surface.blit(rotated_arrow, arrow_rect)

    def handle_input(self, event):
        """Maneja la navegación y actualiza la dirección de la flecha."""
        if not self.active:
            return None

        # Navegación Arriba / Abajo
        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
            self.arrow_angle = 90 # Apunta ARRIBA
            
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
            self.arrow_angle = 270 # Apunta ABAJO (o -90)
            
        elif event.key == pygame.K_RETURN:
            # Apuntar a la derecha al seleccionar (efecto visual de "entrar")
            self.arrow_angle = 0 
            return self.options[self.selected_index]
        
        # Manejo especial para la opción de volumen (Izquierda/Derecha)
        current_opt = self.options[self.selected_index]
        if "Volumen" in current_opt:
            if event.key == pygame.K_LEFT:
                c.MASTER_VOLUME = max(0.0, c.MASTER_VOLUME - 0.1)
                self.arrow_angle = 180 # Apunta IZQUIERDA
            elif event.key == pygame.K_RIGHT:
                c.MASTER_VOLUME = min(1.0, c.MASTER_VOLUME + 0.1)
                self.arrow_angle = 0 # Apunta DERECHA
        
        # Feedback visual si presionas izq/der en otras opciones (aunque no hagan nada)
        elif event.key == pygame.K_LEFT:
            self.arrow_angle = 180
        elif event.key == pygame.K_RIGHT:
            self.arrow_angle = 0
                
        return None
