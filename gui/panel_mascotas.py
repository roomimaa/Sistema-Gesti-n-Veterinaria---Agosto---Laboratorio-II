import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from dao.cliente_dao import ClienteDAO
from dao.mascota_dao import MascotaDAO
from models.mascota import ESPECIES_VALIDAS, Mascota


class PanelMascotas(ttk.Frame):
    def __init__(self, contenedor):
        super().__init__(contenedor)
        self.dao = MascotaDAO()
        self.dao_clientes = ClienteDAO()
        self.id_seleccionado = None
        self.mapa_clientes = {}
        self._crear_widgets()
        self.refrescar()

    def _crear_widgets(self):
        formulario = ttk.LabelFrame(self, text="Datos de la mascota")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Dueño:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.var_cliente = tk.StringVar()
        self.combo_clientes = ttk.Combobox(formulario, textvariable=self.var_cliente, width=30, state="readonly")
        self.combo_clientes.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.var_nombre = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.var_nombre, width=25).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Especie:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.var_especie = tk.StringVar()
        self.combo_especies = ttk.Combobox(
            formulario, textvariable=self.var_especie, values=list(ESPECIES_VALIDAS), state="readonly", width=28
        )
        self.combo_especies.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Raza:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.var_raza = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.var_raza, width=25).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Edad (años):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.var_edad = tk.StringVar(value="0")
        ttk.Spinbox(formulario, from_=0, to=50, textvariable=self.var_edad, width=8).grid(
            row=2, column=1, sticky="w", padx=5, pady=5
        )

        botones = ttk.Frame(self)
        botones.pack(fill="x", padx=10)

        ttk.Button(botones, text="Agregar", command=self.agregar).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar formulario", command=self.limpiar).pack(side="left", padx=4)

        tabla = ttk.LabelFrame(self, text="Listado de mascotas")
        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("id", "dueno", "nombre", "especie", "raza", "edad")
        self.arbol = ttk.Treeview(tabla, columns=columnas, show="headings", height=12)
        encabezados = ("ID", "Dueño", "Nombre", "Especie", "Raza", "Edad")
        anchos = (50, 200, 160, 100, 160, 60)
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
            clientes = self.dao_clientes.seleccionar_todos()
            filas = self.dao.listar_con_cliente()
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudieron leer los datos:\n{error}")
            return
        self.mapa_clientes = {str(c): c.id_cliente for c in clientes}
        self.combo_clientes["values"] = list(self.mapa_clientes.keys())
        self.arbol.delete(*self.arbol.get_children())
        for fila in filas:
            self.arbol.insert("", "end", values=fila)

    def al_seleccionar(self, _evento):
        seleccion = self.arbol.selection()
        if not seleccion:
            return
        valores = self.arbol.item(seleccion[0], "values")
        self.id_seleccionado = int(valores[0])
        dueno = valores[1]
        for texto, id_cliente in self.mapa_clientes.items():
            if texto.startswith(dueno.split(" (")[0]):
                self.var_cliente.set(texto)
                break
        self.var_nombre.set(valores[2])
        self.var_especie.set(valores[3])
        self.var_raza.set(valores[4])
        self.var_edad.set(valores[5])

    def agregar(self):
        try:
            mascota = Mascota(
                self.mapa_clientes.get(self.var_cliente.get(), 0),
                self.var_nombre.get(),
                self.var_especie.get(),
                self.var_raza.get(),
                self.var_edad.get(),
            )
            self.dao.insertar(mascota)
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
        except sqlite3.IntegrityError as error:
            messagebox.showerror("Error de integridad", f"Los datos violan las reglas de la base:\n{error}")
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo guardar la mascota:\n{error}")
        else:
            messagebox.showinfo("Mascota agregada", f"La mascota '{mascota.nombre}' se guardó correctamente.")
            self.limpiar()
            self.refrescar()

    def actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Seleccione una mascota de la tabla para actualizar.")
            return
        try:
            mascota = Mascota(
                self.mapa_clientes.get(self.var_cliente.get(), 0),
                self.var_nombre.get(),
                self.var_especie.get(),
                self.var_raza.get(),
                self.var_edad.get(),
                id_mascota=self.id_seleccionado,
            )
            self.dao.actualizar(mascota)
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
        except sqlite3.IntegrityError as error:
            messagebox.showerror("Error de integridad", f"Los datos violan las reglas de la base:\n{error}")
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo actualizar la mascota:\n{error}")
        else:
            messagebox.showinfo("Mascota actualizada", "Los cambios se guardaron correctamente.")
            self.limpiar()
            self.refrescar()

    def eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Seleccione una mascota de la tabla para eliminar.")
            return
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            "Se eliminará la mascota y sus turnos asociados. ¿Desea continuar?",
        )
        if not confirmacion:
            return
        try:
            self.dao.eliminar(self.id_seleccionado)
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo eliminar la mascota:\n{error}")
        else:
            messagebox.showinfo("Mascota eliminada", "La mascota fue eliminada correctamente.")
            self.limpiar()
            self.refrescar()

    def limpiar(self):
        self.id_seleccionado = None
        self.var_cliente.set("")
        self.var_nombre.set("")
        self.var_especie.set("")
        self.var_raza.set("")
        self.var_edad.set("0")
