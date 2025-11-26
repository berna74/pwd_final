from app.database.conect_db import ConectDB
from app.modules.marca.marca_model import MarcaModel
from app.modules.categoria.categoria_model import CategoriaModel
from app.modules.proveedor.proveedor_model import ProveedorModel

class ArticuloModel:
    def __init__(self, id: int = 0, descripcion: str = "", precio: float = 0.0, stock: int = 0, 
                 marca: object = MarcaModel, proveedor: object = ProveedorModel, categorias: list = []):
        self.id = id
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.marca = marca
        self.proveedor = proveedor
        self.categorias = categorias  # Lista de CategoriaModel

    def serializar(self) -> dict:
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'marca': self.marca.serializar(),
            'proveedor': self.proveedor.serializar(),
            'categorias': [categoria.serializar() for categoria in self.categorias]
        }

    @staticmethod
    def deserializar(data: dict):
        return ArticuloModel(
            id=data['id'],
            descripcion=data['descripcion'],
            precio=data['precio'],
            stock=data['stock'],
            marca=MarcaModel.deserializar(data['marca']),
            proveedor=ProveedorModel.deserializar(data['proveedor']),
            categorias=[CategoriaModel.deserializar(c) for c in data['categorias']]
        )

    @staticmethod
    def get_all():
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor(dictionary=True) as cursor:
                # Obtengo todos los artículos
                cursor.execute("SELECT * FROM ARTICULOS")
                rows = cursor.fetchall()
                articulos = []
                if rows:
                    for row in rows:
                        # Obtengo la marca asociada
                        marca_row = MarcaModel.get_by_id(row['marca_id'])
                        
                        # Obtengo el proveedor asociado
                        proveedor_row = ProveedorModel.get_by_id(row['proveedor_id'])
                        
                        # Obtengo las categorías asociadas
                        cursor.execute("SELECT categoria_id FROM ARTICULOS_CATEGORIAS WHERE articulo_id = %s", (row['id'],))
                        categoria_ids = cursor.fetchall()
                        categorias = [CategoriaModel.get_by_id(c['categoria_id']) for c in categoria_ids]
                        
                        # Construyo el artículo con los datos obtenidos
                        articulo = ArticuloModel(
                            id=row['id'],
                            descripcion=row['descripcion'],
                            precio=row['precio'],
                            stock=row['stock'],
                            marca=marca_row,
                            proveedor=proveedor_row,
                            categorias=categorias
                        )
                        articulos.append(articulo.serializar())
                    return articulos
                return []
        except Exception as exc:
            return {'mensaje': f"Error al listar artículos: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def get_by_id(articulo_id: int):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor(dictionary=True) as cursor:
                # Obtengo el artículo por ID
                cursor.execute("SELECT * FROM articulos WHERE id = %s", (articulo_id,))
                row = cursor.fetchone()
                if row:
                       marca_row = MarcaModel.get_by_id(row['marca_id'])
                       proveedor_row = ProveedorModel.get_by_id(row['proveedor_id'])
                       cursor.execute("SELECT categoria_id FROM articulos_categorias WHERE articulo_id = %s", (row['id'],))
                       categoria_ids = cursor.fetchall()
                       categorias = [CategoriaModel.get_by_id(c['categoria_id']) for c in categoria_ids]
                       articulo = ArticuloModel(
                           id=row['id'],
                           descripcion=row['descripcion'],
                           precio=row['precio'],
                           stock=row['stock'],
                           marca=marca_row,
                           proveedor=proveedor_row,
                           categorias=categorias
                       )
                       return articulo.serializar()
                return {}
        except Exception as exc:
            return {'mensaje': f"Error al buscar un artículo: {exc}"}
        finally:
            cnx.close()

    def create(self):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                # Inserto el artículo
                cursor.execute(
                    "INSERT INTO ARTICULOS (descripcion, precio, stock, marca_id, proveedor_id) VALUES (%s, %s, %s, %s, %s)",
                    (self.descripcion, self.precio, self.stock, self.marca.id, self.proveedor.id)
                )
                articulo_id = cursor.lastrowid
                cnx.commit()
                
                # Inserto las categorías si existen
                if self.categorias:
                    for categoria in self.categorias:
                        cursor.execute(
                            "INSERT INTO ARTICULOS_CATEGORIAS (articulo_id, categoria_id) VALUES (%s, %s)",
                            (articulo_id, categoria.id)
                        )
                    cnx.commit()
                
                return True if articulo_id > 0 else False
                
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al crear un artículo: {exc}"}
        finally:
            cnx.close()

    def update(self):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                # Actualizo el artículo
                cursor.execute(
                    "UPDATE ARTICULOS SET descripcion = %s, precio = %s, stock = %s, marca_id = %s, proveedor_id = %s WHERE id = %s",
                    (self.descripcion, self.precio, self.stock, self.marca.id, self.proveedor.id, self.id)
                )
                result = cursor.rowcount
                
                # Elimino las categorías existentes
                cursor.execute("DELETE FROM ARTICULOS_CATEGORIAS WHERE articulo_id = %s", (self.id,))
                
                # Inserto las nuevas categorías
                if self.categorias:
                    for categoria in self.categorias:
                        cursor.execute(
                            "INSERT INTO ARTICULOS_CATEGORIAS (articulo_id, categoria_id) VALUES (%s, %s)",
                            (self.id, categoria.id)
                        )
                
                cnx.commit()
                return True if result > 0 else False
                
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al actualizar un artículo: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def delete(articulo_id: int):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                # Elimino las categorías asociadas primero
                cursor.execute("DELETE FROM ARTICULOS_CATEGORIAS WHERE articulo_id = %s", (articulo_id,))
                
                # Elimino el artículo
                cursor.execute("DELETE FROM ARTICULOS WHERE id = %s", (articulo_id,))
                result = cursor.rowcount
                cnx.commit()
                
                return True if result > 0 else False
                
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al eliminar un artículo: {exc}"}
        finally:
            cnx.close()