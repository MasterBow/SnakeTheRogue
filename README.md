# 🐍 Snake The Rogue: Un Juego de Snake con Elementos Rogue-like

Este documento describe la arquitectura, estructura de ficheros y el flujo del juego para un proyecto de **Snake The Rogue** implementado en Python, utilizando la librería `turtle` para la renderización.

---

## 🏗️ Diseño General (Visión en Capas)

El proyecto sigue una arquitectura clara de **separación de responsabilidades** (similar a MVC, pero enfocado en capas de juego) para garantizar la modularidad y la fácil extensibilidad.

| Capa | Responsabilidad | Módulos Clave |
| :--- | :--- | :--- |
| **Core (Lógica)** | Reglas de movimiento, actualización de estado, colisiones, gestión de niveles, IA básica. | `game.py`, `collision.py`, `enemies.py` |
| **Model (Datos)** | Almacenamiento y estado del mundo (Grid, entidades, score, vida). | `grid.py`, `snake.py`, `entity.py` |
| **Renderer (Presentación)** | Dibuja el Grid y las entidades usando `turtle`. Maneja optimizaciones de repintado. | `renderer_turtle.py`, `ui.py` |
| **Input / Control** | Captura de teclado y mapeo a acciones. | `input_handler.py` |
| **Persistence / Config** | Constantes del juego y funcionalidad de guardado/carga de progreso. | `config.py`, `save_load.py` |
| **Utils / Herramientas** | Generación de mapas, pathfinding (A* opcional), utilidades de log y pruebas. | `generator.py`, `utils.py` |

---

## 📁 Estructura de Ficheros Sugerida

La estructura modular propuesta para el proyecto es la siguiente:
```text
rogue_snake/
├─ src/
│ ├─ main.py # Entrada del programa; inicia la clase Game
│ ├─ config.py # Constantes del juego (GRID_SIZE, CELL_PIXELS, etc)
│ ├─ game.py # Clase Game principal (bucle, estados)
│ ├─ grid.py # Modelo Grid / Tile / Cell
│ ├─ snake.py # Clase Snake (implementación con collections.deque)
│ ├─ entity.py # Base Entity; clases Enemy, Food, Powerup extienden
│ ├─ enemies.py # EnemyManager y tipos de IA
│ ├─ generator.py # LevelGenerator (algoritmos procedurales)
│ ├─ renderer_turtle.py # Lógica de renderizado con turtle
│ ├─ input_handler.py # Mapeo de teclas y control
│ ├─ collision.py # Lógica de detección y respuesta a colisiones
│ ├─ ui.py # HUD, marcador, menús simples
│ ├─ save_load.py # Guardado/lectura de progreso en formato JSON
│ └─ utils.py # A*, random helpers, etc
├─ assets/ # Recursos visuales o definiciones (opcional)
├─ tests/ # Pruebas unitarias
└─ README.md # Este archivo
```
---

## ⚙️ Modelos de Datos Clave

### Grid
Representa el mundo del juego.

* `cells[y][x]`: Contiene el estado de la celda (Enum: `EMPTY`, `WALL`, `FOOD`, etc.).
* `occupied = set((x,y))`: Para comprobación rápida **O(1)** de disponibilidad de celdas.

### Snake
Representación de la serpiente.

* Implementación: `collections.deque` de coordenadas `[(x_head,y_head), ...]`.
* Propiedades: `direction` (enum `UP`/`DOWN`/`LEFT`/`RIGHT`).
* Métodos: `step(grow=False)`, `change_direction(dir)`, `collides(coord)`.

### Enemy / PowerUp
Representaciones de las entidades dinámicas.

* **Enemy**: `pos`, `type` (roaming, chasing), `state`, `hp`. Método clave: `decide_next_move(grid, snake_head)`.
* **PowerUp**: `{type, duration, effect}`.

---

## ⏳ Game Loop (Arquitectura y Flujo)

El bucle del juego se controlará mediante el modelo de *tick* asíncrono de `turtle` para **evitar el bucle `while True` bloqueante**.

### Pseudocódigo

```python
class Game:
    def start(self):
        self.state = RUNNING
        self.schedule_tick()

    def schedule_tick(self):
        # Llama a self.tick después de 'tick_ms' milisegundos
        turtle.ontimer(self.tick, int(self.tick_ms))

    def tick(self):
        if self.state != RUNNING: 
            return
            
        # 1. Lógica
        self.update_game_logic()
        
        # 2. Renderizado
        self.renderer.render_updates()
        
        # 3. Reprogramar
        self.schedule_tick()
Flujo de update_game_logic()
Mover serpiente: snake.step().

Checar colisión con comida, powerups, paredes, enemigos.

Mover enemigos (según su IA).

Generar nuevos items si es necesario.

Checar condiciones de fin de nivel o muerte.

🗺️ Generación Procedural de Niveles
La naturaleza rogue-like del juego se basará en la generación dinámica de niveles, gestionada por generator.py.

Opciones de Algoritmos (Simplicidad → Complejidad)
Random Walk: (Fácil) Comienza en el centro, camina al azar creando pasajes; coloca paredes alrededor.

Rooms + Corridors (BSP): (Recomendado para un clásico rogue-like) Particiona el mapa, crea habitaciones y las conecta con corredores.

Cellular Automata: Para mapas tipo cavernas/ambientación distinta.

API del Generador:

Python

class LevelGenerator:
    # Retorna el Grid, los puntos de aparición y los puntos de items
    def generate(level_number) -> Grid, spawn_points, item_spawns
🧠 IA Enemiga
La complejidad de la IA variará según el tipo de enemigo:

Roamer: Elige dirección aleatoria; evita paredes.

Patrol: Sigue una lista predefinida de waypoints.

Chaser: Si la distancia a la serpiente es menor a X, usa A* hacia la cabeza de la serpiente; si no, patrulla.

Fleeing: Huye si la serpiente es grande o tiene un powerup especial.

Optimización: Calcular A* solo cada N ticks y limitar la búsqueda a un rectángulo objetivo para mejorar el rendimiento.

🎨 Renderizado con Turtle (Optimizaciones)
Para mitigar la lentitud inherente de turtle:

Coordenadas: Usar coordenadas por celda y transformar a píxeles: pixel_x = cell_x * CELL_SIZE + offset.

Doble Buffer: Usar wn.tracer(0) y llamar wn.update() una sola vez por tick.

Repintado Selectivo: Mantener un buffer de "celdas cambiadas" y repintar solo esas celdas en cada tick.

Reuso de Objetos: Usar turtle.Turtle() por tipo de objeto y stamp() para dibujar las celdas, reusando el objeto en lugar de crear/destruir.

✅ Checklist de Implementación (Pasos Lógicos)
Esqueleto Inicial: Crear la estructura de carpetas, config.py y main.py.

Modelo Básico: Implementar Grid y un LevelGenerator simple (generación estática de prueba).

Núcleo de Movimiento: Implementar Snake, movimiento básico, input y renderer minimal.

Loop y Colisiones: Añadir comida, crecimiento, puntuación y la lógica de collision.py.

Enemigos: Añadir EnemyManager con IA simple (roamer).

Extensión: Añadir powerups y efectos temporales.

Pulido: Optimizar renderer, añadir HUD y menús.

Finalización: Implementar Tests unitarios y guardado/carga.
