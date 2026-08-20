import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from datetime import datetime

from dao.mascota_dao import MascotaDAO
from dao.turno_dao import TurnoDAO
from models.turno import VETERINARIOS, Turno


class PanelTurnos(ttk.Frame):
    def __init__(self, contenedor):
        super().__init__(contenedor)
        self.dao = TurnoDAO()
        self.dao_mascotas = MascotaDAO()
        self.id_seleccionado = None
        self.mapa_mascotas = {}
        self._crear_widgets()
        self.refrescar()

    def _crear_widgets(self):
        formulario = ttk.LabelFrame(self, text="Datos del turno")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Mascota:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.var_mascota = tk.StringVar()
        self.combo_mascotas = ttk.Combobox(formulario, textvariable=self.var_mascota, width=35, state="readonly")
        self.combo_mascotas.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Veterinario:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.var_veterinario = tk.StringVar()
        self.combo_veterinarios = ttk.Combobox(
            formulario, textvariable=self.var_veterinario, values=list(VETERINARIOS), state="readonly", width=25
        )
        self.combo_veterinarios.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Fecha (DD/MM/AAAA):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.var_fecha = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        ttk.Entry(formulario, textvariable=self.var_fecha, width=15).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(formulario, text="Hora (HH:MM):").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.var_hora = tk.StringVar(value="09:00")
        ttk.Spinbox(formulario, values=tuple(f"{h:02d}:00" for h in range(8, 21)), textvariable=self.var_hora, width=8).grid(
            row=1, column=3, sticky="w", padx=5, pady=5
        )

        ttk.Label(formulario, text="Motivo:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.var_motivo = tk.StringVar()
        ttk.Entry(formulario, textvariable=self.var_motivo, width=45).grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

        botones = ttk.Frame(self)
        botones.pack(fill="x", padx=10)

        ttk.Button(botones, text="Agregar", command=self.agregar).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar formulario", command=self.limpiar).pack(side="left", padx=4)

        tabla = ttk.LabelFrame(self, text="Listado de turnos")
        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("id", "fecha", "hora", "mascota", "dueno", "motivo", "veterinario")
        self.arbol = ttk.Treeview(tabla, columns=columnas, show="headings", height=12)
        encabezados = ("ID", "Fecha", "Hora", "Mascota", "Dueño", "Motivo", "Veterinario")
        anchos = (50, 100, 70, 140, 140, 220, 140)
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
            mascotas = self.dao_mascotas.listar_con_cliente()
            filas = self.dao.listar_completos()
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudieron leer los datos:\n{error}")
            return
        self.mapa_mascotas = {f"{fila[2]} ({fila[1]})": fila[0] for fila in mascotas}
        self.combo_mascotas["values"] = list(self.mapa_mascotas.keys())
        self.arbol.delete(*self.arbol.get_children())
        for fila in filas:
            self.arbol.insert("", "end", values=fila)

    def al_seleccionar(self, _evento):
        seleccion = self.arbol.selection()
        if not seleccion:
            return
        valores = self.arbol.item(seleccion[0], "values")
        self.id_seleccionado = int(valores[0])
        clave = f"{valores[3]} ({valores[4]})"
        if clave in self.mapa_mascotas:
            self.var_mascota.set(clave)
        self.var_fecha.set(valores[1])
        self.var_hora.set(valores[2])
        self.var_motivo.set(valores[5])
        self.var_veterinario.set(valores[6])

    def agregar(self):
        try:
            turno = Turno(
                self.mapa_mascotas.get(self.var_mascota.get(), 0),
                self.var_fecha.get(),
                self.var_hora.get(),
                self.var_motivo.get(),
                self.var_veterinario.get(),
            )
            self.dao.insertar(turno)
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
        except sqlite3.IntegrityError as error:
            messagebox.showerror("Error de integridad", f"Los datos violan las reglas de la base:\n{error}")
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo guardar el turno:\n{error}")
        else:
            messagebox.showinfo("Turno agregado", "El turno se registró correctamente.")
            self.limpiar()
            self.refrescar()

    def actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Seleccione un turno de la tabla para actualizar.")
            return
        try:
            turno = Turno(
                self.mapa_mascotas.get(self.var_mascota.get(), 0),
                self.var_fecha.get(),
                self.var_hora.get(),
                self.var_motivo.get(),
                self.var_veterinario.get(),
                id_turno=self.id_seleccionado,
            )
            self.dao.actualizar(turno)
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
        except sqlite3.IntegrityError as error:
            messagebox.showerror("Error de integridad", f"Los datos violan las reglas de la base:\n{error}")
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo actualizar el turno:\n{error}")
        else:
            messagebox.showinfo("Turno actualizado", "Los cambios se guardaron correctamente.")
            self.limpiar()
            self.refrescar()

    def eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Seleccione un turno de la tabla para eliminar.")
            return
        confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Desea eliminar el turno seleccionado?")
        if not confirmacion:
            return
        try:
            self.dao.eliminar(self.id_seleccionado)
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo eliminar el turno:\n{error}")
        else:
            messagebox.showinfo("Turno eliminado", "El turno fue eliminado correctamente.")
            self.limpiar()
            self.refrescar()

    def limpiar(self):
        self.id_seleccionado = None
        self.var_mascota.set("")
        self.var_veterinario.set("")
        self.var_fecha.set(datetime.now().strftime("%d/%m/%Y"))
        self.var_hora.set("09:00")
        self.var_motivo.set("")
