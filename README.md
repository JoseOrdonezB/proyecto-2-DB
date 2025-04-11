# 🎟️ Simulador de Reservas Concurrentes con PostgreSQL

Este proyecto simula múltiples usuarios intentando reservar el **mismo asiento** al mismo tiempo en una base de datos PostgreSQL, evaluando la integridad de los datos bajo diferentes niveles de aislamiento.

---

## 🚀 ¿Qué hace este simulador?

- Conecta a una base de datos PostgreSQL.
- Verifica si la base ya existe; si no, la crea automáticamente.
- Carga las tablas y datos necesarios.
- Simula concurrencia con múltiples hilos (usuarios).
- Controla transacciones y bloqueos para evitar inconsistencias.
- Muestra resultados **en consola** como un listado profesional.

---

## 🧩 Requisitos

- Python 3.8 o superior
- PostgreSQL instalado y corriendo
- Acceso a una cuenta con permisos para crear bases y ejecutar scripts

---

## 📦 Instalación

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias con:

```bash
pip install -r requirements.txt