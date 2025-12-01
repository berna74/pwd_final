-- Modificar la tabla PAGOS para agregar profesor_id y actualizar tipo
-- Cambiar los tipos de pago según los nuevos requerimientos

ALTER TABLE PAGOS 
ADD COLUMN profesor_id INT DEFAULT NULL AFTER alumno_id,
ADD CONSTRAINT fk_pagos_profesor FOREIGN KEY (profesor_id) REFERENCES PROFESORES(id) ON DELETE SET NULL;

-- Actualizar el tipo de dato si es necesario
ALTER TABLE PAGOS 
MODIFY COLUMN tipo ENUM('Cuota Social', 'Abono Mensual', 'Abono Diario', 'Clase') NOT NULL;

-- Comentarios sobre el uso:
-- Cuota Social: Para socios del club (requiere socio_id)
-- Abono Mensual: Para alumnos con abono mensual (requiere alumno_id)
-- Abono Diario: Para alumnos con pago por día (requiere alumno_id)
-- Clase: Para pago de clase individual (requiere alumno_id y profesor_id)
