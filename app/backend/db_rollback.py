import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()
database_name = os.getenv("DB_NAME", "club_tenis_db")

# Configuración de la base de datos
database_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'port': int(os.getenv("DB_PORT", 3306)),  # Conversión segura a entero
    'raise_on_warnings': True,
    "database": database_name
}

# Depuración de las variables de entorno
print("DB_PORT:", os.getenv("DB_PORT"))
print("database_config:", database_config)

# Definición de las tablas a eliminar (orden importante: primero tablas dependientes)
DROPPED_TB = {
    "pagos": "DROP TABLE IF EXISTS PAGOS;",
    "turno_jugadores": "DROP TABLE IF EXISTS TURNO_JUGADORES;",
    "turnos": "DROP TABLE IF EXISTS TURNOS;",
    "alumnos": "DROP TABLE IF EXISTS ALUMNOS;",
    "socio_categoria": "DROP TABLE IF EXISTS SOCIO_CATEGORIA;",
    "socios": "DROP TABLE IF EXISTS SOCIOS;",
    "profesores": "DROP TABLE IF EXISTS PROFESORES;",
    "instructores": "DROP TABLE IF EXISTS INSTRUCTORES;",
    "canchas": "DROP TABLE IF EXISTS CANCHAS;",
    "categorias": "DROP TABLE IF EXISTS CATEGORIAS;",
    # Tablas viejas por si acaso
    "articulos_categorias": "DROP TABLE IF EXISTS ARTICULOS_CATEGORIAS;",
    "articulos": "DROP TABLE IF EXISTS ARTICULOS;",
    "proveedores": "DROP TABLE IF EXISTS PROVEEDORES;",
    "marcas": "DROP TABLE IF EXISTS MARCAS;"
}

# Función para eliminar las tablas
def rollback_db():
    try:
        cxn = mysql.connector.connect(**database_config)
        cursor = cxn.cursor()
        for table in DROPPED_TB:
            print(f"Dropped table: {table}", end=" ")
            try:
                cursor.execute(DROPPED_TB[table])
                print('ok')
                cxn.commit()
            except Error as e:
                print(f"{e}")
        cursor.close()
        cxn.close()
    except Error as err:
        print(f"Error al conectar a la base de datos: {err}")

# Ejecutar la función de rollback
rollback_db()