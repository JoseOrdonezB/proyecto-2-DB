-- Insertar usuarios de prueba
INSERT INTO usuarios (nombre, correo) VALUES
('Ana Torres', 'ana.torres@example.com'),
('Luis Gómez', 'luis.gomez@example.com'),
('Carla Méndez', 'carla.mendez@example.com'),
('Jorge Ruiz', 'jorge.ruiz@example.com'),
('Valeria Soto', 'valeria.soto@example.com'),
('Miguel Herrera', 'miguel.herrera@example.com'),
('Sofía Rivas', 'sofia.rivas@example.com'),
('Pedro Cáceres', 'pedro.caceres@example.com'),
('Daniela Campos', 'daniela.campos@example.com'),
('Elena Paredes', 'elena.paredes@example.com');

-- Insertar eventos de prueba
INSERT INTO eventos (nombre, fecha) VALUES
('Conferencia de Tecnología 2025', '2025-06-15 10:00:00'),
('Feria de Innovación 2025', '2025-07-10 14:00:00');

-- Insertar asientos para los eventos
INSERT INTO asientos (id_evento, numero_asiento) VALUES
-- Evento 1
(1, 'A1'), (1, 'A2'), (1, 'A3'), (1, 'A4'), (1, 'A5'),
(1, 'B1'), (1, 'B2'), (1, 'B3'), (1, 'B4'), (1, 'B5'),
-- Evento 2
(2, 'C1'), (2, 'C2'), (2, 'C3'), (2, 'C4'), (2, 'C5'),
(2, 'D1'), (2, 'D2'), (2, 'D3'), (2, 'D4'), (2, 'D5');

-- Insertar reservas iniciales
INSERT INTO reservas (id_usuario, id_asiento) VALUES
(1, 1),
(2, 2),
(3, 6),
(4, 12),  -- C2 del evento 2
(5, 17);  -- D2 del evento 2
