from app.database.conect_db import ConectDB
from datetime import datetime

class TurnoModel:
    def __init__(self, id: int = 0, cancha: str = "", fecha: str = "", hora_inicio: str = "", 
                 hora_fin: str = "", socio_reserva_id: int = 0, socio_reserva_nombre: str = "",
                 jugadores: list = [], estado: str = "disponible"):
        self.id = id
        self.cancha = cancha
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.socio_reserva_id = socio_reserva_id
        self.socio_reserva_nombre = socio_reserva_nombre
        self.jugadores = jugadores
        self.estado = estado

    def serializar(self) -> dict:
        return {
            "id": self.id,
            "cancha": self.cancha,
            "fecha": self.fecha,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "socio_reserva_id": self.socio_reserva_id,
            "socio_reserva_nombre": self.socio_reserva_nombre,
            "jugadores": self.jugadores,
            "estado": self.estado
        }

    @staticmethod
    def deserializar(data: dict):
        return TurnoModel(
            id=data.get("id", 0),
            cancha=data.get("cancha", ""),
            fecha=data.get("fecha", ""),
            hora_inicio=data.get("hora_inicio", ""),
            hora_fin=data.get("hora_fin", ""),
            socio_reserva_id=data.get("socio_reserva_id", 0),
            socio_reserva_nombre=data.get("socio_reserva_nombre", ""),
            jugadores=data.get("jugadores", []),
            estado=data.get("estado", "disponible")
        )

    @staticmethod
    def get_all():
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT t.*, s.nombre as socio_reserva_nombre, s.apellido as socio_reserva_apellido
                    FROM TURNOS t
                    LEFT JOIN SOCIOS s ON t.socio_reserva_id = s.id
                    ORDER BY t.fecha DESC, t.hora_inicio ASC
                """)
                rows = cursor.fetchall()
                turnos = []
                if rows:
                    for row in rows:
                        cursor.execute("""
                            SELECT jugador_nombre FROM TURNO_JUGADORES
                            WHERE turno_id = %s
                        """, (row['id'],))
                        jugadores_rows = cursor.fetchall()
                        jugadores = [j['jugador_nombre'] for j in jugadores_rows]
                        
                        socio_nombre = ""
                        if row.get('socio_reserva_nombre'):
                            socio_nombre = f"{row['socio_reserva_nombre']} {row.get('socio_reserva_apellido', '')}"
                        
                        turno = {
                            'id': row['id'],
                            'cancha': row['cancha'],
                            'fecha': str(row['fecha']),
                            'hora_inicio': str(row['hora_inicio']),
                            'hora_fin': str(row['hora_fin']),
                            'socio_reserva_id': row['socio_reserva_id'],
                            'socio_reserva_nombre': socio_nombre,
                            'jugadores': jugadores,
                            'estado': row['estado']
                        }
                        turnos.append(turno)
                    return turnos
                return []
        except Exception as exc:
            return {'mensaje': f"Error al listar turnos: {exc}"}
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
                    SELECT t.*, s.nombre as socio_reserva_nombre, s.apellido as socio_reserva_apellido
                    FROM TURNOS t
                    LEFT JOIN SOCIOS s ON t.socio_reserva_id = s.id
                    WHERE t.id = %s
                """, (id,))
                row = cursor.fetchone()
                if row:
                    cursor.execute("""
                        SELECT jugador_nombre FROM TURNO_JUGADORES
                        WHERE turno_id = %s
                    """, (id,))
                    jugadores_rows = cursor.fetchall()
                    jugadores = [j['jugador_nombre'] for j in jugadores_rows]
                    
                    socio_nombre = ""
                    if row.get('socio_reserva_nombre'):
                        socio_nombre = f"{row['socio_reserva_nombre']} {row.get('socio_reserva_apellido', '')}"
                    
                    return TurnoModel(
                        id=row['id'],
                        cancha=row['cancha'],
                        fecha=str(row['fecha']),
                        hora_inicio=str(row['hora_inicio']),
                        hora_fin=str(row['hora_fin']),
                        socio_reserva_id=row['socio_reserva_id'],
                        socio_reserva_nombre=socio_nombre,
                        jugadores=jugadores,
                        estado=row['estado']
                    )
                return None
        except Exception as exc:
            return {'mensaje': f"Error al obtener turno: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def create(turno_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO TURNOS (cancha, fecha, hora_inicio, hora_fin, socio_reserva_id, estado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (turno_data['cancha'], turno_data['fecha'], turno_data['hora_inicio'],
                      turno_data['hora_fin'], turno_data.get('socio_reserva_id'),
                      turno_data.get('estado', 'reservado')))
                
                turno_id = cursor.lastrowid
                
                if 'jugadores' in turno_data and turno_data['jugadores']:
                    for jugador in turno_data['jugadores']:
                        if jugador.strip():
                            cursor.execute("""
                                INSERT INTO TURNO_JUGADORES (turno_id, jugador_nombre)
                                VALUES (%s, %s)
                            """, (turno_id, jugador.strip()))
                
                cnx.commit()
                return {'mensaje': 'Turno creado exitosamente', 'id': turno_id}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al crear turno: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def update(id, turno_data):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("""
                    UPDATE TURNOS 
                    SET cancha = %s, fecha = %s, hora_inicio = %s, hora_fin = %s, 
                        socio_reserva_id = %s, estado = %s
                    WHERE id = %s
                """, (turno_data['cancha'], turno_data['fecha'], turno_data['hora_inicio'],
                      turno_data['hora_fin'], turno_data.get('socio_reserva_id'),
                      turno_data.get('estado', 'reservado'), id))
                
                cursor.execute("DELETE FROM TURNO_JUGADORES WHERE turno_id = %s", (id,))
                if 'jugadores' in turno_data and turno_data['jugadores']:
                    for jugador in turno_data['jugadores']:
                        if jugador.strip():
                            cursor.execute("""
                                INSERT INTO TURNO_JUGADORES (turno_id, jugador_nombre)
                                VALUES (%s, %s)
                            """, (id, jugador.strip()))
                
                cnx.commit()
                return {'mensaje': 'Turno actualizado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al actualizar turno: {exc}"}
        finally:
            cnx.close()

    @staticmethod
    def delete(id):
        cnx = ConectDB.get_connect()
        if cnx is None:
            return {'mensaje': 'No se pudo conectar a la base de datos'}
        try:
            with cnx.cursor() as cursor:
                cursor.execute("DELETE FROM TURNO_JUGADORES WHERE turno_id = %s", (id,))
                cursor.execute("DELETE FROM TURNOS WHERE id = %s", (id,))
                cnx.commit()
                return {'mensaje': 'Turno eliminado exitosamente'}
        except Exception as exc:
            cnx.rollback()
            return {'mensaje': f"Error al eliminar turno: {exc}"}
        finally:
            cnx.close()
