-- Crear tabla PELOTITAS para registrar compra y venta
CREATE TABLE IF NOT EXISTS PELOTITAS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    tipo ENUM('compra', 'venta') NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    proveedor VARCHAR(200),
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insertar datos de ejemplo
INSERT INTO PELOTITAS (fecha, tipo, cantidad, precio_unitario, total, proveedor, observaciones) VALUES
('2024-11-01', 'compra', 100, 150.00, 15000.00, 'Deportes ABC', 'Compra inicial de stock'),
('2024-11-05', 'venta', 10, 200.00, 2000.00, NULL, 'Venta a socios'),
('2024-11-10', 'compra', 50, 145.00, 7250.00, 'Deportes XYZ', 'Reposición de stock'),
('2024-11-15', 'venta', 15, 200.00, 3000.00, NULL, 'Venta a alumnos'),
('2024-11-20', 'venta', 8, 200.00, 1600.00, NULL, 'Venta regular');
