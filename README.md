# 🐍 Snake The Rogue: RPG Edition

![Estado](https://img.shields.io/badge/Estado-Beta%20v0.3.0-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pygame](https://img.shields.io/badge/Library-Pygame-yellow)

**Juego tipo Snake con elementos Rogue-lite, desarrollado en Python y Pygame.**

Este proyecto expande la mecánica clásica de Snake transformándola en un **Action RPG** con mundo abierto, combate de proyectiles, progresión de personaje, enemigos con IA y persistencia de datos.

---

## ✨ Características Principales

### ⚔️ Combate y RPG
* **Mundo Abierto:** Un mapa masivo de `2000x2000` px explorado mediante una cámara de seguimiento.
* **Sistema de Disparo:** Mecánica de *"Twin-stick shooter"* simplificada (la serpiente dispara en la dirección de su movimiento).
* **Progresión por Niveles:** Gana XP comiendo. Al subir de nivel, aumentan tus estadísticas base (`+HP`, `+Daño`, `+Velocidad`) y recuperas salud.
* **Enemigos Inteligentes:** 3 tipos de enemigos (Normal, Tanque, Rápido) que utilizan vectores de persecución para cazar al jugador dinámicamente.
* **Dificultad Dinámica:** El juego escala en dificultad (aumento de daño enemigo) por cada 30 segundos de supervivencia.

### 💾 Persistencia y Tienda
* **Base de Datos SQLite:** El progreso (Max HP, Dinero, Mejoras) se guarda automáticamente en `rogue_snake.db`.
* **Tienda In-Game:** Sistema de economía para comprar curaciones o mejoras permanentes de estadísticas (Daño, Velocidad de Ataque, HP).

### 🎨 Motor "Out-of-the-Box" (Sin Dependencias Externas)
* **Assets Procedurales:** El juego genera sus propios gráficos (sprites geométricos) y efectos de sonido (ondas sintetizadas) si no encuentra archivos externos. **¡No requiere descargar imágenes para funcionar!**
* **Game Loop Híbrido:** Renderizado fluido a **60 FPS** interpolado con una lógica de juego clásica (grid-based) a **15 FPS**.
* **Interfaz Completa:** Menú principal animado, HUD detallado, opciones de volumen y pantalla de Game Over.

---

## 🚀 Instalación y Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/MasterBow/SnakeTheRogue.git](https://github.com/MasterBow/SnakeTheRogue.git)
    cd SnakeTheRogue
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install pygame
    ```

3.  **Ejecutar el juego:**
    ```bash
    python main.py
    ```

---

## 🎮 Controles

### Generales
| Contexto | Tecla | Acción |
| :--- | :---: | :--- |
| **Movimiento** | `Flechas` | Mover a la serpiente / Navegar Menú |
| **Combate** | `Espacio` | Disparar proyectil |
| **Interacción** | `E` | Entrar a la Tienda (zona morada) |
| **Menús** | `Enter` | Confirmar / Empezar Partida |
| **Sistema** | `ESC` | Pausa / Salir de Tienda / Volver |

### 🛒 Atajos de Tienda (Dentro de la zona de compra)
| Tecla | Costo | Efecto |
| :---: | :---: | :--- |
| `H` | **$15** | **Poción:** Restaura 50 HP (Instantáneo) |
| `U` | **$50** | **Upgrade HP:** +10 Max HP (Permanente) |
| `D` | **$75** | **Damage:** +5 Daño (Permanente) |
| `A` | **$120** | **Atk Speed:** Disparo más rápido (Permanente) |

---

## 📁 Estructura del Proyecto

El código sigue una **arquitectura modular** con separación de responsabilidades (MVC):

```text
snake_rogue_pygame/
├─ main.py           # Entry Point: Inicializa la instancia de Game.
├─ game.py           # Controlador: Bucle principal, estados y manejo de eventos.
├─ menu.py           # Vista: Manejo de menús y sprites de interfaz de usuario.
├─ config.py         # Configuración: Constantes globales y paleta de colores.
├─ database.py       # Modelo: Gestión de SQLite (Save/Load).
├─ snake.py          # Jugador: Lógica de movimiento, RPG y Audio Synth.
├─ enemy.py          # Entidad: IA de persecución y definición de enemigos.
├─ projectile.py     # Entidad: Física y colisiones de las balas.
├─ camera.py         # Motor: Conversión de coordenadas Mundo -> Pantalla.
├─ food.py           # Entidad: Comida (XP).
├─ shop.py           # Entidad: Lógica de la zona de tienda.
└─ rogue_snake.db    # Archivo de guardado (Auto-generado al jugar).
