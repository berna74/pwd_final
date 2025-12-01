#!/usr/bin/env python3
"""
Script para migrar la tabla PAGOS
- Agregar campo profesor_id
- Actualizar tipo ENUM con nuevos valores
"""

import mysql.connector
from app.database.conect_db import ConectDB

def migrate_pagos():
    print("Iniciando migración de la tabla PAGOS...")
    
    cnx = ConectDB.get_connect()
    if cnx is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return False
    
    try:
        cursor = cnx.cursor()
        
        # 1. Agregar columna profesor_id
        print("\n1. Agregando columna profesor_id...")
        try:
            cursor.execute("""
                ALTER TABLE PAGOS 
                ADD COLUMN profesor_id INT DEFAULT NULL AFTER alumno_id
            """)
            print("✓ Columna profesor_id agregada")
        except mysql.connector.Error as err:
            if err.errno == 1060:  # Duplicate column name
                print("⚠ La columna profesor_id ya existe")
            else:
                raise
        
        # 2. Agregar foreign key
        print("\n2. Agregando foreign key para profesor_id...")
        try:
            cursor.execute("""
                ALTER TABLE PAGOS 
                ADD CONSTRAINT fk_pagos_profesor 
                FOREIGN KEY (profesor_id) REFERENCES PROFESORES(id) ON DELETE SET NULL
            """)
            print("✓ Foreign key agregada")
        except mysql.connector.Error as err:
            if err.errno == 1061:  # Duplicate key name
                print("⚠ La foreign key ya existe")
            elif err.errno == 1005:  # Can't create table
                print("⚠ No se pudo crear la foreign key (puede que ya exista)")
            elif err.errno == 1826:  # Duplicate foreign key constraint name
                print("⚠ La foreign key ya existe")
            else:
                print(f"⚠ Error al crear foreign key: {err}")
        
        # 3. Actualizar valores existentes
        print("\n3. Actualizando valores existentes de tipo...")
        try:
            # Mapear valores viejos a nuevos
            cursor.execute("""
                UPDATE PAGOS 
                SET tipo = CASE 
                    WHEN tipo = 'cuota_socio' THEN 'Cuota Social'
                    WHEN tipo = 'abono_clase' THEN 'Abono Mensual'
                    ELSE tipo
                END
            """)
            print(f"✓ {cursor.rowcount} registros actualizados")
        except mysql.connector.Error as err:
            print(f"⚠ Error al actualizar valores: {err}")
        
        cnx.commit()
        print("\n✅ Migración completada exitosamente!")
        print("\nTipos de pago actualizados:")
        print("  - Cuota Social (para socios)")
        print("  - Abono Mensual (para alumnos)")
        print("  - Abono Diario (para alumnos)")
        print("  - Clase (para clases individuales con profesor)")
        
        return True
        
    except Exception as exc:
        print(f"\n❌ Error durante la migración: {exc}")
        cnx.rollback()
        return False
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    migrate_pagos()
