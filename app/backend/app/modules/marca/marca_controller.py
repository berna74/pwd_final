from .marca_model import MarcaModel

class MarcaController:
     @staticmethod
     def get_all():
        marcas = MarcaModel.get_all()
        return marcas
    
     @staticmethod
     def get_one(id):
        marca = MarcaModel(id=id).get_by_id()
        return marca
     @staticmethod
     def crear(data:dict):
        marca = MarcaModel(nombre=data['nombre'])
        result= marca.create()
        return result
        
     @staticmethod
     def modificar(data:dict):
        marca = MarcaModel(id=data['id'], nombre=data['nombre'])
        result = marca.update()
        return result
        
     @staticmethod    
     def eliminar(id):
        result = MarcaModel.delete(id)
        return result