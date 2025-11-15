# database.py

import sqlite3

# Nombre de nuestro archivo de base de datos
DB_NAME = 'rogue_snake.db'

def get_db_connection():
    """Establece una conexión con la DB y la devuelve."""
    # .connect() crea el archivo si no existe
    conn = sqlite3.connect(DB_NAME)
    # Esto nos permite acceder a los datos por nombre de columna (como un diccionario)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Crea las tablas de la base de datos si no existen."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Creamos una tabla 'player' para guardar las estadísticas
    # Usamos "id = 1" para el perfil del jugador (juego de un solo jugador)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY,
        max_hp INTEGER NOT NULL DEFAULT 100,
        money INTEGER NOT NULL DEFAULT 25,
        attack_damage INTEGER NOT NULL DEFAULT 10,
        attack_speed INTEGER NOT NULL DEFAULT 500,
        projectile_speed INTEGER NOT NULL DEFAULT 15
    );
    """)
    
    # Nos aseguramos de que la fila del jugador (id=1) exista
    # 'INSERT OR IGNORE' no hará nada si la fila ya existe
    cursor.execute("INSERT OR IGNORE INTO player (id) VALUES (1);")
    
    conn.commit()
    conn.close()

def load_player_data(snake):
    """Carga los datos de la DB y los aplica al objeto 'snake'."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Selecciona el único perfil de jugador
    player_data = cursor.execute("SELECT * FROM player WHERE id = 1").fetchone()
    
    # Aplica las estadísticas guardadas al objeto serpiente
    snake.max_hp = player_data['max_hp']
    snake.hp = snake.max_hp # Inicia con vida completa
    snake.money = player_data['money']
    snake.attack_damage = player_data['attack_damage']
    snake.attack_speed = player_data['attack_speed']
    snake.projectile_speed = player_data['projectile_speed']
    
    conn.close()
    print(f"Datos cargados: HP={snake.max_hp}, Dinero=${snake.money}")

def save_player_data(snake):
    """Guarda las estadísticas actuales del objeto 'snake' en la DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    UPDATE player SET
        max_hp = ?,
        money = ?,
        attack_damage = ?,
        attack_speed = ?,
        projectile_speed = ?
    WHERE id = 1;
    """, (snake.max_hp, snake.money, snake.attack_damage, snake.attack_speed, snake.projectile_speed))
    
    conn.commit()
    conn.close()
    print(f"Datos guardados: HP={snake.max_hp}, Dinero=${snake.money}")
