from app.database.conect_db import ConectDB

class ProveedorModel:
    def __init__(self, id=0, nombre="", telefono="", direccion="", email=""):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "email": self.email
        }
        
    @staticmethod
    def deserializar(data: dict):
        return ProveedorModel(
            id=data['id'],
            nombre=data['nombre'],
            telefono=data['telefono'],
            direccion=data['direccion'],
            email=data['email'] 
            )


    @staticmethod
    def get_all():
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        with cnx.cursor(dictionary=True) as cursor:
            try:
                cursor.execute("SELECT * FROM PROVEEDORES")
                rows = cursor.fetchall()
                return rows if rows else False
            except Exception as exc:
                return {'mensaje': f"error al listar proveedores {exc}"}
            finally:
                cnx.close()

    @staticmethod
    def get_by_id(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return None
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM PROVEEDORES WHERE id = %s", (id,))
                row = cursor.fetchone()
                if row:
                    return ProveedorModel(
                        id=row['id'],
                        nombre=row['nombre'],
                        telefono=row['telefono'],
                        direccion=row['direccion'],
                        email=row['email']
                    )
                return None
        finally:
            cnx.close()
                
    def create(self):
        cnx = ConectDB.get_connect()
        with cnx.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO PROVEEDORES (nombre, telefono, direccion, email) VALUES (%s, %s, %s, %s)",
                    (self.nombre, self.telefono, self.direccion, self.email)
                )
                cnx.commit()
                return cursor.rowcount > 0
            except Exception as exc:
                cnx.rollback()
                print(f"error crear proveedor {exc}")
                return False
            finally:
                cnx.close()

    def update(self):
        cnx = ConectDB.get_connect()
        with cnx.cursor() as cursor:
            try:
                cursor.execute(
                    "UPDATE PROVEEDORES SET nombre = %s, telefono = %s, direccion = %s, email = %s WHERE id = %s",
                    (self.nombre, self.telefono, self.direccion, self.email, self.id)
                )
                cnx.commit()
                return cursor.rowcount > 0
            except Exception as exc:
                cnx.rollback()
                print(f"error modificar proveedor {exc}")
                return False
            finally:
                cnx.close()

    @staticmethod
    def delete(id):
        cnx = ConectDB.get_connect()
        with cnx.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM PROVEEDORES WHERE id = %s", (id,))
                cnx.commit()
                return cursor.rowcount > 0
            except Exception as exc:
                cnx.rollback()
                print(f"error eliminar proveedor {exc}")
                return False
            finally:
                cnx.close()
