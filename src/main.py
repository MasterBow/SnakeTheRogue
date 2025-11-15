# main.py
"""
Punto de Entrada Principal del Juego Snake The Rogue.

Este archivo tiene la única responsabilidad de:
1. Importar la clase principal del juego (Game).
2. Crear una instancia de la clase Game.
3. Ejecutar el bucle principal del juego.
"""

# Importa la clase Game desde nuestro módulo 'game'
from game import Game

if __name__ == '__main__':
    # Crea una instancia del juego
    game_instance = Game()
    
    # Inicia el bucle principal del juego
    game_instance.run()
