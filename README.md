**🐍 Snake The Rogue**

Juego tipo Snake desarrollado con Python y Pygame.

Este documento describe la arquitectura, estructura de archivos y flujo interno del proyecto. El juego expande la idea clásica de Snake hacia un pequeño roguelite con mundo abierto, combate, progresión y guardado persistente.

Estado actual: La base modular del juego está completa. El sistema de combate, estadísticas, mundo con cámara, guardado en SQLite y un bucle de juego con lógica desacoplada del render ya funcionan correctamente.

**Características Implementadas**

Mundo Abierto con Cámara: La serpiente se mueve en un mundo grande (2000x2000 px). Una cámara sigue al jugador en lugar de limitar todo a una sola pantalla.

Combate y Estadísticas: La serpiente cuenta con HP, dinero y atributos como daño y velocidad de ataque.

Sistema de Disparo: Presiona Espacio para disparar en la dirección actual del movimiento.

Enemigos con HP: Los enemigos tienen vida propia y requieren proyectiles para ser derrotados.

Progresión y Tienda: Al vencer enemigos ganas dinero. Puedes comprar curaciones o mejoras permanentes.

Persistencia con SQLite: El juego guarda progreso (Max HP y dinero) en rogue_snake.db.

Bucle de Juego Dual:

Render fluido a 60 FPS.

Lógica (movimiento, colisiones) a 15 FPS.

**Cómo Empezar**

**Clonar el repositorio:**
```
git clone [https://github.com/MasterBow/SnakeTheRogue.git](https://github.com/MasterBow/SnakeTheRogue.git)
cd SnakeTheRogue
```

**Instalar dependencias:**
```
pip install pygame
```

**Ejecutar el juego:**
```
python main.py

```
**Controles**
```
Acción

Tecla

Mover la serpiente

Flechas

Disparar

Espacio

Entrar a la tienda

E (cerca de la tienda)

Comprar curación

H

Comprar mejora permanente

U

Salir de la tienda

ESC
```
**📁 Estructura de Archivos**
```
snake_rogue_pygame/
├─ main.py          # Punto de entrada del juego.
├─ game.py          # Bucle principal y lógica de orquestación.
├─ config.py        # Constantes globales.
├─ database.py      # Persistencia (SQLite).
├─ snake.py         # Jugador, stats, disparos.
├─ enemy.py         # Enemigos y sus barras de vida.
├─ projectile.py    # Proyectiles.
├─ camera.py        # Cámara que sigue al jugador.
├─ food.py          # Comida (objeto pasivo).
├─ shop.py          # Tienda y sus ítems.
└─ rogue_snake.db   # Base de datos (generada automáticamente).
```

**Arquitectura Lógica**

main.py: Punto de entrada. Crea una instancia de Game y llama a su bucle principal.

game.py: Orquestador del juego: maneja eventos, estados, colisiones, render y lógica interna.
```
mientras True:
    events()
    update()  # Solo corre a 15 FPS
    draw()    # Corre a 60 FPS

```
```
config.py: Contiene constantes: colores, tamaños, FPS y parámetros base.

database.py: Crea tablas y almacena max_hp y money. Carga esos datos al iniciar.

snake.py: Administra al jugador: movimiento, estadísticas, disparos y cooldowns.

enemy.py: Enemigos con HP, dibujado y barra de vida.

projectile.py: Balas que se mueven en línea recta según dirección inicial.

camera.py: Convierte coordenadas del mundo a coordenadas de pantalla.

food.py: Objeto pasivo que se dibuja en pantalla según la cámara.

shop.py: Área interactiva que vende mejoras y curaciones.

⏳ Arquitectura del Game Loop (60 / 15 FPS)

El juego separa el renderizado de la lógica mediante un timestep fijo.

Renderizado y entrada → 60 FPS

Lógica del juego → 15 FPS

logic_timer = 0.0
```
```
mientras True:
    dt = clock.tick(60) / 1000
    logic_timer += dt
```
    events()   # fluido

    si logic_timer >= 1 / 15:
        update()
        logic_timer -= 1 / 15

    draw()
    display.flip()
```
```
**🗺️ Roadmap**

(Próximas características y mejoras)

**🛠️ Recursos Utilizados**
```
IntelliCode, Continue (Local), QwenCode 2.5 2B (local): Usados principalmente para corregir sintaxis y mejorar la estructura del código.

Llama 3.3 7B de Chat: Consultado para dudas y sugerencias durante el desarrollo.
```
