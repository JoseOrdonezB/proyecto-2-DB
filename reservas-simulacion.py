import psycopg2             # Librería para conectarse y trabajar con bases de datos PostgreSQL
import threading            # Para manejar múltiples hilos (concurrencia)
import time                 # Para medir duración de la simulación
import configparser         # Para leer el archivo de configuración config.ini
import os                   # Para obtener rutas absolutas
from inicializador_db import verificar_o_crear_base  # Función que crea tablas y datos si no existen

# Cargar la configuración desde config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Extraer los parámetros de conexión a la base de datos
DB_CONFIG = {
    'dbname': config['database']['dbname'],
    'user': config['database']['user'],
    'password': config['database']['password'],
    'host': config['database']['host'],
    'port': config['database']['port']
}

# Asiento específico a reservar y nivel de aislamiento para la transacción
ID_ASIENTO = int(config['simulacion']['asiento_id'])
AISLAMIENTO = config['simulacion']['aislamiento']

# Mensajes de depuración para verificar carga del archivo config.ini
print(sep='')
print(f"📂 Cargando archivo config.ini desde: {os.path.abspath('config.ini')}")
print(f"🛠️ Usuario leído: {DB_CONFIG['user']}")
print(f"🛠️ Contraseña leída: {DB_CONFIG['password']}")
print(f"🛠️ DB leída: {DB_CONFIG['dbname']}")
print(f"📂 Directorio de trabajo actual: {os.getcwd()}")
print(sep='')

# Variables globales protegidas por un lock para contabilizar resultados
lock = threading.Lock()  # Para evitar condiciones de carrera al actualizar resultados
resultados = {
    'exitosas': 0,  # Número de reservas exitosas
    'fallidas': 0   # Número de reservas fallidas (por conflicto o error)
}

# Función que representa el intento de un usuario por reservar un asiento
def intentar_reservar(id_usuario):
    try:
        # Conectarse a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_session(isolation_level=AISLAMIENTO, autocommit=False)
        cur = conn.cursor()

        # Verificar si el asiento ya ha sido reservado, bloqueándolo mientras tanto
        cur.execute("SELECT id_reserva FROM reservas WHERE id_asiento = %s FOR UPDATE;", (ID_ASIENTO,))
        ya_reservado = cur.fetchone()

        if ya_reservado:
            # Si el asiento ya fue reservado, cancelar la transacción y contar como fallida
            with lock:
                resultados['fallidas'] += 1
            conn.rollback()
        else:
            # Si no está reservado, insertar una nueva reserva
            cur.execute(
                "INSERT INTO reservas (id_usuario, id_asiento) VALUES (%s, %s);",
                (id_usuario, ID_ASIENTO)
            )
            conn.commit()
            with lock:
                resultados['exitosas'] += 1

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        # En caso de error (ej. violación de unicidad o conexión), contar como fallida
        with lock:
            resultados['fallidas'] += 1
        print(f"[Usuario {id_usuario}] 💥 Error: {e}")

# Función que lanza múltiples hilos simulando usuarios concurrentes
def simular_reservas(num_usuarios):
    threads = []
    resultados['exitosas'] = 0
    resultados['fallidas'] = 0

    inicio = time.time()  # Iniciar cronómetro

    for i in range(num_usuarios):
        id_usuario = (i % 5) + 1  # Rotar entre los primeros 5 usuarios (1 al 5)
        hilo = threading.Thread(target=intentar_reservar, args=(id_usuario,))
        threads.append(hilo)
        hilo.start()

    # Esperar a que todos los hilos terminen
    for hilo in threads:
        hilo.join()

    fin = time.time()
    duracion_ms = round((fin - inicio) * 1000, 2)

    # Mostrar resultados de la simulación
    print("\n🧪 Resultados de la simulación")
    print("──────────────────────────────")
    print(f"👥 Usuarios concurrentes: {num_usuarios}")
    print(f"🔒 Nivel de aislamiento: {AISLAMIENTO}")
    print(f"✅ Reservas exitosas: {resultados['exitosas']}")
    print(f"❌ Reservas fallidas: {resultados['fallidas']}")
    print(f"⏱️ Tiempo total: {duracion_ms} ms\n")

# Punto de entrada del script
if __name__ == "__main__":
    verificar_o_crear_base()  # Crear tablas y datos si es la primera vez
    print("🎯 Simulación de reserva concurrente iniciada...\n")
    simular_reservas(num_usuarios=10)  # Ejecutar simulación con 10 usuarios
