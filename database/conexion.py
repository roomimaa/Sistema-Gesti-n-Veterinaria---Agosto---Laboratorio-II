import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_BD = os.path.join(os.path.dirname(BASE_DIR), "veterinaria.db")
RUTA_SCHEMA = os.path.join(BASE_DIR, "schema.sql")


def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BD)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_base_datos():
    conexion = None
    try:
        with open(RUTA_SCHEMA, "r", encoding="utf-8") as archivo:
            script = archivo.read()
        conexion = obtener_conexion()
        conexion.executescript(script)
        conexion.commit()
    except sqlite3.Error as error:
        print(f"Error al inicializar la base de datos: {error}")
        raise
    finally:
        if conexion is not None:
            conexion.close()
