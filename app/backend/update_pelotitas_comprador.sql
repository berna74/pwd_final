-- Agregar campos de comprador a la tabla PELOTITAS

ALTER TABLE PELOTITAS 
ADD COLUMN comprador_tipo ENUM('socio', 'alumno', 'otro') DEFAULT NULL AFTER proveedor,
ADD COLUMN comprador_id INT DEFAULT NULL AFTER comprador_tipo,
ADD COLUMN comprador_nombre VARCHAR(200) DEFAULT NULL AFTER comprador_id;

-- No agregamos FK porque 'otro' no tiene ID relacionado
-- Para 'socio' y 'alumno' validaremos en la aplicación

-- Comentarios:
-- comprador_tipo: Tipo de comprador (socio, alumno, otro)
-- comprador_id: ID del socio o alumno (NULL si es 'otro')
-- comprador_nombre: Nombre del comprador (para tipo 'otro' o cache del nombre)
