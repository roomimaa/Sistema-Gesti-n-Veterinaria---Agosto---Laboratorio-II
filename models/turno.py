from datetime import datetime

VETERINARIOS = ("Dra. Gómez", "Dr. Pérez", "Dra. Fernández", "Dr. Sosa")


class Turno:
    def __init__(self, id_mascota, fecha, hora, motivo, veterinario, id_turno=None):
        self._id_turno = id_turno
        self.id_mascota = id_mascota
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.veterinario = veterinario

    @property
    def id_turno(self):
        return self._id_turno

    @property
    def id_mascota(self):
        return self._id_mascota

    @id_mascota.setter
    def id_mascota(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("Debe seleccionar una mascota válida.")
        self._id_mascota = valor

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        texto = (valor or "").strip()
        try:
            datetime.strptime(texto, "%d/%m/%Y")
        except ValueError:
            raise ValueError("La fecha debe tener el formato DD/MM/AAAA.")
        self._fecha = texto

    @property
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, valor):
        texto = (valor or "").strip()
        try:
            datetime.strptime(texto, "%H:%M")
        except ValueError:
            raise ValueError("La hora debe tener el formato HH:MM (24 hs).")
        self._hora = texto

    @property
    def motivo(self):
        return self._motivo

    @motivo.setter
    def motivo(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El motivo del turno es obligatorio.")
        self._motivo = valor.strip()

    @property
    def veterinario(self):
        return self._veterinario

    @veterinario.setter
    def veterinario(self, valor):
        texto = (valor or "").strip()
        if texto not in VETERINARIOS:
            raise ValueError("Debe seleccionar un veterinario válido.")
        self._veterinario = texto

    def __str__(self):
        return f"{self._fecha} {self._hora} - {self._motivo}"
