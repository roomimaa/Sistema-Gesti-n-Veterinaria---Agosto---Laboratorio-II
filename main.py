from database.conexion import inicializar_base_datos
from gui.app import App


def main():
    inicializar_base_datos()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
