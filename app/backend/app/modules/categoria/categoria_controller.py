from .categoria_model import CategoriaModel

class CategoriaController:
    @staticmethod
    def get_all():
        return CategoriaModel.get_all()

    @staticmethod
    def get_one(id):
        return CategoriaModel(id=id).get_by_id()

    @staticmethod
    def crear(data):
        print(f"DEBUG - Controller crear recibe: {data}")
        print(f"DEBUG - Intentando acceder a data['nombre']: {data.get('nombre', 'NO EXISTE')}")
        categoria = CategoriaModel(nombre=data['nombre'])
        return categoria.create()

    @staticmethod
    def modificar(data):
        categoria = CategoriaModel(id=data['id'], nombre=data['nombre'])
        return categoria.update()

    @staticmethod
    def eliminar(id):
        return CategoriaModel.delete(id)