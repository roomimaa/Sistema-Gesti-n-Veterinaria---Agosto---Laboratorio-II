import sqlite3

from database.conexion import obtener_conexion
from models.cliente import Cliente


class ClienteDAO:
    def insertar(self, cliente):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono, email, domicilio) VALUES (?, ?, ?, ?)",
                (cliente.nombre, cliente.telefono, cliente.email, cliente.domicilio),
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

    def actualizar(self, cliente):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE clientes SET nombre = ?, telefono = ?, email = ?, domicilio = ? WHERE id_cliente = ?",
                (cliente.nombre, cliente.telefono, cliente.email, cliente.domicilio, cliente.id_cliente),
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

    def eliminar(self, id_cliente):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))
            conexion.commit()
            return cursor.rowcount
        except sqlite3.Error:
            if conexion is not None:
                conexion.rollback()
            raise
        finally:
            if conexion is not None:
                conexion.close()

    def buscar_por_id(self, id_cliente):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id_cliente, nombre, telefono, email, domicilio FROM clientes WHERE id_cliente = ?",
                (id_cliente,),
            )
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Cliente(fila[1], fila[2], fila[3], fila[4], id_cliente=fila[0])
        except sqlite3.Error:
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
                "SELECT id_cliente, nombre, telefono, email, domicilio FROM clientes ORDER BY nombre"
            )
            filas = cursor.fetchall()
            return [Cliente(f[1], f[2], f[3], f[4], id_cliente=f[0]) for f in filas]
        except sqlite3.Error:
            raise
        finally:
            if conexion is not None:
                conexion.close()

    def contar_todos(self):
        conexion = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM clientes")
            return cursor.fetchone()[0]
        except sqlite3.Error:
            raise
        finally:
            if conexion is not None:
                conexion.close()
