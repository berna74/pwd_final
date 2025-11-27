from app.database.conect_db import ConectDB
from app.modules.categoria.categoria_model import CategoriaModel
from app.modules.profesor.profesor_model import ProfesorModel

class SocioModel:
    def __init__(self, id: int = 0, nombre: str = "", apellido: str = "", dni: str = "", 
                 email: str = "", telefono: str = "", fecha_inscripcion: str = "",
                 profesor: object = ProfesorModel, categorias: list = []):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.fecha_inscripcion = fecha_inscripcion
        self.profesor = profesor
        self.categorias = categorias  # Lista de CategoriaModel

    def serializar(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_inscripcion': self.fecha_inscripcion,
            'profesor': self.profesor.serializar(),
            'categorias': [categoria.serializar() for categoria in self.categorias]
        }

    @staticmethod
    def deserializar(data: dict):
        return SocioModel(
            id=data['id'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            email=data['email'],
            telefono=data['telefono'],
            fecha_inscripcion=data['fecha_inscripcion'],
            profesor=ProfesorModel.deserializar(data['profesor']),
            categorias=[CategoriaModel.deserializar(c) for c in data['categorias']]
        )

    @staticmethod
    def get_all():
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor(dictionary=True) as cursor:
                # Obtengo todos los socios
                cursor.execute("SELECT * FROM SOCIOS")
                rows = cursor.fetchall()
                socios = []
                for row in rows:
                    # Obtengo el profesor
                    cursor.execute("SELECT * FROM PROFESORES WHERE id = %s", (row['profesor_id'],))
                    profesor_row = cursor.fetchone()
                    profesor = ProfesorModel.deserializar(profesor_row)
                    
                    # Obtengo las categorías del socio
                    cursor.execute("""
                        SELECT c.* FROM CATEGORIAS c
                        INNER JOIN SOCIO_CATEGORIA sc ON c.id = sc.categoria_id
                        WHERE sc.socio_id = %s
                    """, (row['id'],))
                    categorias_rows = cursor.fetchall()
                    categorias = [CategoriaModel.deserializar(cat) for cat in categorias_rows]
                    
                    socio = SocioModel(
                        id=row['id'],
                        nombre=row['nombre'],
                        apellido=row['apellido'],
                        dni=row['dni'],
                        email=row['email'],
                        telefono=row['telefono'],
                        fecha_inscripcion=str(row['fecha_inscripcion']),
                        profesor=profesor,
                        categorias=categorias
                    )
                    socios.append(socio.serializar())
                return socios
        except Exception as exc:
            return {'mensaje': f"Error al listar socios: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def get_by_id(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return None
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM SOCIOS WHERE id = %s", (id,))
                row = cursor.fetchone()
                if not row:
                    return None
                
                # Obtengo el profesor
                cursor.execute("SELECT * FROM PROFESORES WHERE id = %s", (row['profesor_id'],))
                profesor_row = cursor.fetchone()
                profesor = ProfesorModel.deserializar(profesor_row)
                
                # Obtengo las categorías del socio
                cursor.execute("""
                    SELECT c.* FROM CATEGORIAS c
                    INNER JOIN SOCIO_CATEGORIA sc ON c.id = sc.categoria_id
                    WHERE sc.socio_id = %s
                """, (id,))
                categorias_rows = cursor.fetchall()
                categorias = [CategoriaModel.deserializar(cat) for cat in categorias_rows]
                
                socio = SocioModel(
                    id=row['id'],
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    dni=row['dni'],
                    email=row['email'],
                    telefono=row['telefono'],
                    fecha_inscripcion=str(row['fecha_inscripcion']),
                    profesor=profesor,
                    categorias=categorias
                )
                return socio.serializar()
        except Exception as exc:
            return {'mensaje': f"Error al obtener socio: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def create(socio_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO SOCIOS (nombre, apellido, dni, email, telefono, fecha_inscripcion, profesor_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (socio_data['nombre'], socio_data['apellido'], socio_data['dni'], 
                      socio_data['email'], socio_data['telefono'], socio_data['fecha_inscripcion'],
                      socio_data['profesor_id']))
                
                socio_id = cursor.lastrowid
                
                # Insertar categorías
                if 'categorias' in socio_data:
                    for categoria_id in socio_data['categorias']:
                        cursor.execute("""
                            INSERT INTO SOCIO_CATEGORIA (socio_id, categoria_id)
                            VALUES (%s, %s)
                        """, (socio_id, categoria_id))
                
                cnx.commit()
                return {'mensaje': 'Socio creado exitosamente', 'id': socio_id}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al crear socio: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def update(id, socio_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    UPDATE SOCIOS 
                    SET nombre = %s, apellido = %s, dni = %s, email = %s, telefono = %s, 
                        fecha_inscripcion = %s, profesor_id = %s
                    WHERE id = %s
                """, (socio_data['nombre'], socio_data['apellido'], socio_data['dni'],
                      socio_data['email'], socio_data['telefono'], socio_data['fecha_inscripcion'],
                      socio_data['profesor_id'], id))
                
                # Actualizar categorías
                cursor.execute("DELETE FROM SOCIO_CATEGORIA WHERE socio_id = %s", (id,))
                if 'categorias' in socio_data:
                    for categoria_id in socio_data['categorias']:
                        cursor.execute("""
                            INSERT INTO SOCIO_CATEGORIA (socio_id, categoria_id)
                            VALUES (%s, %s)
                        """, (id, categoria_id))
                
                cnx.commit()
                return {'mensaje': 'Socio actualizado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al actualizar socio: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def delete(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                # Eliminar relaciones con categorías
                cursor.execute("DELETE FROM SOCIO_CATEGORIA WHERE socio_id = %s", (id,))
                
                # Eliminar socio
                cursor.execute("DELETE FROM SOCIOS WHERE id = %s", (id,))
                cnx.commit()
                return {'mensaje': 'Socio eliminado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al eliminar socio: {exc}"}
        finally:
            cnx.close()
