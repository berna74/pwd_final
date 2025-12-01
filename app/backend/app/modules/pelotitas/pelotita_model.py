from app.database.conect_db import ConectDB

class Pelotita:
    def __init__(self, id=None, fecha=None, tipo=None, cantidad=None, precio_unitario=None, 
                 total=None, proveedor=None, comprador_tipo=None, comprador_id=None, 
                 comprador_nombre=None, observaciones=None, created_at=None, updated_at=None):
        self.id = id
        self.fecha = fecha
        self.tipo = tipo
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total = total
        self.proveedor = proveedor
        self.comprador_tipo = comprador_tipo
        self.comprador_id = comprador_id
        self.comprador_nombre = comprador_nombre
        self.observaciones = observaciones
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'fecha': str(self.fecha) if self.fecha else None,
            'tipo': self.tipo,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario) if self.precio_unitario else None,
            'total': float(self.total) if self.total else None,
            'proveedor': self.proveedor,
            'comprador_tipo': self.comprador_tipo,
            'comprador_id': self.comprador_id,
            'comprador_nombre': self.comprador_nombre,
            'observaciones': self.observaciones,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }

    @staticmethod
    def get_all():
        sql = """
            SELECT p.*, 
                   CASE 
                       WHEN p.comprador_tipo = 'socio' THEN CONCAT(s.nombre, ' ', s.apellido)
                       WHEN p.comprador_tipo = 'alumno' THEN CONCAT(a.nombre, ' ', a.apellido)
                       ELSE p.comprador_nombre
                   END as comprador_nombre_completo
            FROM PELOTITAS p
            LEFT JOIN SOCIOS s ON p.comprador_tipo = 'socio' AND p.comprador_id = s.id
            LEFT JOIN ALUMNOS a ON p.comprador_tipo = 'alumno' AND p.comprador_id = a.id
            ORDER BY p.fecha DESC, p.id DESC
        """
        results = ConectDB.read(sql)
        pelotitas = []
        for result in results:
            # Reemplazar comprador_nombre con el nombre completo si existe
            if result.get('comprador_nombre_completo'):
                result['comprador_nombre'] = result['comprador_nombre_completo']
            pelotita = Pelotita(**{k: v for k, v in result.items() if k != 'comprador_nombre_completo'})
            pelotitas.append(pelotita)
        return pelotitas

    @staticmethod
    def get_by_id(pelotita_id):
        sql = """
            SELECT p.*, 
                   CASE 
                       WHEN p.comprador_tipo = 'socio' THEN CONCAT(s.nombre, ' ', s.apellido)
                       WHEN p.comprador_tipo = 'alumno' THEN CONCAT(a.nombre, ' ', a.apellido)
                       ELSE p.comprador_nombre
                   END as comprador_nombre_completo
            FROM PELOTITAS p
            LEFT JOIN SOCIOS s ON p.comprador_tipo = 'socio' AND p.comprador_id = s.id
            LEFT JOIN ALUMNOS a ON p.comprador_tipo = 'alumno' AND p.comprador_id = a.id
            WHERE p.id = %s
        """
        result = ConectDB.read(sql, (pelotita_id,))
        if result:
            data = result[0]
            if data.get('comprador_nombre_completo'):
                data['comprador_nombre'] = data['comprador_nombre_completo']
            return Pelotita(**{k: v for k, v in data.items() if k != 'comprador_nombre_completo'})
        return None

    @staticmethod
    def create(data):
        sql = """
            INSERT INTO PELOTITAS (fecha, tipo, cantidad, precio_unitario, total, proveedor, 
                                   comprador_tipo, comprador_id, comprador_nombre, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('fecha'),
            data.get('tipo'),
            data.get('cantidad'),
            data.get('precio_unitario'),
            data.get('total'),
            data.get('proveedor'),
            data.get('comprador_tipo'),
            data.get('comprador_id'),
            data.get('comprador_nombre'),
            data.get('observaciones')
        )
        pelotita_id = ConectDB.write(sql, params)
        return Pelotita.get_by_id(pelotita_id)

    @staticmethod
    def update(pelotita_id, data):
        sql = """
            UPDATE PELOTITAS 
            SET fecha = %s, tipo = %s, cantidad = %s, precio_unitario = %s, 
                total = %s, proveedor = %s, comprador_tipo = %s, comprador_id = %s, 
                comprador_nombre = %s, observaciones = %s
            WHERE id = %s
        """
        params = (
            data.get('fecha'),
            data.get('tipo'),
            data.get('cantidad'),
            data.get('precio_unitario'),
            data.get('total'),
            data.get('proveedor'),
            data.get('comprador_tipo'),
            data.get('comprador_id'),
            data.get('comprador_nombre'),
            data.get('observaciones'),
            pelotita_id
        )
        ConectDB.write(sql, params)
        return Pelotita.get_by_id(pelotita_id)

    @staticmethod
    def delete(pelotita_id):
        sql = "DELETE FROM PELOTITAS WHERE id = %s"
        ConectDB.write(sql, (pelotita_id,))
        return True
    
    @staticmethod
    def get_resumen():
        """Obtiene resumen de compras y ventas"""
        sql = """
            SELECT 
                tipo,
                SUM(cantidad) as total_cantidad,
                SUM(total) as total_monto,
                COUNT(*) as total_registros
            FROM PELOTITAS
            GROUP BY tipo
        """
        results = ConectDB.read(sql)
        return results
