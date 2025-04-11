import psycopg2
import configparser
import os
import subprocess

def verificar_o_crear_base():
    config = configparser.ConfigParser()
    config.read('config.ini')

    db_name = config['database']['dbname']
    user = config['database']['user']
    password = config['database']['password']
    host = config['database']['host']
    port = config['database']['port']

    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
        existe = cur.fetchone()

        if not existe:
            print(f"📦 La base de datos '{db_name}' no existe. Creándola...")
            cur.execute(f"CREATE DATABASE {db_name};")
            print("✅ Base de datos creada correctamente.")

            print("🧱 Ejecutando scripts de inicialización...")
            subprocess.run(["psql", "-U", user, "-d", db_name, "-f", "init_db.sql"])
            subprocess.run(["psql", "-U", user, "-d", db_name, "-f", "data.sql"])
            print("✅ Tablas y datos cargados.")
        else:
            print(f"✅ La base de datos '{db_name}' ya existe. Saltando creación.")

        cur.close()
        conn.close()

    except Exception as e:
        print("💥 Error durante la verificación/creación de la base de datos:")
        print(e)