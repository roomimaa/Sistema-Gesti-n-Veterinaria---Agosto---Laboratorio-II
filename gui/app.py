import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from gui.panel_clientes import PanelClientes
from gui.panel_mascotas import PanelMascotas
from gui.panel_turnos import PanelTurnos


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Veterinaria")
        self.geometry("1020x640")
        self.minsize(900, 560)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.panel_clientes = PanelClientes(self.notebook)
        self.panel_mascotas = PanelMascotas(self.notebook)
        self.panel_turnos = PanelTurnos(self.notebook)

        self.notebook.add(self.panel_clientes, text="  Clientes  ")
        self.notebook.add(self.panel_mascotas, text="  Mascotas  ")
        self.notebook.add(self.panel_turnos, text="  Turnos  ")

        self.notebook.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)

    def al_cambiar_pestana(self, _evento):
        try:
            indice = self.notebook.index(self.notebook.select())
            if indice == 1:
                self.panel_mascotas.refrescar()
            elif indice == 2:
                self.panel_turnos.refrescar()
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos", f"No se pudo actualizar la vista:\n{error}")
