from app.database.conect_db import ConectDB
from app.modules.profesor.profesor_model import ProfesorModel

class AlumnoModel:
    def __init__(self, id: int = 0, nombre: str = "", apellido: str = "", dni: str = "", 
                 email: str = "", telefono: str = "", fecha_inscripcion: str = "",
                 profesor: object = ProfesorModel, nivel: str = "", activo: bool = True):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.fecha_inscripcion = fecha_inscripcion
        self.profesor = profesor
        self.nivel = nivel
        self.activo = activo

    def serializar(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_inscripcion': self.fecha_inscripcion,
            'profesor': self.profesor.serializar() if hasattr(self.profesor, 'serializar') else None,
            'nivel': self.nivel,
            'activo': self.activo
        }

    @staticmethod
    def deserializar(data: dict):
        return AlumnoModel(
            id=data['id'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            email=data['email'],
            telefono=data['telefono'],
            fecha_inscripcion=data['fecha_inscripcion'],
            profesor=ProfesorModel.deserializar(data['profesor']) if data.get('profesor') else None,
            nivel=data.get('nivel', ''),
            activo=data.get('activo', True)
        )

    @staticmethod
    def get_all():
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM ALUMNOS")
                rows = cursor.fetchall()
                alumnos = []
                for row in rows:
                    cursor.execute("SELECT * FROM PROFESORES WHERE id = %s", (row['profesor_id'],))
                    profesor_row = cursor.fetchone()
                    profesor = ProfesorModel.deserializar(profesor_row) if profesor_row else None
                    
                    alumno = AlumnoModel(
                        id=row['id'],
                        nombre=row['nombre'],
                        apellido=row['apellido'],
                        dni=row['dni'],
                        email=row['email'],
                        telefono=row['telefono'],
                        fecha_inscripcion=str(row['fecha_inscripcion']),
                        profesor=profesor,
                        nivel=row.get('nivel', ''),
                        activo=bool(row.get('activo', True))
                    )
                    alumnos.append(alumno.serializar())
                return alumnos
        except Exception as exc:
            return {'mensaje': f"Error al listar alumnos: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def get_by_id(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return None
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM ALUMNOS WHERE id = %s", (id,))
                row = cursor.fetchone()
                if not row:
                    return None
                
                cursor.execute("SELECT * FROM PROFESORES WHERE id = %s", (row['profesor_id'],))
                profesor_row = cursor.fetchone()
                profesor = ProfesorModel.deserializar(profesor_row) if profesor_row else None
                
                alumno = AlumnoModel(
                    id=row['id'],
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    dni=row['dni'],
                    email=row['email'],
                    telefono=row['telefono'],
                    fecha_inscripcion=str(row['fecha_inscripcion']),
                    profesor=profesor,
                    nivel=row.get('nivel', ''),
                    activo=bool(row.get('activo', True))
                )
                return alumno.serializar()
        except Exception as exc:
            return {'mensaje': f"Error al obtener alumno: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def create(alumno_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ALUMNOS (nombre, apellido, dni, email, telefono, fecha_inscripcion, profesor_id, nivel, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (alumno_data['nombre'], alumno_data['apellido'], alumno_data['dni'], 
                      alumno_data['email'], alumno_data['telefono'], alumno_data['fecha_inscripcion'],
                      alumno_data['profesor_id'], alumno_data.get('nivel', ''), alumno_data.get('activo', True)))
                
                alumno_id = cursor.lastrowid
                cnx.commit()
                return {'mensaje': 'Alumno creado exitosamente', 'id': alumno_id}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al crear alumno: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def update(id, alumno_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    UPDATE ALUMNOS 
                    SET nombre = %s, apellido = %s, dni = %s, email = %s, telefono = %s, 
                        fecha_inscripcion = %s, profesor_id = %s, nivel = %s, activo = %s
                    WHERE id = %s
                """, (alumno_data['nombre'], alumno_data['apellido'], alumno_data['dni'],
                      alumno_data['email'], alumno_data['telefono'], alumno_data['fecha_inscripcion'],
                      alumno_data['profesor_id'], alumno_data.get('nivel', ''), 
                      alumno_data.get('activo', True), id))
                
                cnx.commit()
                return {'mensaje': 'Alumno actualizado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al actualizar alumno: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def delete(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("DELETE FROM ALUMNOS WHERE id = %s", (id,))
                cnx.commit()
                return {'mensaje': 'Alumno eliminado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al eliminar alumno: {exc}"}
        finally:
            cnx.close()
