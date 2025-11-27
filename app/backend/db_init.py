import mysql.connector
from mysql.connector import Error, errorcode

import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "club_tenis_db")

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'port': int(os.getenv("DB_PORT",3306)),
    'raise_on_warnings': True,
}
TABLES = {}
SEEDS = {}

TABLES['CATEGORIAS'] = (
    "CREATE TABLE `CATEGORIAS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(50) NOT NULL,"
    "  `descripcion` varchar(200),"
    "  PRIMARY KEY (`id`)"
    ") "
)

TABLES['PROFESORES'] = (
    "CREATE TABLE `PROFESORES` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(50) NOT NULL,"
    "  `apellido` varchar(50) NOT NULL,"
    "  `especialidad` varchar(100) NOT NULL,"
    "  `telefono` varchar(20) NOT NULL,"
    "  `email` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") "
)

TABLES['SOCIOS'] = (
    "CREATE TABLE `SOCIOS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(50) NOT NULL,"
    "  `apellido` varchar(50) NOT NULL,"
    "  `dni` varchar(20) NOT NULL UNIQUE,"
    "  `email` varchar(100) NOT NULL,"
    "  `telefono` varchar(20) NOT NULL,"
    "  `fecha_inscripcion` DATE NOT NULL,"
    "  `profesor_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`profesor_id`) REFERENCES PROFESORES(id)"
    ") "
)

TABLES["SOCIO_CATEGORIA"] = (
    "CREATE TABLE `SOCIO_CATEGORIA` ("
    "  `socio_id` int(11) NOT NULL,"
    "  `categoria_id` int(11) NOT NULL,"
    "  FOREIGN KEY (`socio_id`) REFERENCES SOCIOS(id),"
    "  FOREIGN KEY (`categoria_id`) REFERENCES CATEGORIAS(id)"
    ") "
)

TABLES['TURNOS'] = (
    "CREATE TABLE `TURNOS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `cancha` varchar(50) NOT NULL,"
    "  `fecha` DATE NOT NULL,"
    "  `hora_inicio` TIME NOT NULL,"
    "  `hora_fin` TIME NOT NULL,"
    "  `socio_reserva_id` int(11),"
    "  `estado` varchar(20) DEFAULT 'disponible',"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`socio_reserva_id`) REFERENCES SOCIOS(id)"
    ") "
)

TABLES['TURNO_JUGADORES'] = (
    "CREATE TABLE `TURNO_JUGADORES` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `turno_id` int(11) NOT NULL,"
    "  `jugador_nombre` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`turno_id`) REFERENCES TURNOS(id) ON DELETE CASCADE"
    ") "
)

TABLES['ALUMNOS'] = (
    "CREATE TABLE `ALUMNOS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `nombre` varchar(50) NOT NULL,"
    "  `apellido` varchar(50) NOT NULL,"
    "  `dni` varchar(20) NOT NULL UNIQUE,"
    "  `email` varchar(100) NOT NULL,"
    "  `telefono` varchar(20) NOT NULL,"
    "  `fecha_inscripcion` DATE NOT NULL,"
    "  `profesor_id` int(11) NOT NULL,"
    "  `nivel` varchar(50),"
    "  `activo` BOOLEAN DEFAULT TRUE,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`profesor_id`) REFERENCES PROFESORES(id)"
    ") "
)

TABLES['PAGOS'] = (
    "CREATE TABLE `PAGOS` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `tipo` varchar(20) NOT NULL,"
    "  `monto` DECIMAL(10,2) NOT NULL,"
    "  `fecha_pago` DATE NOT NULL,"
    "  `mes` int(11) NOT NULL,"
    "  `anio` int(11) NOT NULL,"
    "  `socio_id` int(11),"
    "  `alumno_id` int(11),"
    "  `metodo_pago` varchar(50),"
    "  `observaciones` TEXT,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`socio_id`) REFERENCES SOCIOS(id),"
    "  FOREIGN KEY (`alumno_id`) REFERENCES ALUMNOS(id)"
    ") "
)

