class Cliente:
    def __init__(self, nombre, telefono, email="", domicilio="", id_cliente=None):
        self._id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.domicilio = domicilio

    @property
    def id_cliente(self):
        return self._id_cliente

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre del cliente es obligatorio.")
        self._nombre = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El teléfono del cliente es obligatorio.")
        self._telefono = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = (valor or "").strip()

    @property
    def domicilio(self):
        return self._domicilio

    @domicilio.setter
    def domicilio(self, valor):
        self._domicilio = (valor or "").strip()

    def __str__(self):
        return f"{self._nombre} (Tel: {self._telefono})"
