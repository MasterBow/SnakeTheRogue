# database.py
"""
Módulo de Persistencia de Datos (Base de Datos).
"""

import sqlite3

DB_NAME = 'rogue_snake.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
    cursor.execute("INSERT OR IGNORE INTO player (id) VALUES (1);")
    conn.commit() 
    conn.close()

def load_player_data(snake):
    conn = get_db_connection()
    cursor = conn.cursor()
    player_data = cursor.execute("SELECT * FROM player WHERE id = 1").fetchone()
    
    snake.max_hp = player_data['max_hp']
    snake.hp = snake.max_hp 
    snake.money = player_data['money']
    snake.attack_damage = player_data['attack_damage']
    snake.attack_speed = player_data['attack_speed']
    snake.projectile_speed = player_data['projectile_speed']
    conn.close()
    print(f"Datos cargados: HP={snake.max_hp}, Dinero=${snake.money}")

def save_player_data(snake):
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
    print("Datos guardados correctamente.")

# --- NUEVA FUNCIÓN ---
def reset_player_data():
    """Reinicia los valores del jugador a los defecto (Nueva Partida)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Reseteamos a los valores iniciales por defecto
    cursor.execute("""
    UPDATE player SET
        max_hp = 100,
        money = 25,
        attack_damage = 10,
        attack_speed = 500,
        projectile_speed = 15
    WHERE id = 1;
    """)
    conn.commit()
    conn.close()
    print("Partida reiniciada.")