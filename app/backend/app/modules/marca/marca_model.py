from ...database.conect_db import ConectDB

class MarcaModel:
    def __init__(self, id: int=0, nombre: str=""):
        self.id = id
        self.nombre = nombre

    def serializar(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }

    @staticmethod
    def deserializar(data: dict):
        return MarcaModel(
            id=data['id'],
            nombre=data['nombre'],
            )
        
    @staticmethod
    def get_all():
        cnx = ConectDB.get_connect()
        if cnx is None:
           return {'mensaje': 'No se pudo conectar a la base de datos'}
        with cnx.cursor(dictionary=True) as cursor:
            try:
                # ejecuto la query
                cursor.execute(f"SELECT * FROM MARCAS")
                # guardo en una variable el resultado
                rows = cursor.fetchall()
                # lista de diccionarios
                marcas = []
                if rows:
                    for row in rows:
                        marcas.append(row)
                    return marcas                
                return False
            # si ocurre una excepción, solo imprime el error y no devuelve nada
            except Exception as exc:
                return {'mensaje': f" error al listar marcas {exc}"}
            finally:
                cnx.close()
    @staticmethod    
    def get_by_id(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return None
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM MARCAS WHERE id = %s", (id,))
                row = cursor.fetchone()
                if row:
                    return MarcaModel(id=row['id'], nombre=row['nombre'])
                return None
        finally:
            cnx.close()
                
    def create(self):
        cnx = ConectDB.get_connect()
        with cnx.cursor() as cursor:
            try:
                # ejecuto la query
                cursor.execute("INSERT INTO MARCAS (nombre) VALUES (%s)", 
                               (self.nombre,))
                result = cursor.rowcount
                cnx.commit()
                if result > 0:
                    return True
                return False
                
            except Exception as exc:
                cnx.rollback()
                print(f" error crear una marca {exc}")
            finally:
                cnx.close()
        
    def update(self):
        cnx = ConectDB.get_connect()
        with cnx.cursor(dictionary=True) as cursor:
            try:
                # ejecuto la query
                cursor.execute("UPDATE MARCAS SET nombre = %s WHERE id = %s", 
                               (self.nombre, self.id))
                result = cursor.rowcount
                cnx.commit()
                
                if result > 0:
                    return True
                return False
                
            except Exception as exc:
                cnx.rollback()
                return {'mensaje':f" error al actualizar una marca {exc}"}
            finally:
                cnx.close()
                
    @staticmethod
    def delete(id:int):
        cnx = ConectDB.get_connect()
        with cnx.cursor(dictionary=True) as cursor:
            try:
                # ejecuto la query
                cursor.execute("DELETE FROM MARCAS where id = %s ", 
                               (id,))
                result = cursor.rowcount
                cnx.commit()
                if result > 0:
                    return True
                return False
            except Exception as exc:
                cnx.rollback()
                return {'mensaje':f" error al buscar una marca {exc}"}
            finally:
                cnx.close()    