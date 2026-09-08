"""Manejo de conexión y esquemas para la base de datos SQLite3."""
import os
import sqlite3
from typing import Optional

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "students.db")


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Crea y retorna una conexión a la base de datos SQLite con soporte para nombres de columna."""
    path = db_path if db_path is not None else DEFAULT_DB_PATH
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Inicializa las tablas e índices necesarios en la base de datos."""
    conn = get_connection(db_path)
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    edad INTEGER NOT NULL,
                    telefono TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    status TEXT NOT NULL CHECK(status IN ('activo', 'inactivo')) DEFAULT 'activo',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_students_status ON students(status);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_students_nombres ON students(nombres);")
    finally:
        conn.close()
