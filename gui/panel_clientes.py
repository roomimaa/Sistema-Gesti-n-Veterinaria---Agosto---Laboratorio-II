import tkinter as tk
from tkinter import ttk, messagebox

from dao.cliente_dao import ClienteDAO
from models.cliente import Cliente


class PanelClientes(ttk.Frame):
    def __init__(self, contenedor):
        super().__init__(contenedor)
        self.dao = ClienteDAO()
        self.id_seleccionado = None
        self._crear_widgets()
        self.refrescar()

    def _crear_widgets(self):
        formulario = ttk.LabelFrame(self, text="Datos del cliente")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.var_nombre = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.var_nombre, width=32).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Teléfono:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.var_telefono = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.var_telefono, width=20).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Email:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.var_email = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.var_email, width=32).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Domicilio:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.var_domicilio = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.var_domicilio, width=32).grid(row=1, column=3, padx=5, pady=5)

        botones = ttk.Frame(self)
        botones.pack(fill="x", padx=10)

        ttk.Button(botones, text="Agregar", command=self.agregar).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar formulario", command=self.limpiar).pack(side="left", padx=4)

        tabla = ttk.LabelFrame(self, text="Listado de clientes")
        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("id", "nombre", "telefono", "email", "domicilio")
        self.arbol = ttk.Treeview(tabla, columns=columnas, show="headings", height=12)
        encabezados = ("ID", "Nombre", "Teléfono", "Email", "Domicilio")
        anchos = (50, 200, 120, 220, 250)
        for col, texto, ancho in zip(columnas, encabezados, anchos):
            self.arbol.heading(col, text=texto)
            self.arbol.column(col, width=ancho, anchor="w")

        barra = ttk.Scrollbar(tabla, orient="vertical", command=self.arbol.yview)
        self.arbol.configure(yscrollcommand=barra.set)
        self.arbol.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.arbol.bind("<<TreeviewSelect>>", self.al_seleccionar)

    def refrescar(self):
        try:
            clientes = self.dao.seleccionar_todos()
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo leer la tabla de clientes:\n{error}")
            return
        self.arbol.delete(*self.arbol.get_children())
        for c in clientes:
            self.arbol.insert("", "end", values=(c.id_cliente, c.nombre, c.telefono, c.email, c.domicilio))

    def al_seleccionar(self, _evento):
        seleccion = self.arbol.selection()
        if not seleccion:
            return
        valores = self.arbol.item(seleccion[0], "values")
        self.id_seleccionado = int(valores[0])
        self.var_nombre.set(valores[1])
        self.var_telefono.set(valores[2])
        self.var_email.set(valores[3])
        self.var_domicilio.set(valores[4])

    def agregar(self):
        try:
            cliente = Cliente(
                self.var_nombre.get(),
                self.var_telefono.get(),
                self.var_email.get(),
                self.var_domicilio.get(),
            )
            self.dao.insertar(cliente)
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
        except sqlite3.IntegrityError as error:
            messagebox.showerror("Error de integridad", f"Los datos violan las reglas de la base:\n{error}")
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo guardar el cliente:\n{error}")
        else:
            messagebox.showinfo("Cliente agregado", f"El cliente '{cliente.nombre}' se guardó correctamente.")
            self.limpiar()
            self.refrescar()

    def actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Seleccione un cliente de la tabla para actualizar.")
            return
        try:
            cliente = Cliente(
                self.var_nombre.get(),
                self.var_telefono.get(),
                self.var_email.get(),
                self.var_domicilio.get(),
                id_cliente=self.id_seleccionado,
            )
            self.dao.actualizar(cliente)
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
        except sqlite3.IntegrityError as error:
            messagebox.showerror("Error de integridad", f"Los datos violan las reglas de la base:\n{error}")
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo actualizar el cliente:\n{error}")
        else:
            messagebox.showinfo("Cliente actualizado", "Los cambios se guardaron correctamente.")
            self.limpiar()
            self.refrescar()

    def eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Seleccione un cliente de la tabla para eliminar.")
            return
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            "Se eliminará el cliente y, por integridad en cascada,\ntambién sus mascotas y turnos. ¿Desea continuar?",
        )
        if not confirmacion:
            return
        try:
            self.dao.eliminar(self.id_seleccionado)
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo eliminar el cliente:\n{error}")
        else:
            messagebox.showinfo("Cliente eliminado", "El cliente fue eliminado correctamente.")
            self.limpiar()
            self.refrescar()

    def limpiar(self):
        self.id_seleccionado = None
        self.var_nombre.set("")
        self.var_telefono.set("")
        self.var_email.set("")
        self.var_domicilio.set("")
