from app.database.conect_db import ConectDB

class CategoriaModel:
    def __init__(self, id: int = 0, nombre: str = "", descripcion: str = ""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    def serializar(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

    @staticmethod
    def deserializar(data: dict):
        return CategoriaModel(
            id=data.get("id", 0),
            nombre=data.get("nombre", ""),
            descripcion=data.get("descripcion", "")
        )

    @staticmethod
    def get_all():
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        with cnx.cursor(dictionary=True) as cursor:
            try:
                cursor.execute("SELECT * FROM CATEGORIAS")
                rows = cursor.fetchall()
                categorias = []
                if rows:
                    for row in rows:
                        categorias.append(row)
                    return categorias
                return False
            except Exception as exc:
                return {'mensaje': f"error al listar categorías {exc}"}
            finally:
                cnx.close()
    @staticmethod
    def get_by_id(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return None
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM CATEGORIAS WHERE id = %s", (id,))
                row = cursor.fetchone()
                if row:
                    return CategoriaModel(id=row['id'], nombre=row['nombre'], descripcion=row.get('descripcion', ''))
                return None
        finally:
            cnx.close()

    def create(self):
        cnx = ConectDB.get_connect()
        with cnx.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO CATEGORIAS (nombre, descripcion) VALUES (%s, %s)", (self.nombre, self.descripcion))
                result = cursor.rowcount
                cnx.commit()
                if result > 0:
                    return True
                return False
            except Exception as exc:
                cnx.rollback()
                print(f"error crear una categoría {exc}")
            finally:
                cnx.close()

    def update(self):
        cnx = ConectDB.get_connect()
        with cnx.cursor(dictionary=True) as cursor:
            try:
                cursor.execute("UPDATE CATEGORIAS SET nombre = %s, descripcion = %s WHERE id = %s", (self.nombre, self.descripcion, self.id))
                result = cursor.rowcount
                cnx.commit()
                if result > 0:
                    return True
                return False
            except Exception as exc:
                cnx.rollback()
                return {'mensaje': f"error al modificar una categoría {exc}"}
            finally:
                cnx.close()

    @staticmethod
    def delete(id: int):
        cnx = ConectDB.get_connect()
        with cnx.cursor(dictionary=True) as cursor:
            try:
                cursor.execute("DELETE FROM CATEGORIAS WHERE id = %s", (id,))
                result = cursor.rowcount
                cnx.commit()
                if result > 0:
                    return True
                return False
            except Exception as exc:
                cnx.rollback()
                return {'mensaje': f"error al eliminar una categoría {exc}"}
            finally:
                cnx.close()