SEEDS['CATEGORIAS'] = (
    "INSERT INTO CATEGORIAS (nombre, descripcion) "
    "VALUES (%s, %s)",
    [
        ('Junior', 'Socios menores de 18 años'),
        ('Senior', 'Socios adultos de 18 a 60 años'),
        ('Veterano', 'Socios mayores de 60 años'),
        ('Profesional', 'Jugadores profesionales o de alta competencia'),
        ('Recreativo', 'Socios que juegan ocasionalmente'),
        ('Principiante', 'Socios que están aprendiendo a jugar'),
        ('Familiar', 'Membresía familiar con descuentos')
    ]
)

SEEDS['PROFESORES'] = (
    "INSERT INTO PROFESORES (nombre, apellido, especialidad, telefono, email) "
    "VALUES (%s, %s, %s, %s, %s)",
    [
        ('Carlos', 'Rodríguez', 'Técnica de Saque y Volea', '1144556677', 'carlos.rodriguez@clubtenis.com'),
        ('María', 'Fernández', 'Entrenamiento Físico y Táctico', '1167891234', 'maria.fernandez@clubtenis.com'),
        ('Roberto', 'González', 'Principiantes y Niños', '1133445566', 'roberto.gonzalez@clubtenis.com'),
        ('Laura', 'Martínez', 'Alta Competencia', '1122334455', 'laura.martinez@clubtenis.com'),
        ('Diego', 'López', 'Preparación Mental y Estrategia', '1198765432', 'diego.lopez@clubtenis.com')
    ]
)

SEEDS['SOCIOS'] = (
    "INSERT INTO SOCIOS (nombre, apellido, dni, email, telefono, fecha_inscripcion, profesor_id) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
    [
        ('Juan', 'Pérez', '12345678', 'juan.perez@email.com', '1144556688', '2024-01-15', 1),
        ('Ana', 'García', '23456789', 'ana.garcia@email.com', '1155667799', '2024-02-20', 2),
        ('Luis', 'Fernández', '34567890', 'luis.fernandez@email.com', '1166778800', '2024-03-10', 3),
        ('Sofia', 'Torres', '45678901', 'sofia.torres@email.com', '1177889911', '2024-04-05', 4),
        ('Miguel', 'Ramírez', '56789012', 'miguel.ramirez@email.com', '1188990022', '2024-05-12', 5),
        ('Carla', 'Sánchez', '67890123', 'carla.sanchez@email.com', '1199001133', '2024-06-18', 1),
        ('Pedro', 'Moreno', '78901234', 'pedro.moreno@email.com', '1100112244', '2024-07-22', 3),
        ('Julia', 'Romero', '89012345', 'julia.romero@email.com', '1111223355', '2024-08-30', 2)
    ]
)

SEEDS['SOCIO_CATEGORIA'] = (
    "INSERT INTO SOCIO_CATEGORIA (socio_id, categoria_id) "
    "VALUES (%s, %s)",
    [
        (1, 2), (1, 5),
        (2, 2), (2, 4),
        (3, 1),
        (4, 2), (4, 6),
        (5, 3),
        (6, 2), (6, 5),
        (7, 1),
        (8, 2), (8, 4)
    ]
)

SEEDS['TURNOS'] = (
    "INSERT INTO TURNOS (cancha, fecha, hora_inicio, hora_fin, socio_reserva_id, estado) "
    "VALUES (%s, %s, %s, %s, %s, %s)",
    [
        ('Cancha Central', '2024-12-15', '09:00:00', '09:30:00', 1, 'reservado'),
        ('Cancha Central', '2024-12-15', '09:30:00', '10:00:00', 1, 'reservado'),
        ('Cancha 1', '2024-12-15', '10:00:00', '10:30:00', 2, 'reservado'),
        ('Cancha 2', '2024-12-15', '14:00:00', '14:30:00', 3, 'reservado'),
        ('Cancha 3', '2024-12-16', '16:00:00', '16:30:00', 4, 'reservado'),
        ('Cancha 1', '2024-12-16', '17:00:00', '17:30:00', 5, 'reservado'),
        ('Cancha Central', '2024-12-17', '08:00:00', '08:30:00', None, 'disponible'),
        ('Cancha 2', '2024-12-17', '11:00:00', '11:30:00', None, 'disponible')
    ]
)

