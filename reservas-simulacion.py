import psycopg2
import threading
import time
import configparser
from inicializador_db import verificar_o_crear_base

config = configparser.ConfigParser()
config.read('config.ini')

DB_CONFIG = {
    'dbname': config['database']['dbname'],
    'user': config['database']['user'],
    'password': config['database']['password'],
    'host': config['database']['host'],
    'port': config['database']['port']
}

ID_ASIENTO = int(config['simulacion']['asiento_id'])
AISLAMIENTO = config['simulacion']['aislamiento']

lock = threading.Lock()
resultados = {
    'exitosas': 0,
    'fallidas': 0
}

def intentar_reservar(id_usuario):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_session(isolation_level=AISLAMIENTO, autocommit=False)
        cur = conn.cursor()

        cur.execute("SELECT id_asiento FROM reservas WHERE id_asiento = %s FOR UPDATE;", (ID_ASIENTO,))
        ocupado = cur.fetchone()

        if ocupado:
            with lock:
                resultados['fallidas'] += 1
            conn.rollback()
        else:
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
        with lock:
            resultados['fallidas'] += 1
        print(f"[Usuario {id_usuario}] 💥 Error: {e}")

def simular_reservas(num_usuarios):
    threads = []
    resultados['exitosas'] = 0
    resultados['fallidas'] = 0

    inicio = time.time()

    for i in range(num_usuarios):
        id_usuario = (i % 5) + 1
        hilo = threading.Thread(target=intentar_reservar, args=(id_usuario,))
        threads.append(hilo)
        hilo.start()

    for hilo in threads:
        hilo.join()

    fin = time.time()
    duracion_ms = round((fin - inicio) * 1000, 2)

    print("\n🧪 Resultados de la simulación")
    print("──────────────────────────────")
    print(f"👥 Usuarios concurrentes: {num_usuarios}")
    print(f"🔒 Nivel de aislamiento: {AISLAMIENTO}")
    print(f"✅ Reservas exitosas: {resultados['exitosas']}")
    print(f"❌ Reservas fallidas: {resultados['fallidas']}")
    print(f"⏱️ Tiempo total: {duracion_ms} ms\n")

if __name__ == "__main__":
    verificar_o_crear_base()

    print("🎯 Simulación de reserva concurrente iniciada...\n")

    simular_reservas(num_usuarios=10)