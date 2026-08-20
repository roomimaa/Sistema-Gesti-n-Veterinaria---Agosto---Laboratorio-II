CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre     TEXT    NOT NULL,
    telefono   TEXT    NOT NULL,
    email      TEXT,
    domicilio  TEXT
);

CREATE TABLE IF NOT EXISTS mascotas (
    id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    nombre     TEXT    NOT NULL,
    especie    TEXT    NOT NULL,
    raza       TEXT,
    edad       INTEGER NOT NULL CHECK (edad >= 0),
    FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS turnos (
    id_turno    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_mascota  INTEGER NOT NULL,
    fecha       TEXT    NOT NULL,
    hora        TEXT    NOT NULL,
    motivo      TEXT    NOT NULL,
    veterinario TEXT    NOT NULL,
    FOREIGN KEY (id_mascota) REFERENCES mascotas (id_mascota) ON DELETE CASCADE
);
