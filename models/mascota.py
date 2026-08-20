ESPECIES_VALIDAS = ("Perro", "Gato", "Ave", "Conejo", "Reptil", "Otro")


class Mascota:
    def __init__(self, id_cliente, nombre, especie, raza="", edad=0, id_mascota=None):
        self._id_mascota = id_mascota
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad

    @property
    def id_mascota(self):
        return self._id_mascota

    @property
    def id_cliente(self):
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("Debe seleccionar un cliente válido.")
        self._id_cliente = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre de la mascota es obligatorio.")
        self._nombre = valor.strip()

    @property
    def especie(self):
        return self._especie

    @especie.setter
    def especie(self, valor):
        texto = (valor or "").strip()
        if texto not in ESPECIES_VALIDAS:
            raise ValueError("Debe seleccionar una especie válida.")
        self._especie = texto

    @property
    def raza(self):
        return self._raza

    @raza.setter
    def raza(self, valor):
        self._raza = (valor or "").strip()

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, valor):
        try:
            numero = int(valor)
        except (TypeError, ValueError):
            raise ValueError("La edad debe ser un número entero.")
        if numero < 0:
            raise ValueError("La edad no puede ser negativa.")
        self._edad = numero

    def __str__(self):
        return f"{self._nombre} ({self._especie})"
