# Informe de Síntesis - Sistema SiPePa
## Sistema de Administración de Pelota a Paleta del Club Sol de Mayo

---

## 1. Descripción General

**SiPePa** es un sistema integral de gestión administrativa desarrollado específicamente para el Club Sol de Mayo, diseñado para optimizar la administración de actividades deportivas, gestión de miembros, control financiero y manejo de inventario relacionado con la disciplina de pelota a paleta.

### Tecnologías Utilizadas

**Backend:**
- Python 3 con Flask Framework
- MySQL Database
- Arquitectura RESTful API
- Estructura modular por entidades

**Frontend:**
- Vue 3 con Composition API
- TypeScript para tipado estático
- Vite como build tool
- Pinia para gestión de estado
- Axios para comunicación HTTP

---

## 2. Módulos Funcionales

### 2.1 Gestión de Socios

**Descripción:** Administración completa de la base de socios del club.

**Funcionalidades:**
- Registro de nuevos socios con datos personales completos
- Actualización de información de socios existentes
- Consulta y visualización de datos de socios
- Control de estado activo/inactivo
- Eliminación lógica de registros

**Datos Gestionados:**
- Nombre y apellido
- DNI (documento de identidad)
- Teléfono de contacto
- Email
- Domicilio
- Estado (activo/inactivo)

**Componentes:**
- `SociosList.vue`: Listado general con búsqueda y filtros
- `SociosCreate.vue`: Formulario de alta de nuevos socios
- `SociosUpdate.vue`: Edición de datos existentes
- `SociosShow.vue`: Visualización detallada de información

---

### 2.2 Gestión de Alumnos

**Descripción:** Control de alumnos que toman clases en el club, con asignación de profesores.

**Funcionalidades:**
- Registro de alumnos con datos personales
- Asignación obligatoria de profesor responsable
- Actualización de información y cambio de profesor
- Consulta de alumnos por profesor
- Control de estado activo/inactivo

**Datos Gestionados:**
- Nombre y apellido
- DNI
- Teléfono
- Email
- Domicilio
- Profesor asignado (relación con módulo Profesores)
- Estado (activo/inactivo)

**Componentes:**
- `AlumnosList.vue`: Listado con filtros por profesor
- `AlumnosCreate.vue`: Formulario de alta con selector de profesor
- `AlumnosUpdate.vue`: Edición de datos y reasignación de profesor
- `AlumnosShow.vue`: Visualización detallada

**Relaciones:**
- Cada alumno está vinculado a un profesor
- Los alumnos pueden realizar pagos por clases
- Los alumnos pueden comprar pelotitas

---

### 2.3 Gestión de Profesores

**Descripción:** Administración del cuerpo docente del club.

**Funcionalidades:**
- Registro de profesores con datos personales
- Actualización de información
- Consulta de profesores disponibles
- Control de estado activo/inactivo

**Datos Gestionados:**
- Nombre y apellido
- DNI
- Teléfono
- Email
- Domicilio
- Estado (activo/inactivo)

**Componentes:**
- `ProfesoresList.vue`: Listado completo de profesores
- `ProfesoresCreate.vue`: Alta de nuevos profesores
- `ProfesoresUpdate.vue`: Edición de datos
- `ProfesoresShow.vue`: Visualización detallada

**Relaciones:**
- Cada profesor puede tener múltiples alumnos asignados
- Los profesores están vinculados a pagos tipo "Clase"

---

### 2.4 Gestión de Turnos

**Descripción:** Administración de turnos de uso de canchas del club.

**Funcionalidades:**
- Creación de turnos con fecha y hora
- Asignación de turnos a socios
- Control de disponibilidad de canchas
- Modificación y cancelación de turnos

**Datos Gestionados:**
- Fecha del turno
- Hora de inicio
- Cancha asignada
- Socio responsable (relación con módulo Socios)
- Estado del turno

**Componentes:**
- `TurnosList.vue`: Listado de turnos
- `TurnosCreate.vue`: Reserva de nuevos turnos
- `TurnosUpdate.vue`: Modificación de turnos
- `TurnosShow.vue`: Detalle de turnos

---

### 2.5 Gestión de Categorías

**Descripción:** Clasificación de socios y alumnos según nivel de juego.

**Funcionalidades:**
- Creación de categorías de juego
- Actualización de nombres y descripciones
- Consulta de categorías disponibles
- Eliminación de categorías sin uso

**Datos Gestionados:**
- Nombre de la categoría
- Descripción
- Estado (activo/inactivo)

**Componentes:**
- `CategoriasList.vue`: Listado de categorías
- `CategoriasCreate.vue`: Alta de nuevas categorías
- `CategoriasUpdate.vue`: Edición de categorías
- `CategoriasShow.vue`: Visualización detallada

---

