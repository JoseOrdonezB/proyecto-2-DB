-- Insertar usuarios de prueba
INSERT INTO usuarios (nombre, correo) VALUES
('Ana Torres', 'ana.torres@example.com'),
('Luis Gómez', 'luis.gomez@example.com'),
('Carla Méndez', 'carla.mendez@example.com'),
('Jorge Ruiz', 'jorge.ruiz@example.com'),
('Valeria Soto', 'valeria.soto@example.com');

-- Insertar un evento de prueba
INSERT INTO eventos (nombre, fecha) 
VALUES ('Conferencia de Tecnología 2025', '2025-06-15 10:00:00');

-- Insertar 10 asientos para ese evento
INSERT INTO asientos (id_evento, numero_asiento) VALUES
(1, 'A1'), (1, 'A2'), (1, 'A3'), (1, 'A4'), (1, 'A5'),
(1, 'B1'), (1, 'B2'), (1, 'B3'), (1, 'B4'), (1, 'B5');

-- Insertar algunas reservas iniciales
INSERT INTO reservas (id_usuario, id_asiento) VALUES
(1, 1),
(2, 2),
(3, 6);