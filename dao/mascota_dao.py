import sqlite3

from database.conexion import obtener_conexion
from models.mascota import Mascota


class MascotaDAO:
    def insertar(self, mascota):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO mascotas (id_cliente, nombre, especie, raza, edad) VALUES (?, ?, ?, ?, ?)",
                (mascota.id_cliente, mascota.nombre, mascota.especie, mascota.raza, mascota.edad),
            )
            conexion.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            if conexion is not None:
                conexion.rollback()
            raise
        finally:
            if conexion is not None:
                conexion.close()

    def actualizar(self, mascota):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE mascotas SET id_cliente = ?, nombre = ?, especie = ?, raza = ?, edad = ? WHERE id_mascota = ?",
                (mascota.id_cliente, mascota.nombre, mascota.especie, mascota.raza, mascota.edad, mascota.id_mascota),
            )
            conexion.commit()
            return cursor.rowcount
        except sqlite3.Error:
            if conexion is not None:
                conexion.rollback()
            raise
        finally:
            if conexion is not None:
                conexion.close()

    def eliminar(self, id_mascota):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM mascotas WHERE id_mascota = ?", (id_mascota,))
            conexion.commit()
            return cursor.rowcount
        except sqlite3.Error:
            if conexion is not None:
                conexion.rollback()
            raise
        finally:
            if conexion is not None:
                conexion.close()

    def seleccionar_todos(self):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id_mascota, id_cliente, nombre, especie, raza, edad FROM mascotas ORDER BY nombre"
            )
            filas = cursor.fetchall()
            return [Mascota(f[1], f[2], f[3], f[4], f[5], id_mascota=f[0]) for f in filas]
        except sqlite3.Error:
            raise
        finally:
            if conexion is not None:
                conexion.close()

    def listar_con_cliente(self):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT m.id_mascota, c.nombre, m.nombre, m.especie, m.raza, m.edad
                FROM mascotas m
                INNER JOIN clientes c ON m.id_cliente = c.id_cliente
                ORDER BY m.id_mascota
                """
            )
            return cursor.fetchall()
        except sqlite3.Error:
            raise
        finally:
            if conexion is not None:
                conexion.close()
