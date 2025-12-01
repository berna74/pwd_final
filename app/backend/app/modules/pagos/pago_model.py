from app.database.conect_db import ConectDB

class PagoModel:
    def __init__(self, id: int = 0, tipo: str = "", monto: float = 0.0, fecha_pago: str = "",
                 mes: int = 0, anio: int = 0, socio_id: int = None, alumno_id: int = None,
                 profesor_id: int = None, metodo_pago: str = "", observaciones: str = "", 
                 socio_nombre: str = "", alumno_nombre: str = "", profesor_nombre: str = ""):
        self.id = id
        self.tipo = tipo
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.mes = mes
        self.anio = anio
        self.socio_id = socio_id
        self.alumno_id = alumno_id
        self.profesor_id = profesor_id
        self.metodo_pago = metodo_pago
        self.observaciones = observaciones
        self.socio_nombre = socio_nombre
        self.alumno_nombre = alumno_nombre
        self.profesor_nombre = profesor_nombre

    def serializar(self) -> dict:
        return {
            'id': self.id,
            'tipo': self.tipo,
            'monto': float(self.monto),
            'fecha_pago': self.fecha_pago,
            'mes': self.mes,
            'anio': self.anio,
            'socio_id': self.socio_id,
            'alumno_id': self.alumno_id,
            'profesor_id': self.profesor_id,
            'metodo_pago': self.metodo_pago,
            'observaciones': self.observaciones,
            'socio_nombre': self.socio_nombre,
            'alumno_nombre': self.alumno_nombre,
            'profesor_nombre': self.profesor_nombre
        }

    @staticmethod
    def get_all():
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT p.*, 
                           CONCAT(s.nombre, ' ', s.apellido) as socio_nombre,
                           CONCAT(a.nombre, ' ', a.apellido) as alumno_nombre,
                           CONCAT(pr.nombre, ' ', pr.apellido) as profesor_nombre
                    FROM PAGOS p
                    LEFT JOIN SOCIOS s ON p.socio_id = s.id
                    LEFT JOIN ALUMNOS a ON p.alumno_id = a.id
                    LEFT JOIN PROFESORES pr ON p.profesor_id = pr.id
                    ORDER BY p.fecha_pago DESC, p.id DESC
                """)
                rows = cursor.fetchall()
                pagos = []
                for row in rows:
                    pago = PagoModel(
                        id=row['id'],
                        tipo=row['tipo'],
                        monto=float(row['monto']),
                        fecha_pago=str(row['fecha_pago']),
                        mes=row['mes'],
                        anio=row['anio'],
                        socio_id=row['socio_id'],
                        alumno_id=row['alumno_id'],
                        profesor_id=row['profesor_id'],
                        metodo_pago=row['metodo_pago'],
                        observaciones=row['observaciones'],
                        socio_nombre=row.get('socio_nombre', ''),
                        alumno_nombre=row.get('alumno_nombre', ''),
                        profesor_nombre=row.get('profesor_nombre', '')
                    )
                    pagos.append(pago.serializar())
                return pagos
        except Exception as exc:
            return {'mensaje': f"Error al listar pagos: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def get_by_id(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return None
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT p.*, 
                           CONCAT(s.nombre, ' ', s.apellido) as socio_nombre,
                           CONCAT(a.nombre, ' ', a.apellido) as alumno_nombre,
                           CONCAT(pr.nombre, ' ', pr.apellido) as profesor_nombre
                    FROM PAGOS p
                    LEFT JOIN SOCIOS s ON p.socio_id = s.id
                    LEFT JOIN ALUMNOS a ON p.alumno_id = a.id
                    LEFT JOIN PROFESORES pr ON p.profesor_id = pr.id
                    WHERE p.id = %s
                """, (id,))
                row = cursor.fetchone()
                if not row:
                    return None
                
                pago = PagoModel(
                    id=row['id'],
                    tipo=row['tipo'],
                    monto=float(row['monto']),
                    fecha_pago=str(row['fecha_pago']),
                    mes=row['mes'],
                    anio=row['anio'],
                    socio_id=row['socio_id'],
                    alumno_id=row['alumno_id'],
                    profesor_id=row['profesor_id'],
                    metodo_pago=row['metodo_pago'],
                    observaciones=row['observaciones'],
                    socio_nombre=row.get('socio_nombre', ''),
                    alumno_nombre=row.get('alumno_nombre', ''),
                    profesor_nombre=row.get('profesor_nombre', '')
                )
                return pago.serializar()
        except Exception as exc:
            return {'mensaje': f"Error al obtener pago: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def create(pago_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO PAGOS (tipo, monto, fecha_pago, mes, anio, socio_id, alumno_id, profesor_id, metodo_pago, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (pago_data['tipo'], pago_data['monto'], pago_data['fecha_pago'],
                      pago_data['mes'], pago_data['anio'], pago_data.get('socio_id'),
                      pago_data.get('alumno_id'), pago_data.get('profesor_id'),
                      pago_data.get('metodo_pago'), pago_data.get('observaciones')))
                
                pago_id = cursor.lastrowid
                cnx.commit()
                return {'mensaje': 'Pago registrado exitosamente', 'id': pago_id}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al registrar pago: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def update(id, pago_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    UPDATE PAGOS 
                    SET tipo = %s, monto = %s, fecha_pago = %s, mes = %s, anio = %s,
                        socio_id = %s, alumno_id = %s, profesor_id = %s, metodo_pago = %s, observaciones = %s
                    WHERE id = %s
                """, (pago_data['tipo'], pago_data['monto'], pago_data['fecha_pago'],
                      pago_data['mes'], pago_data['anio'], pago_data.get('socio_id'),
                      pago_data.get('alumno_id'), pago_data.get('profesor_id'),
                      pago_data.get('metodo_pago'), pago_data.get('observaciones'), id))
                
                cnx.commit()
                return {'mensaje': 'Pago actualizado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al actualizar pago: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def delete(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("DELETE FROM PAGOS WHERE id = %s", (id,))
                cnx.commit()
                return {'mensaje': 'Pago eliminado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al eliminar pago: {exc}"}
        finally:
            cnx.close()
