import psycopg2              # Librería para conectarse y trabajar con bases de datos PostgreSQL
import configparser          # Para leer archivos de configuración .ini
import os                    # Para manejar rutas de archivos
import time                  # Para agregar pequeñas pausas durante la ejecución
import sys                   # Para terminar el programa en caso de errores críticos

# Función principal: verifica si la base de datos ya existe, y si no, la crea junto con las tablas y datos iniciales
def verificar_o_crear_base():
    # Leer archivo de configuración
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Obtener credenciales de conexión
    db_name = config['database']['dbname']
    user = config['database']['user']
    password = config['database']['password']
    host = config['database']['host']
    port = config['database']['port']

    # Mostrar directorio actual (útil para depuración)
    print(f"📂 Directorio de trabajo actual: {os.getcwd()}")

    try:
        # Conectarse a la base de datos "postgres", que existe por defecto, para poder crear otras bases
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True  # Permitir ejecutar CREATE DATABASE directamente
        cur = conn.cursor()

        # Verificar si la base de datos que necesitamos ya existe
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
        existe = cur.fetchone()

        if not existe:
            # Si no existe, crearla
            print(f"📦 La base de datos '{db_name}' no existe. Creándola...")
            cur.execute(f"CREATE DATABASE {db_name};")
            print("✅ Base de datos creada correctamente.")

            print("🧱 Ejecutando scripts de inicialización...")
            time.sleep(1)  # Pequeña pausa para asegurar que la base esté lista para usar

            base_path = os.path.dirname(os.path.abspath(__file__))  # Ruta del archivo actual

            # Conectarse ahora a la nueva base de datos
            conn_db = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn_db.autocommit = True
            cur_db = conn_db.cursor()

            try:
                # Ejecutar el script que crea tablas
                with open(os.path.join(base_path, "db_init.sql"), "r") as f:
                    cur_db.execute(f.read())
                print("✅ Script db_init.sql ejecutado correctamente.")

                # Ejecutar el script que inserta los datos iniciales
                with open(os.path.join(base_path, "data.sql"), "r") as f:
                    cur_db.execute(f.read())
                print("✅ Script data.sql ejecutado correctamente.")

            except Exception as script_error:
                # Si hay error en los scripts SQL, abortar el programa
                print("💥 Error al ejecutar scripts SQL:")
                print(script_error)
                print("🚫 Cancelando simulación por error de inicialización.")
                sys.exit(1)

            # Cerrar conexión a la base de datos recién creada
            cur_db.close()
            conn_db.close()

        else:
            # Si la base ya existe, no hacer nada
            print(f"✅ La base de datos '{db_name}' ya existe. Saltando creación.")

        # Cerrar conexión a la base postgres
        cur.close()
        conn.close()

    except Exception as e:
        # Capturar errores generales de conexión o creación
        print("💥 Error durante la verificación/creación de la base de datos:")
        print(e)
        print("🚫 Cancelando simulación por error de conexión.")
        sys.exit(1)