SEEDS['TURNO_JUGADORES'] = (
    "INSERT INTO TURNO_JUGADORES (turno_id, jugador_nombre) "
    "VALUES (%s, %s)",
    [
        (1, 'Juan Pérez'),
        (1, 'Ana García'),
        (2, 'Juan Pérez'),
        (2, 'Luis Fernández'),
        (3, 'Ana García'),
        (3, 'Sofia Torres'),
        (4, 'Luis Fernández'),
        (4, 'Miguel Ramírez'),
        (5, 'Sofia Torres'),
        (5, 'Carla Sánchez'),
        (6, 'Miguel Ramírez'),
        (6, 'Pedro Moreno')
    ]
)

SEEDS['ALUMNOS'] = (
    "INSERT INTO ALUMNOS (nombre, apellido, dni, email, telefono, fecha_inscripcion, profesor_id, nivel, activo) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    [
        ('Martín', 'Gómez', '11223344', 'martin.gomez@email.com', '1122334455', '2024-01-10', 3, 'Principiante', True),
        ('Lucía', 'Herrera', '22334455', 'lucia.herrera@email.com', '1133445566', '2024-02-15', 3, 'Principiante', True),
        ('Diego', 'Silva', '33445566', 'diego.silva@email.com', '1144556677', '2024-03-20', 1, 'Intermedio', True),
        ('Valentina', 'Castro', '44556677', 'valentina.castro@email.com', '1155667788', '2024-04-25', 2, 'Intermedio', True),
        ('Tomás', 'Ruiz', '55667788', 'tomas.ruiz@email.com', '1166778899', '2024-05-30', 4, 'Avanzado', True),
        ('Emma', 'Vargas', '66778899', 'emma.vargas@email.com', '1177889900', '2024-06-10', 1, 'Intermedio', True)
    ]
)

SEEDS['PAGOS'] = (
    "INSERT INTO PAGOS (tipo, monto, fecha_pago, mes, anio, socio_id, alumno_id, metodo_pago, observaciones) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    [
        ('cuota_socio', 15000.00, '2024-11-05', 11, 2024, 1, None, 'Transferencia', 'Pago puntual'),
        ('cuota_socio', 15000.00, '2024-11-08', 11, 2024, 2, None, 'Efectivo', None),
        ('cuota_socio', 15000.00, '2024-11-10', 11, 2024, 3, None, 'Débito', None),
        ('abono_clase', 8000.00, '2024-11-06', 11, 2024, None, 1, 'Efectivo', 'Clases con Roberto González'),
        ('abono_clase', 8000.00, '2024-11-07', 11, 2024, None, 2, 'Transferencia', 'Clases con Roberto González'),
        ('abono_clase', 10000.00, '2024-11-09', 11, 2024, None, 3, 'Efectivo', 'Clases con Carlos Rodríguez'),
        ('cuota_socio', 15000.00, '2024-10-05', 10, 2024, 1, None, 'Transferencia', None),
        ('abono_clase', 8000.00, '2024-10-06', 10, 2024, None, 1, 'Efectivo', None)
    ]
)


def create_database(cursor):
    try:
        cursor.execute(
            f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'", )
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database already exists")
        else:
            print(err)
    else:
        print(f"Database {DB_NAME} created successfully.")


def create_tables(tables, cursor):

    for table_name in tables:
        table_description = tables[table_name]
        try:
            print(f"Creating table {table_name}: ", end="")
            cursor.execute(table_description)
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def seeds_tables(seed, cursor):
    for table_name in seed:
        seed_description = seed[table_name]
        try:
            print(f"Seeding table {table_name}: ", end="")
            cursor.executemany(seed_description[0], seed_description[1])
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


cxn = mysql.connector.connect(**DB_CONFIG)
cursor = cxn.cursor()
cursor.close()
cxn.close()

create_database(cursor)
CONF_DB = DB_CONFIG.copy()
CONF_DB['database'] = DB_NAME
cxn = mysql.connector.connect(**CONF_DB)
cursor = cxn.cursor()
create_tables(TABLES, cursor)
seeds_tables(SEEDS, cursor)
cxn.commit()
cursor.close()
cxn.close()