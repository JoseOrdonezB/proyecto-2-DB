# 🎟️ Simulador de Reservas Concurrentes con PostgreSQL

Este proyecto simula múltiples usuarios intentando reservar el mismo asiento al mismo tiempo en una base de datos PostgreSQL. Evalúa cómo diferentes niveles de aislamiento (`READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`) afectan la integridad de los datos durante operaciones concurrentes usando transacciones.

---

## 📁 ¿Qué hay dentro del proyecto?

```
simulador_reservas/
├── simulador_reservas.py        # Script principal que corre la simulación
├── db_initializer.py            # Crea la base y ejecuta los scripts SQL si no existen
├── init_db.sql                  # Crea las tablas, funciones y triggers
├── data.sql                     # Inserta usuarios, eventos, asientos y reservas iniciales
├── config.ini                   # Configuración editable de base de datos y simulación
├── requirements.txt             # Dependencias (psycopg2-binary)
└── README.md                    # Instrucciones del proyecto
```

---

## 🚀 ¿Cómo se corre el simulador?

1. Asegúrate de tener PostgreSQL 17 corriendo y accesible.
2. Configura `config.ini` con tu usuario de postgres y una contraseña válida.
3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecuta el simulador:

```bash
python3 simulador_reservas.py
```

El sistema se encargará de:
- Verificar si la base existe (y crearla si no).
- Crear las tablas y cargar los datos si es necesario.
- Ejecutar la simulación concurrente de reservas.
- Mostrar los resultados directamente en consola.