### 2.6 Gestión de Pagos

**Descripción:** Control financiero completo de todos los ingresos del club.

**Funcionalidades:**
- Registro de pagos según tipo de concepto
- Identificación del pagador (socio o alumno)
- Registro de profesor en pagos por clases
- Selección de método de pago
- Registro de fecha y monto
- Consultas y reportes de pagos

**Tipos de Pagos:**
1. **Cuota Social**: Pago mensual de socios
2. **Abono Mensual**: Paquete mensual de clases
3. **Abono Diario**: Pago por clase individual
4. **Clase**: Pago por clase con profesor específico

**Métodos de Pago:**
- Efectivo
- Transferencia bancaria

**Datos Gestionados:**
- Tipo de pago (ENUM)
- Monto
- Fecha de pago
- Método de pago (ENUM)
- Pagador: Socio o Alumno (relación polimórfica)
- Profesor (solo para tipo "Clase")
- Observaciones

**Componentes:**
- `PagosList.vue`: Listado completo con filtros por tipo
- `PagosCreate.vue`: Formulario adaptativo según tipo de pago
- `PagosUpdate.vue`: Edición de pagos existentes
- `PagosShow.vue`: Visualización detallada con toda la información

**Características Especiales:**
- Formulario dinámico que muestra selector de profesor solo para tipo "Clase"
- Validación de campos según tipo de pago seleccionado
- Etiquetas contextuales: "Pagado por (Socio)" o "Pagado por (Alumno)"
- Cálculos automáticos y reportes por período

**Relaciones:**
- Vinculado a Socios (pagador)
- Vinculado a Alumnos (pagador)
- Vinculado a Profesores (solo en tipo "Clase")

---

### 2.7 Gestión de Pelotitas (Inventario)

**Descripción:** Control completo de inventario de pelotitas, incluyendo compras a proveedores y ventas a socios/alumnos.

**Funcionalidades:**
- Registro de compras a proveedores
- Registro de ventas a socios, alumnos u otros
- Control de stock disponible
- Cálculo de ganancias/pérdidas
- Consulta de movimientos de inventario

**Tipos de Transacciones:**
1. **Compra**: Adquisición de pelotitas a proveedores
2. **Venta**: Venta de pelotitas a clientes del club

**Tipos de Compradores:**
- **Socio**: Miembro del club
- **Alumno**: Estudiante de clases
- **Otro**: Comprador externo (nombre manual)

**Datos Gestionados:**
- Tipo de movimiento (compra/venta)
- Cantidad de pelotitas
- Precio unitario
- Precio total (calculado)
- Fecha de transacción
- Proveedor (en compras)
- Comprador tipo (socio/alumno/otro)
- Comprador ID (relación con Socios o Alumnos)
- Comprador nombre (nombre completo o texto libre)

**Componentes:**
- `PelotitasList.vue`: Listado con columnas separadas para proveedor y comprador
- `PelotitasCreate.vue`: Formulario adaptativo según tipo de transacción
- `PelotitasUpdate.vue`: Edición de movimientos
- `PelotitasShow.vue`: Visualización detallada

**Características Especiales:**
- Formulario inteligente que cambia campos según tipo de transacción
- Selector dinámico de comprador con tres opciones
- Carga automática de listas de socios y alumnos
- Campo manual para compradores externos
- Cálculo automático de precios totales
- Columnas separadas en listado para claridad

**Relaciones:**
- Vinculado a tabla PROVEEDORES (solo en compras)
- Vinculado a SOCIOS (en ventas a socios)
- Vinculado a ALUMNOS (en ventas a alumnos)

---

## 3. Características Técnicas

### 3.1 Arquitectura Backend

**Estructura Modular:**
```
app/modules/
├── socios/
│   ├── socio_model.py (lógica de negocio)
│   ├── socio_controller.py (controladores API)
│   └── socio_routes.py (definición de rutas)
├── alumnos/
├── profesores/
├── turnos/
├── categorias/
├── pagos/
└── pelotitas/
```

**Características:**
- Patrón MVC (Modelo-Vista-Controlador)
- Separación de responsabilidades
- Reutilización de código
- Mantenibilidad y escalabilidad

**Conexión a Base de Datos:**
- Clase `ConectDB` para gestión de conexiones
- Manejo de transacciones
- Prevención de SQL Injection mediante parámetros
- Gestión de errores con rollback automático

### 3.2 Arquitectura Frontend

**Estructura de Componentes:**
```
src/
├── components/
│   ├── socios/
│   ├── alumnos/
│   ├── profesores/
│   ├── turnos/
│   ├── categorias/
│   ├── pagos/
│   └── pelotitas/
├── views/
├── stores/ (Pinia)
├── services/ (API)
├── interfaces/ (TypeScript)
└── router/
```

