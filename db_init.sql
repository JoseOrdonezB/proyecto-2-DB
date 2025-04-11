-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de eventos
CREATE TABLE IF NOT EXISTS eventos (
    id_evento SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha TIMESTAMP NOT NULL
);

-- Tabla de asientos
CREATE TABLE IF NOT EXISTS asientos (
    id_asiento SERIAL PRIMARY KEY,
    id_evento INTEGER NOT NULL REFERENCES eventos(id_evento) ON DELETE CASCADE,
    numero_asiento VARCHAR(10) NOT NULL,
    UNIQUE(id_evento, numero_asiento)
);

-- Tabla de reservas
CREATE TABLE IF NOT EXISTS reservas (
    id_reserva SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_asiento INTEGER NOT NULL REFERENCES asientos(id_asiento) ON DELETE CASCADE,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_asiento)
);

-- Tabla de bitácora de reservas
CREATE TABLE IF NOT EXISTS bitacora_reservas (
    id_bitacora SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    id_asiento INTEGER REFERENCES asientos(id_asiento) ON DELETE SET NULL,
    accion VARCHAR(50) NOT NULL,
    descripcion TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Función para registrar en la bitácora cuando se hace una reserva
CREATE OR REPLACE FUNCTION registrar_bitacora_reserva()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO bitacora_reservas (
        id_usuario,
        id_asiento,
        accion,
        descripcion,
        fecha
    ) VALUES (
        NEW.id_usuario,
        NEW.id_asiento,
        'RESERVA_EXITOSA',
        'Reserva confirmada para el asiento ' || NEW.id_asiento ||
        ' por el usuario ' || NEW.id_usuario,
        CURRENT_TIMESTAMP
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que llama a la función después de insertar una reserva
DROP TRIGGER IF EXISTS trigger_bitacora_reserva ON reservas;

CREATE TRIGGER trigger_bitacora_reserva
AFTER INSERT ON reservas
FOR EACH ROW
EXECUTE FUNCTION registrar_bitacora_reserva();