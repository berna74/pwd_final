from .articulo_model import ArticuloModel
from app.modules.marca.marca_model import MarcaModel
from app.modules.proveedor.proveedor_model import ProveedorModel

class ArticuloController:
     @staticmethod
     def get_all():
        articulos = ArticuloModel.get_all()
        return articulos
    
     @staticmethod
     def get_one(id):
        articulo = ArticuloModel(id=id).get_by_id()
        return articulo
     @staticmethod
     def crear(data:dict):
        # get_by_id ya devuelve un objeto MarcaModel, no necesita deserializar
        marca = MarcaModel.get_by_id(data['marca_id'])
        proveedor = ProveedorModel.get_by_id(data['proveedor_id'])
        articulo = ArticuloModel(
            descripcion=data['descripcion'], 
            precio=data['precio'], 
            stock=data['stock'], 
            marca=marca,
            proveedor=proveedor
        )
        result= articulo.create()
        return result
        
     @staticmethod
     def modificar(data:dict):
         # Obtengo las instancias de marca y proveedor
         marca = MarcaModel.get_by_id(data['marca_id'])
         proveedor = ProveedorModel.get_by_id(data['proveedor_id'])
         
         # Obtengo las categorías si existen
         from app.modules.categoria.categoria_model import CategoriaModel
         categorias = []
         if 'categorias' in data and data['categorias']:
             categorias = [CategoriaModel.get_by_id(cat_id) for cat_id in data['categorias']]
         
         # Creo el artículo con todos los datos
         articulo = ArticuloModel(
             id=data['id'],
             descripcion=data['descripcion'], 
             precio=data['precio'], 
             stock=data['stock'], 
             marca=marca,
             proveedor=proveedor,
             categorias=categorias
         )
         result = articulo.update()
         return result
        
     @staticmethod    
     def eliminar(id):
        result = ArticuloModel.delete(id)
        return result