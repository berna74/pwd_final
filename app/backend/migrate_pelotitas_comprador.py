#!/usr/bin/env python3
"""
Script para agregar campos de comprador a la tabla PELOTITAS
"""

import mysql.connector
from app.database.conect_db import ConectDB

def migrate_pelotitas_comprador():
    print("Iniciando migración de PELOTITAS - Agregar comprador...")
    
    cnx = ConectDB.get_connect()
    if cnx is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return False
    
    try:
        cursor = cnx.cursor()
        
        # 1. Agregar columna comprador_tipo
        print("\n1. Agregando columna comprador_tipo...")
        try:
            cursor.execute("""
                ALTER TABLE PELOTITAS 
                ADD COLUMN comprador_tipo ENUM('socio', 'alumno', 'otro') DEFAULT NULL AFTER proveedor
            """)
            print("✓ Columna comprador_tipo agregada")
        except mysql.connector.Error as err:
            if err.errno == 1060:  # Duplicate column name
                print("⚠ La columna comprador_tipo ya existe")
            else:
                raise
        
        # 2. Agregar columna comprador_id
        print("\n2. Agregando columna comprador_id...")
        try:
            cursor.execute("""
                ALTER TABLE PELOTITAS 
                ADD COLUMN comprador_id INT DEFAULT NULL AFTER comprador_tipo
            """)
            print("✓ Columna comprador_id agregada")
        except mysql.connector.Error as err:
            if err.errno == 1060:
                print("⚠ La columna comprador_id ya existe")
            else:
                raise
        
        # 3. Agregar columna comprador_nombre
        print("\n3. Agregando columna comprador_nombre...")
        try:
            cursor.execute("""
                ALTER TABLE PELOTITAS 
                ADD COLUMN comprador_nombre VARCHAR(200) DEFAULT NULL AFTER comprador_id
            """)
            print("✓ Columna comprador_nombre agregada")
        except mysql.connector.Error as err:
            if err.errno == 1060:
                print("⚠ La columna comprador_nombre ya existe")
            else:
                raise
        
        cnx.commit()
        print("\n✅ Migración completada exitosamente!")
        print("\nCampos agregados:")
        print("  - comprador_tipo: Tipo de comprador (socio, alumno, otro)")
        print("  - comprador_id: ID del socio o alumno (NULL para 'otro')")
        print("  - comprador_nombre: Nombre del comprador")
        
        return True
        
    except Exception as exc:
        print(f"\n❌ Error durante la migración: {exc}")
        cnx.rollback()
        return False
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    migrate_pelotitas_comprador()
