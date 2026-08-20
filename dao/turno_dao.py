import sqlite3

from database.conexion import obtener_conexion
from models.turno import Turno


class TurnoDAO:
    def insertar(self, turno):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO turnos (id_mascota, fecha, hora, motivo, veterinario) VALUES (?, ?, ?, ?, ?)",
                (turno.id_mascota, turno.fecha, turno.hora, turno.motivo, turno.veterinario),
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

    def actualizar(self, turno):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE turnos SET id_mascota = ?, fecha = ?, hora = ?, motivo = ?, veterinario = ? WHERE id_turno = ?",
                (turno.id_mascota, turno.fecha, turno.hora, turno.motivo, turno.veterinario, turno.id_turno),
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

    def eliminar(self, id_turno):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM turnos WHERE id_turno = ?", (id_turno,))
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
                "SELECT id_turno, id_mascota, fecha, hora, motivo, veterinario FROM turnos ORDER BY fecha, hora"
            )
            filas = cursor.fetchall()
            return [Turno(f[1], f[2], f[3], f[4], f[5], id_turno=f[0]) for f in filas]
        except sqlite3.Error:
            raise
        finally:
            if conexion is not None:
                conexion.close()

    def listar_completos(self):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT t.id_turno, t.fecha, t.hora, m.nombre, c.nombre, t.motivo, t.veterinario
                FROM turnos t
                INNER JOIN mascotas m ON t.id_mascota = m.id_mascota
                INNER JOIN clientes c ON m.id_cliente = c.id_cliente
                ORDER BY t.fecha, t.hora
                """
            )
            return cursor.fetchall()
        except sqlite3.Error:
            raise
        finally:
            if conexion is not None:
                conexion.close()