**Características:**
- Componentes reutilizables
- State management centralizado con Pinia
- Tipado estático con TypeScript
- Routing declarativo con Vue Router
- Peticiones HTTP centralizadas con Axios

### 3.3 Base de Datos

**Tablas Principales:**

1. **SOCIOS**: Datos de socios del club
2. **ALUMNOS**: Información de alumnos con profesor asignado
3. **PROFESORES**: Datos del cuerpo docente
4. **TURNOS**: Reservas de canchas
5. **CATEGORIAS**: Clasificación por nivel de juego
6. **PAGOS**: Registro de todos los ingresos financieros
7. **PELOTITAS**: Inventario y movimientos de pelotitas
8. **PROVEEDORES**: Proveedores de pelotitas

**Características:**
- Claves primarias auto-incrementales
- Claves foráneas para integridad referencial
- Campos ENUM para valores predefinidos
- Timestamps de creación y actualización
- Índices para optimización de consultas

---

## 4. Funcionalidades Transversales

### 4.1 Sistema CRUD Completo

Cada módulo implementa las operaciones fundamentales:
- **Create**: Alta de nuevos registros
- **Read**: Consulta y visualización de datos
- **Update**: Actualización de información existente
- **Delete**: Eliminación (física o lógica)

### 4.2 Interfaz de Usuario

**Características:**
- Diseño responsive adaptable a diferentes dispositivos
- Modales para formularios de creación y edición
- Tablas interactivas con ordenamiento
- Búsqueda y filtrado en tiempo real
- Validación de formularios
- Mensajes de confirmación y error
- Iconografía intuitiva con Iconify

### 4.3 Validaciones

**Backend:**
- Validación de tipos de datos
- Validación de campos obligatorios
- Validación de integridad referencial
- Manejo de errores con mensajes descriptivos

**Frontend:**
- Validación en tiempo real
- Prevención de envío de formularios inválidos
- Mensajes de error contextuales
- Validaciones específicas por tipo de dato

### 4.4 Seguridad

- Prevención de SQL Injection
- Sanitización de inputs
- Manejo seguro de conexiones a base de datos
- Control de errores sin exposición de información sensible

---

## 5. Flujos de Trabajo Principales

### 5.1 Flujo de Registro de Socio
1. Administrador accede a módulo Socios
2. Clic en "Nuevo Socio"
3. Completa formulario con datos personales
4. Validación de campos
5. Confirmación y alta en base de datos
6. Socio disponible para reservar turnos y realizar pagos

### 5.2 Flujo de Registro de Alumno
1. Administrador accede a módulo Alumnos
2. Clic en "Nuevo Alumno"
3. Completa datos personales
4. Selecciona profesor responsable (obligatorio)
5. Confirmación y alta
6. Alumno vinculado a profesor para gestión de clases

### 5.3 Flujo de Registro de Pago
1. Administrador accede a módulo Pagos
2. Clic en "Nuevo Pago"
3. Selecciona tipo de pago (Cuota Social, Abono, Clase)
4. Sistema adapta formulario según tipo seleccionado
5. Selecciona pagador (socio o alumno según corresponda)
6. Si es tipo "Clase", selecciona profesor
7. Ingresa monto y método de pago
8. Confirmación y registro
9. Actualización de estado financiero

### 5.4 Flujo de Venta de Pelotitas
1. Administrador accede a módulo Pelotitas
2. Clic en "Nueva Venta"
3. Selecciona tipo "Venta"
4. Selecciona tipo de comprador (Socio/Alumno/Otro)
5. Sistema carga lista correspondiente o habilita campo manual
6. Ingresa cantidad y precio
7. Sistema calcula total automáticamente
8. Confirmación y registro
9. Actualización de inventario

### 5.5 Flujo de Compra de Pelotitas
1. Administrador accede a módulo Pelotitas
2. Clic en "Nueva Compra"
3. Selecciona tipo "Compra"
4. Selecciona proveedor
5. Ingresa cantidad y precio de compra
6. Confirmación y registro
7. Incremento de stock disponible

---

## 6. Reportes y Consultas

El sistema permite realizar diversas consultas:

- **Pagos por período**: Filtrado por fechas
- **Pagos por tipo**: Cuotas sociales, abonos, clases
- **Pagos por socio/alumno**: Historial individual
- **Movimientos de pelotitas**: Compras y ventas
- **Estado de inventario**: Stock actual
- **Alumnos por profesor**: Agrupación de estudiantes
- **Turnos por socio**: Historial de reservas
- **Estado de cuenta por socio**: Pagos realizados

---

## 7. Ventajas del Sistema

### 7.1 Para la Administración
- **Centralización**: Toda la información en un solo lugar
- **Automatización**: Reducción de tareas manuales
- **Trazabilidad**: Registro completo de todas las operaciones
- **Rapidez**: Consultas instantáneas de información
- **Control**: Seguimiento preciso de finanzas e inventario

