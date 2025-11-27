from app.database.conect_db import ConectDB

class ProfesorModel:
    def __init__(self, id: int = 0, nombre: str = "", apellido: str = "", especialidad: str = "", 
                 telefono: str = "", email: str = ""):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.telefono = telefono
        self.email = email

    def serializar(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "especialidad": self.especialidad,
            "telefono": self.telefono,
            "email": self.email
        }

    @staticmethod
    def deserializar(data: dict):
        return ProfesorModel(
            id=data.get("id", 0),
            nombre=data.get("nombre", ""),
            apellido=data.get("apellido", ""),
            especialidad=data.get("especialidad", ""),
            telefono=data.get("telefono", ""),
            email=data.get("email", "")
        )

    @staticmethod
    def get_all():
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM PROFESORES")
                rows = cursor.fetchall()
                profesores = []
                if rows:
                    for row in rows:
                        profesores.append(row)
                    return profesores
                return []
        except Exception as exc:
            return {'mensaje': f"Error al listar instructores: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def get_by_id(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return None
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM PROFESORES WHERE id = %s", (id,))
                row = cursor.fetchone()
                if row:
                    return ProfesorModel(
                        id=row['id'],
                        nombre=row['nombre'],
                        apellido=row['apellido'],
                        especialidad=row['especialidad'],
                        telefono=row['telefono'],
                        email=row['email']
                    )
                return None
        except Exception as exc:
            return {'mensaje': f"Error al obtener instructor: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def create(profesor_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO PROFESORES (nombre, apellido, especialidad, telefono, email)
                    VALUES (%s, %s, %s, %s, %s)
                """, (profesor_data['nombre'], profesor_data['apellido'], 
                      profesor_data['especialidad'], profesor_data['telefono'], 
                      profesor_data['email']))
                cnx.commit()
                return {'mensaje': 'Profesor creado exitosamente', 'id': cursor.lastrowid}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al crear instructor: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def update(id, profesor_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    UPDATE PROFESORES 
                    SET nombre = %s, apellido = %s, especialidad = %s, telefono = %s, email = %s
                    WHERE id = %s
                """, (profesor_data['nombre'], profesor_data['apellido'], 
                      profesor_data['especialidad'], profesor_data['telefono'], 
                      profesor_data['email'], id))
                cnx.commit()
                return {'mensaje': 'Profesor actualizado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al actualizar instructor: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def delete(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("DELETE FROM PROFESORES WHERE id = %s", (id,))
                cnx.commit()
                return {'mensaje': 'Profesor eliminado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al eliminar instructor: {exc}"}
        finally:
            cnx.close()