### 7.2 Para los Usuarios
- **Interfaz intuitiva**: Fácil de usar sin capacitación extensa
- **Rapidez de operación**: Formularios optimizados
- **Información clara**: Visualización organizada de datos
- **Flexibilidad**: Adaptable a diferentes necesidades

### 7.3 Técnicas
- **Escalabilidad**: Arquitectura modular permite crecimiento
- **Mantenibilidad**: Código organizado y documentado
- **Extensibilidad**: Fácil agregar nuevos módulos
- **Performance**: Consultas optimizadas con índices
- **Confiabilidad**: Manejo robusto de errores

---

## 8. Tecnologías y Herramientas

### Backend
- **Python 3**: Lenguaje de programación principal
- **Flask**: Framework web minimalista y flexible
- **MySQL**: Sistema de gestión de base de datos relacional
- **mysql-connector-python**: Conector para Python-MySQL

### Frontend
- **Vue 3**: Framework JavaScript progresivo
- **TypeScript**: Superset de JavaScript con tipado estático
- **Vite**: Build tool de nueva generación
- **Pinia**: Librería de gestión de estado para Vue
- **Vue Router**: Routing oficial para Vue.js
- **Axios**: Cliente HTTP para peticiones
- **Iconify**: Biblioteca de iconos unificada

### Desarrollo
- **VS Code**: Editor de código
- **Git**: Control de versiones
- **Python venv**: Entornos virtuales
- **npm**: Gestor de paquetes para Node.js

---

## 9. Casos de Uso Principales

### CU-01: Gestionar Socios
**Actor:** Administrador  
**Descripción:** Permite realizar altas, bajas, modificaciones y consultas de socios del club.

### CU-02: Gestionar Alumnos
**Actor:** Administrador  
**Descripción:** Permite administrar alumnos con asignación de profesores responsables.

### CU-03: Gestionar Profesores
**Actor:** Administrador  
**Descripción:** Permite administrar el cuerpo docente del club.

### CU-04: Gestionar Turnos
**Actor:** Administrador  
**Descripción:** Permite gestionar reservas de canchas para socios.

### CU-05: Gestionar Categorías
**Actor:** Administrador  
**Descripción:** Permite administrar categorías de juego según nivel.

### CU-06: Registrar Pago
**Actor:** Administrador  
**Descripción:** Permite registrar diferentes tipos de pagos (cuotas, abonos, clases) identificando al pagador y, en caso de clases, al profesor.

### CU-07: Consultar Pagos
**Actor:** Administrador  
**Descripción:** Permite consultar historial de pagos con filtros por tipo, fecha, socio o alumno.

### CU-08: Registrar Compra de Pelotitas
**Actor:** Administrador  
**Descripción:** Permite registrar compras de pelotitas a proveedores actualizando inventario.

### CU-09: Registrar Venta de Pelotitas
**Actor:** Administrador  
**Descripción:** Permite registrar ventas de pelotitas a socios, alumnos u otros compradores.

### CU-10: Consultar Inventario
**Actor:** Administrador  
**Descripción:** Permite consultar stock actual y movimientos de pelotitas.

---

## 10. Mejoras Futuras Potenciales

### Funcionalidades
- Sistema de autenticación y autorización de usuarios
- Diferentes roles (administrador, recepcionista, profesor)
- Dashboard con estadísticas y gráficos
- Generación de reportes en PDF
- Sistema de notificaciones por email o SMS
- Recordatorios de vencimiento de cuotas
- Reserva de turnos online para socios
- App móvil complementaria

### Técnicas
- Implementación de caché para mejorar performance
- Sistema de backups automáticos
- Logging avanzado de operaciones
- Testing automatizado (unit tests, integration tests)
- CI/CD para despliegue automático
- Migración a arquitectura de microservicios

---

## 11. Conclusiones

El **Sistema SiPePa** representa una solución integral y moderna para la gestión administrativa del Club Sol de Mayo. Su arquitectura modular, basada en tecnologías actuales y probadas, garantiza:

- **Eficiencia operativa**: Automatización de procesos administrativos
- **Control financiero**: Seguimiento preciso de ingresos
- **Gestión de inventario**: Control de compras y ventas de pelotitas
- **Trazabilidad**: Registro completo de todas las operaciones
- **Escalabilidad**: Capacidad de crecimiento y adaptación

El sistema está completamente funcional y en condiciones de ser desplegado en producción, con todas las funcionalidades críticas implementadas y probadas. Su diseño permite futuras extensiones sin necesidad de modificar la arquitectura base.

---

**Fecha del Informe:** 28 de noviembre de 2025  
**Versión del Sistema:** 1.0  
**Estado:** Producción Ready
