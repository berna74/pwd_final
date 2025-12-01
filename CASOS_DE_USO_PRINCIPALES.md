# Análisis UML - Casos de Uso Principales del Sistema SiPePa
## Sistema de Administración de Pelota a Paleta del Club Sol de Mayo

---

## Introducción al Análisis

Como analista de sistemas experimentado, he identificado los **3 casos de uso más críticos** del sistema SiPePa basándome en los siguientes criterios de análisis:

1. **Impacto en el negocio**: Funcionalidad esencial para la operación del club
2. **Complejidad funcional**: Cantidad de actores, precondiciones y flujos alternos
3. **Integridad de datos**: Relaciones con múltiples entidades del modelo de dominio
4. **Frecuencia de uso**: Operaciones que se realizan diariamente
5. **Valor para el usuario**: ROI (retorno de inversión) para la gestión del club

Tras analizar todos los módulos del sistema, los casos de uso más importantes son:

1. **CU-01: Registrar Pago** (Criticidad: ALTA)
2. **CU-02: Reservar Turno** (Criticidad: ALTA)
3. **CU-03: Gestionar Inventario de Pelotitas** (Criticidad: MEDIA-ALTA)

---

# CASO DE USO 01: REGISTRAR PAGO

## 1. Información General

| Elemento | Descripción |
|----------|-------------|
| **ID** | CU-01 |
| **Nombre** | Registrar Pago |
| **Actor Principal** | Administrador |
| **Actores Secundarios** | Socio, Alumno, Profesor (datos) |
| **Tipo** | Primario, Esencial |
| **Complejidad** | Alta |
| **Prioridad** | Crítica |
| **Estado** | Implementado |
| **Versión** | 1.0 |

---

## 2. Descripción

Este caso de uso permite al administrador del club registrar todos los ingresos económicos de la institución, diferenciando entre cuatro tipos de pagos: Cuota Social, Abono Mensual, Abono Diario y Clase. El sistema adapta dinámicamente el formulario según el tipo seleccionado y valida la integridad referencial con las entidades Socios, Alumnos y Profesores.

**Importancia del Negocio:**
- Control financiero centralizado del club
- Trazabilidad completa de ingresos
- Registro contable para auditorías
- Base para reportes de rentabilidad
- Liquidación de honorarios a profesores

---

## 3. Actores

### Actor Principal
- **Administrador**: Personal administrativo del club autorizado para registrar transacciones financieras

### Actores Secundarios
- **Socio**: Persona que realiza el pago (referenciado en BD)
- **Alumno**: Estudiante que realiza el pago (referenciado en BD)
- **Profesor**: Docente que dictó la clase (solo en tipo "Clase")

---

## 4. Precondiciones

1. El administrador debe estar autenticado en el sistema
2. Debe existir al menos un Socio o Alumno registrado en el sistema
3. Para pagos tipo "Clase", debe existir al menos un Profesor activo
4. La base de datos debe estar accesible y operativa
5. El sistema frontend debe tener conexión con el backend (API REST)

---

## 5. Postcondiciones

### Postcondiciones de Éxito
1. El pago queda registrado en la tabla PAGOS de la base de datos
2. Se asigna un ID único auto-incremental al registro
3. Se registra timestamp de creación (created_at)
4. El monto queda vinculado al pagador (Socio o Alumno)
5. Si es tipo "Clase", queda vinculado al Profesor correspondiente
6. El administrador recibe confirmación visual del registro exitoso
7. El pago aparece inmediatamente en el listado de pagos

### Postcondiciones de Fracaso
1. El registro no se guarda en la base de datos
2. Se mantiene la integridad referencial (no se crean datos huérfanos)
3. Se muestra mensaje de error descriptivo al administrador
4. El formulario conserva los datos ingresados para reintento

---

## 6. Flujo Normal (Escenario Principal)

### Trigger/Disparador
El administrador necesita registrar un ingreso de dinero al club.

### Flujo de Eventos

| # | Actor | Sistema |
|---|-------|---------|
| 1 | El administrador accede al módulo "Pagos" desde el menú principal | |
| 2 | | El sistema carga la vista PagosView.vue y muestra el componente PagosList con todos los pagos existentes |
| 3 | El administrador hace clic en el botón "Nuevo Pago" | |
| 4 | | El sistema abre el modal PagosCreate.vue con el formulario vacío |
| 5 | | El sistema carga las listas de Socios, Alumnos y Profesores desde el store (Pinia) mediante llamadas al backend |
| 6 | El administrador selecciona el **Tipo de Pago** del dropdown | |
| 7 | | El sistema adapta dinámicamente el formulario según el tipo:<br>- "Cuota Social": habilita selector de Socio, campos mes/año<br>- "Abono Mensual": habilita selector de Socio o Alumno, campos mes/año<br>- "Abono Diario": habilita selector de Socio o Alumno<br>- "Clase": habilita selector de Alumno y Profesor (obligatorio) |
| 8 | El administrador completa los campos requeridos:<br>- Pagador (Socio o Alumno según corresponda)<br>- Monto<br>- Fecha de pago<br>- Método de pago (Efectivo/Transferencia)<br>- Profesor (solo si tipo = "Clase")<br>- Mes y Año (si corresponde)<br>- Observaciones (opcional) | |
| 9 | | El sistema valida en tiempo real cada campo según reglas de negocio |
| 10 | El administrador hace clic en "Guardar" | |
| 11 | | El sistema valida todos los campos obligatorios |
| 12 | | El sistema construye el objeto JSON con la estructura PagoModel |
| 13 | | El sistema envía petición POST a `/api/pagos` con los datos del pago |
| 14 | | El backend recibe la petición en `pago_controller.create_pago()` |
| 15 | | El backend valida la integridad referencial (existencia de Socio/Alumno/Profesor) |
| 16 | | El backend ejecuta INSERT en la tabla PAGOS con todos los campos |
| 17 | | La base de datos MySQL asigna ID auto-incremental y registra timestamp |
| 18 | | El backend retorna código HTTP 201 con el objeto pago creado (incluyendo nombres de las entidades relacionadas mediante JOINs) |
| 19 | | El frontend actualiza el store de Pinia con el nuevo pago |
| 20 | | El sistema cierra el modal y muestra mensaje de éxito |
| 21 | | El sistema refresca automáticamente la lista de pagos mostrando el nuevo registro |
| 22 | El administrador visualiza el pago registrado en la tabla | |

---

## 7. Flujos Alternos

### FA-01: Cancelar Registro
**Punto de Extensión:** Paso 10 del flujo normal

| # | Descripción |
|---|-------------|
| FA-01.1 | El administrador hace clic en "Cancelar" o presiona la tecla ESC |
| FA-01.2 | El sistema cierra el modal sin guardar cambios |
| FA-01.3 | El sistema descarta todos los datos ingresados |
| FA-01.4 | El caso de uso termina sin modificar la base de datos |

### FA-02: Error de Validación de Campos
**Punto de Extensión:** Paso 11 del flujo normal

| # | Descripción |
|---|-------------|
| FA-02.1 | El sistema detecta que faltan campos obligatorios o tienen formato inválido |
| FA-02.2 | El sistema muestra mensajes de error específicos junto a cada campo problemático |
| FA-02.3 | El sistema impide el envío del formulario (botón Guardar permanece habilitado pero sin efecto) |
| FA-02.4 | El administrador corrige los errores |
| FA-02.5 | El flujo retorna al paso 9 del flujo normal |

### FA-03: Error de Conexión con Backend
**Punto de Extensión:** Paso 13 del flujo normal

| # | Descripción |
|---|-------------|
| FA-03.1 | El sistema intenta enviar la petición POST pero falla la conexión HTTP |
| FA-03.2 | El frontend (Axios) genera una excepción de red |
| FA-03.3 | El sistema captura la excepción y muestra mensaje: "Error de conexión. Verifique su conexión a internet" |
| FA-03.4 | El modal permanece abierto conservando todos los datos ingresados |
| FA-03.5 | El administrador puede reintentar el guardado (retorna a paso 10) o cancelar |

### FA-04: Error de Integridad Referencial
**Punto de Extensión:** Paso 15 del flujo normal

| # | Descripción |
|---|-------------|
| FA-04.1 | El backend detecta que el socio_id, alumno_id o profesor_id no existen en sus tablas respectivas |
| FA-04.2 | El backend ejecuta rollback de la transacción |
| FA-04.3 | El backend retorna código HTTP 400 con mensaje: "El socio/alumno/profesor seleccionado no existe" |
| FA-04.4 | El frontend muestra el mensaje de error en un alert |
| FA-04.5 | El administrador debe verificar los datos o refrescar las listas de selección |
| FA-04.6 | Puede reintentar (retorna a paso 8) o cancelar |

### FA-05: Error de Base de Datos
**Punto de Extensión:** Paso 16 del flujo normal

| # | Descripción |
|---|-------------|
| FA-05.1 | La ejecución del INSERT falla por error de MySQL (constraint violation, conexión perdida, etc.) |
| FA-05.2 | El backend captura la excepción MySQLError |
| FA-05.3 | El backend ejecuta rollback automático |
| FA-05.4 | El backend retorna código HTTP 500 con mensaje genérico: "Error al guardar el pago" |
| FA-05.5 | El sistema frontend muestra el error y sugiere reintentar |
| FA-05.6 | El modal permanece abierto con los datos |

### FA-06: Registro de Pago por Clase sin Profesor
**Punto de Extensión:** Paso 8 del flujo normal

| # | Descripción |
|---|-------------|
| FA-06.1 | El administrador selecciona tipo "Clase" pero no selecciona profesor |
| FA-06.2 | Al intentar guardar, el sistema valida y detecta que profesor_id es NULL |
| FA-06.3 | El sistema muestra mensaje: "Debe seleccionar un profesor para pagos tipo Clase" |
| FA-06.4 | El sistema resalta el campo Profesor en rojo |
| FA-06.5 | El administrador debe seleccionar un profesor |
| FA-06.6 | Retorna al paso 8 del flujo normal |

---

## 8. Flujos de Excepción

### FE-01: Sistema Fuera de Línea
**Descripción:** El backend está completamente inaccesible

| # | Descripción |
|---|-------------|
| FE-01.1 | El usuario intenta acceder al módulo Pagos |
| FE-01.2 | El sistema intenta cargar las listas de Socios/Alumnos/Profesores |
| FE-01.3 | Todas las peticiones HTTP fallan con timeout |
| FE-01.4 | El sistema muestra mensaje: "Sistema temporalmente fuera de servicio. Intente más tarde" |
| FE-01.5 | El caso de uso termina sin poder registrar el pago |

---

## 9. Reglas de Negocio

| ID | Regla | Descripción |
|----|-------|-------------|
| RN-01 | Tipificación de Pagos | Los pagos deben clasificarse obligatoriamente en uno de los 4 tipos definidos: Cuota Social, Abono Mensual, Abono Diario o Clase |
| RN-02 | Pagador Único | Un pago debe tener exactamente un pagador: Socio O Alumno, nunca ambos simultáneamente |
| RN-03 | Profesor en Clases | Los pagos tipo "Clase" DEBEN tener asociado un profesor_id válido |
| RN-04 | Métodos de Pago | Solo se aceptan dos métodos de pago: Efectivo y Transferencia (eliminados Cheque y Tarjeta de Crédito) |
| RN-05 | Monto Positivo | El monto del pago debe ser un número positivo mayor a cero |
| RN-06 | Fecha Válida | La fecha de pago no puede ser posterior a la fecha actual del sistema |
| RN-07 | Integridad Referencial | Todos los IDs referenciados (socio_id, alumno_id, profesor_id) deben existir en sus tablas respectivas |
| RN-08 | Mes y Año para Cuotas | Los pagos tipo "Cuota Social" y "Abono Mensual" deben registrar mes (1-12) y año (YYYY) |

---

## 10. Requisitos Especiales

### Requisitos No Funcionales

**RNF-01: Performance**
- El tiempo de respuesta del registro no debe superar los 2 segundos en condiciones normales
- La carga de las listas de selección (Socios, Alumnos, Profesores) debe completarse en menos de 1 segundo

**RNF-02: Usabilidad**
- El formulario debe adaptarse automáticamente según el tipo de pago seleccionado sin recargar la página
- Los campos deben validarse en tiempo real mientras el usuario escribe
- El sistema debe proporcionar feedback visual claro (colores, mensajes) sobre el estado de validación

**RNF-03: Confiabilidad**
- El sistema debe garantizar la atomicidad de las transacciones (todo o nada)
- No se deben crear registros huérfanos en caso de error
- El sistema debe recuperarse automáticamente de errores transitorios de conexión

**RNF-04: Seguridad**
- Solo usuarios autenticados con rol "Administrador" pueden registrar pagos
- Los datos deben transmitirse por HTTPS en producción
- Se debe prevenir SQL Injection mediante prepared statements

**RNF-05: Auditabilidad**
- Cada pago debe registrar timestamp de creación (created_at)
- El sistema debe mantener log de todas las transacciones financieras
- No se permite eliminación física de pagos (solo baja lógica si aplica)

---

## 11. Diagrama de Casos de Uso (Notación UML)

```
┌─────────────────────────────────────────────────────────────┐
│                   Sistema SiPePa - Pagos                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│          ┌──────────────────────────┐                       │
│          │   Registrar Pago         │                       │
│          │      (CU-01)             │                       │
│          └────────┬─────────────────┘                       │
│                   │                                         │
│                   │ <<include>>                             │
│                   │                                         │
│     ┌─────────────┴─────────────┐                          │
│     │                           │                          │
│     ▼                           ▼                          │
│  ┌─────────────────┐    ┌──────────────────┐              │
│  │ Validar Pagador │    │ Validar Profesor │              │
│  │   (UC-01.1)     │    │   (UC-01.2)      │              │
│  └─────────────────┘    └──────────────────┘              │
│                                │                           │
│                                │ <<extend>>                │
│                        [tipo = "Clase"]                    │
│                                                            │
└────────────────────────────────────────────────────────────┘

     Actor Principal              Actores Secundarios
    ┌──────────┐                 ┌────────┐ ┌────────┐ ┌──────────┐
    │ Adminis- │ ───────────────▶│ Socio  │ │ Alumno │ │ Profesor │
    │  trador  │                 │ (datos)│ │ (datos)│ │  (datos) │
    └──────────┘                 └────────┘ └────────┘ └──────────┘
```

---

## 12. Diagrama de Secuencia (Flujo Normal)

```
Administrador    Frontend         Store         Backend         BD
     │               │              │              │             │
     │───[1] Click───▶│              │              │             │
     │               │──[2] Open────▶│              │             │
     │               │    Modal      │              │             │
     │               │              │              │             │
     │               │──[3] Load────▶│              │             │
     │               │    Lists      │──[4] GET────▶│             │
     │               │              │    /socios    │──[5] SELECT▶│
     │               │              │              │◀────[6]─────│
     │               │              │◀────[7]──────│             │
     │               │◀────[8]──────│              │             │
     │               │              │              │             │
     │──[9] Fill─────▶│              │              │             │
     │    Form        │              │              │             │
     │               │              │              │             │
     │──[10] Click───▶│              │              │             │
     │    Guardar     │              │              │             │
     │               │──[11] Validate│              │             │
     │               │──[12] Build───│              │             │
     │               │    Payload    │              │             │
     │               │              │              │             │
     │               │──────[13] POST /api/pagos──▶│             │
     │               │              │              │──[14] INSERT▶│
     │               │              │              │◀────[15]────│
     │               │              │◀────[16]─────│  (ID:123)   │
     │               │◀────[17]─────│   201 OK     │             │
     │◀──[18] OK─────│              │              │             │
     │               │──[19] Refresh│              │             │
     │               │◀────[20]─────│              │             │
     │               │              │              │             │
```

---

## 13. Matriz de Trazabilidad

| Requisito Funcional | Componente Frontend | Componente Backend | Tabla BD | Regla de Negocio |
|---------------------|---------------------|-----------------------|----------|------------------|
| Seleccionar tipo de pago | PagosCreate.vue (select) | - | PAGOS.tipo | RN-01 |
| Seleccionar pagador | PagosCreate.vue (select) | - | PAGOS.socio_id / alumno_id | RN-02, RN-07 |
| Seleccionar profesor | PagosCreate.vue (select) | - | PAGOS.profesor_id | RN-03, RN-07 |
| Ingresar monto | PagosCreate.vue (input) | pago_controller.py | PAGOS.monto | RN-05 |
| Seleccionar método | PagosCreate.vue (select) | - | PAGOS.metodo_pago | RN-04 |
| Validar formulario | PagosCreate.vue (validations) | pago_controller.py | - | RN-05, RN-06, RN-08 |
| Guardar pago | - | pago_model.py create() | PAGOS (INSERT) | RN-07 |
| Cargar listas | usePagosStore (Pinia) | socio_controller, alumno_controller, profesor_controller | SOCIOS, ALUMNOS, PROFESORES | - |

---

## 14. Puntos de Extensión

Este caso de uso puede ser extendido por los siguientes casos de uso secundarios:

- **CU-07: Generar Recibo de Pago** - Impresión de comprobante tras el registro
- **CU-08: Enviar Notificación de Pago** - Email/SMS de confirmación al pagador
- **CU-09: Registrar Pago Parcial** - Permitir pagos en cuotas
- **CU-10: Aplicar Descuentos** - Sistema de promociones y descuentos

---

## 15. Notas Adicionales

### Consideraciones Técnicas
- El campo `total` no se calcula en este caso de uso (monto = total)
- Los nombres completos (socio_nombre, alumno_nombre, profesor_nombre) se obtienen mediante JOINs en el backend
- El frontend utiliza Pinia para gestión de estado reactivo
- La validación se realiza en dos capas: cliente (UX) y servidor (seguridad)

### Evolución Futura
- Implementar escaneo de QR para pagos electrónicos
- Integración con pasarelas de pago online
- Dashboard de análisis financiero en tiempo real
- Recordatorios automáticos de vencimiento de cuotas

---

# CASO DE USO 02: RESERVAR TURNO

## 1. Información General

| Elemento | Descripción |
|----------|-------------|
| **ID** | CU-02 |
| **Nombre** | Reservar Turno |
| **Actor Principal** | Administrador |
| **Actores Secundarios** | Socio (datos) |
| **Tipo** | Primario, Esencial |
| **Complejidad** | Media-Alta |
| **Prioridad** | Crítica |
| **Estado** | Implementado |
| **Versión** | 1.0 |

---

## 2. Descripción

Este caso de uso permite al administrador gestionar las reservas de canchas del club, asignando turnos a socios para fechas y horarios específicos. El sistema controla la disponibilidad de canchas, evita solapamientos de horarios y mantiene un registro completo de las reservas.

**Importancia del Negocio:**
- Optimización del uso de las instalaciones deportivas
- Control de acceso a las canchas
- Prevención de conflictos de horarios
- Maximización de ingresos por uso de instalaciones
- Experiencia del usuario (socios pueden planificar sus partidos)

---

## 3. Actores

### Actor Principal
- **Administrador**: Personal autorizado para gestionar reservas de turnos

### Actores Secundarios
- **Socio**: Miembro del club que solicita la reserva (referenciado en BD)

---

## 4. Precondiciones

1. El administrador debe estar autenticado en el sistema
2. Debe existir al menos un Socio activo registrado en el sistema
3. Deben existir canchas configuradas en el sistema
4. La fecha de reserva debe ser igual o posterior a la fecha actual
5. La base de datos debe estar accesible y operativa

---

## 5. Postcondiciones

### Postcondiciones de Éxito
1. El turno queda registrado en la tabla TURNOS
2. Se asigna ID único al turno
3. La cancha queda marcada como ocupada en el horario reservado
4. El socio queda vinculado al turno
5. El estado del turno se establece como "reservado"
6. Se registra timestamp de creación
7. El turno aparece en el listado de turnos y en el calendario

### Postcondiciones de Fracaso
1. No se crea el registro en la base de datos
2. La disponibilidad de la cancha permanece sin cambios
3. Se muestra mensaje de error al administrador
4. El formulario conserva los datos para reintento

---

## 6. Flujo Normal (Escenario Principal)

### Trigger/Disparador
Un socio solicita reservar una cancha o el administrador necesita agendar un turno.

### Flujo de Eventos

| # | Actor | Sistema |
|---|-------|---------|
| 1 | El administrador accede al módulo "Turnos" desde el menú principal | |
| 2 | | El sistema carga TurnosView.vue y muestra calendario/lista de turnos existentes |
| 3 | El administrador hace clic en "Nuevo Turno" | |
| 4 | | El sistema abre modal TurnosCreate.vue con formulario vacío |
| 5 | | El sistema carga lista de Socios activos desde el backend |
| 6 | El administrador selecciona la **Cancha** (ej: Cancha 1, Cancha 2) | |
| 7 | El administrador selecciona la **Fecha** del turno | |
| 8 | | El sistema consulta al backend los horarios disponibles para esa fecha y cancha |
| 9 | | El sistema muestra slots de horarios disponibles |
| 10 | El administrador selecciona **Hora de inicio** del turno | |
| 11 | El administrador selecciona **Hora de fin** del turno | |
| 12 | | El sistema valida que hora_fin > hora_inicio |
| 13 | | El sistema calcula la duración del turno |
| 14 | El administrador selecciona el **Socio** que reserva el turno | |
| 15 | El administrador opcionalmente agrega jugadores adicionales al turno | |
| 16 | El administrador hace clic en "Confirmar Reserva" | |
| 17 | | El sistema valida disponibilidad de la cancha en ese horario |
| 18 | | El sistema verifica que no haya solapamiento con otros turnos |
| 19 | | El sistema construye objeto TurnoModel con todos los datos |
| 20 | | El sistema envía petición POST a `/api/turnos` |
| 21 | | El backend valida integridad referencial del socio_id |
| 22 | | El backend ejecuta INSERT en tabla TURNOS |
| 23 | | MySQL asigna ID y timestamp |
| 24 | | El backend retorna código 201 con el turno creado (incluyendo nombre del socio) |
| 25 | | El frontend actualiza el store y cierra el modal |
| 26 | | El sistema muestra mensaje de confirmación |
| 27 | | El calendario/lista se actualiza mostrando el nuevo turno |
| 28 | El administrador visualiza el turno reservado | |

---

## 7. Flujos Alternos

### FA-01: Horario No Disponible
**Punto de Extensión:** Paso 17 del flujo normal

| # | Descripción |
|---|-------------|
| FA-01.1 | El sistema detecta que existe otro turno en el mismo horario y cancha |
| FA-01.2 | El sistema retorna código HTTP 409 (Conflict) con mensaje: "El horario seleccionado ya está ocupado" |
| FA-01.3 | El frontend muestra el mensaje de error |
| FA-01.4 | El sistema sugiere horarios alternativos disponibles |
| FA-01.5 | El administrador debe seleccionar otro horario o fecha |
| FA-01.6 | Retorna al paso 7 del flujo normal |

### FA-02: Solapamiento Parcial de Horarios
**Punto de Extensión:** Paso 18 del flujo normal

| # | Descripción |
|---|-------------|
| FA-02.1 | El sistema detecta que el turno se solapa parcialmente con otro turno existente |
| FA-02.2 | Ejemplo: Turno existente 14:00-16:00, nuevo turno 15:00-17:00 |
| FA-02.3 | El sistema muestra mensaje: "El horario se solapa con otro turno" |
| FA-02.4 | El sistema resalta visualmente el conflicto en el calendario |
| FA-02.5 | El administrador debe ajustar los horarios |
| FA-02.6 | Retorna al paso 10 del flujo normal |

### FA-03: Fecha Pasada
**Punto de Extensión:** Paso 7 del flujo normal

| # | Descripción |
|---|-------------|
| FA-03.1 | El administrador intenta seleccionar una fecha anterior a la fecha actual |
| FA-03.2 | El sistema bloquea la selección de fechas pasadas en el date picker |
| FA-03.3 | Si se intenta enviar, el sistema valida y muestra: "No se pueden reservar turnos en fechas pasadas" |
| FA-03.4 | El administrador debe seleccionar fecha válida (hoy o futura) |

### FA-04: Hora de Fin Menor a Hora de Inicio
**Punto de Extensión:** Paso 12 del flujo normal

| # | Descripción |
|---|-------------|
| FA-04.1 | El sistema valida y detecta que hora_fin <= hora_inicio |
| FA-04.2 | El sistema muestra mensaje: "La hora de fin debe ser posterior a la hora de inicio" |
| FA-04.3 | El sistema resalta los campos de hora en rojo |
| FA-04.4 | El administrador debe corregir los horarios |
| FA-04.5 | Retorna al paso 10 del flujo normal |

### FA-05: Socio Inactivo
**Punto de Extensión:** Paso 21 del flujo normal

| # | Descripción |
|---|-------------|
| FA-05.1 | El backend valida el socio_id y detecta que el socio está inactivo (estado = 0) |
| FA-05.2 | El backend retorna código HTTP 400 con mensaje: "El socio seleccionado está inactivo" |
| FA-05.3 | El frontend muestra el mensaje de error |
| FA-05.4 | El administrador debe seleccionar un socio activo |

---

## 8. Flujos de Excepción

### FE-01: Error al Consultar Disponibilidad
**Descripción:** Falla la consulta de horarios disponibles

| # | Descripción |
|---|-------------|
| FE-01.1 | El sistema intenta consultar horarios disponibles en el paso 8 |
| FE-01.2 | La petición al backend falla (timeout, error 500) |
| FE-01.3 | El sistema muestra mensaje: "Error al cargar horarios disponibles" |
| FE-01.4 | El sistema deshabilita los campos de hora |
| FE-01.5 | El administrador puede reintentar o cancelar la reserva |

---

## 9. Reglas de Negocio

| ID | Regla | Descripción |
|----|-------|-------------|
| RN-09 | Cancha Obligatoria | Todo turno debe estar asignado a una cancha específica |
| RN-10 | Fecha Futura | No se permiten reservas para fechas pasadas |
| RN-11 | Duración Mínima | Los turnos deben tener duración mínima de 1 hora |
| RN-12 | No Solapamiento | No puede haber dos turnos simultáneos en la misma cancha |
| RN-13 | Socio Activo | Solo socios con estado "activo" pueden reservar turnos |
| RN-14 | Horario de Apertura | Las reservas solo pueden hacerse dentro del horario de operación del club (ej: 08:00-22:00) |
| RN-15 | Un Responsable | Cada turno debe tener exactamente un socio responsable de la reserva |

---

## 10. Requisitos Especiales

**RNF-06: Sincronización**
- El sistema debe actualizar la disponibilidad en tiempo real cuando se crea o cancela un turno
- Múltiples administradores deben ver cambios sincronizados instantáneamente

**RNF-07: Visualización**
- El sistema debe proporcionar vista de calendario mensual/semanal/diaria
- Los turnos deben distinguirse visualmente por cancha y estado

---

## 11. Diagrama de Secuencia (Validación de Disponibilidad)

```
Administrador    Frontend         Backend         BD
     │               │              │             │
     │──[1] Select───▶│              │             │
     │    Fecha       │              │             │
     │               │──[2] GET─────▶│             │
     │               │   /turnos?    │             │
     │               │   fecha=X&    │──[3] SELECT▶│
     │               │   cancha=Y    │   FROM      │
     │               │              │   TURNOS    │
     │               │              │   WHERE...  │
     │               │              │◀────[4]─────│
     │               │              │  (resultados)│
     │               │◀────[5]──────│             │
     │               │   turnos[]    │             │
     │               │──[6] Calculate│             │
     │               │   Available   │             │
     │               │   Slots       │             │
     │◀──[7] Show────│              │             │
     │    Available  │              │             │
     │    Hours      │              │             │
```

---

# CASO DE USO 03: GESTIONAR INVENTARIO DE PELOTITAS

## 1. Información General

| Elemento | Descripción |
|----------|-------------|
| **ID** | CU-03 |
| **Nombre** | Gestionar Inventario de Pelotitas |
| **Actor Principal** | Administrador |
| **Actores Secundarios** | Proveedor, Socio, Alumno (datos) |
| **Tipo** | Primario, Esencial |
| **Complejidad** | Alta |
| **Prioridad** | Alta |
| **Estado** | Implementado |
| **Versión** | 1.0 |

---

## 2. Descripción

Este caso de uso permite al administrador gestionar el inventario completo de pelotitas del club, registrando tanto compras a proveedores como ventas a socios, alumnos o compradores externos. El sistema calcula automáticamente stock disponible, precios totales y márgenes de ganancia.

**Importancia del Negocio:**
- Control de inventario en tiempo real
- Gestión de compras y proveedores
- Registro de ventas y clientes
- Cálculo automático de rentabilidad
- Prevención de desabastecimiento
- Trazabilidad completa de movimientos

---

## 3. Actores

### Actor Principal
- **Administrador**: Personal autorizado para gestionar compras y ventas

### Actores Secundarios
- **Proveedor**: Empresa/persona que vende pelotitas al club
- **Socio**: Miembro del club que compra pelotitas
- **Alumno**: Estudiante que compra pelotitas
- **Comprador Externo**: Persona no registrada que compra pelotitas

---

## 4. Precondiciones

1. El administrador debe estar autenticado
2. Para registrar ventas a Socios/Alumnos, deben existir registros en esas tablas
3. Debe existir al menos un Proveedor registrado para compras
4. La base de datos debe estar accesible

---

## 5. Postcondiciones

### Postcondiciones de Éxito (Compra)
1. El movimiento de compra queda registrado en tabla PELOTITAS
2. Se incrementa el stock disponible
3. Se vincula el proveedor al movimiento
4. Se registra precio de compra y cantidad
5. Se actualiza el inventario en tiempo real

### Postcondiciones de Éxito (Venta)
1. El movimiento de venta queda registrado en tabla PELOTITAS
2. Se decrementa el stock disponible
3. Se vincula el comprador (socio/alumno/otro)
4. Se registra precio de venta y cantidad
5. Se calcula automáticamente el margen de ganancia

---

## 6. Flujo Normal - Subproceso A: Registrar Compra

### Trigger/Disparador
El club recibe un lote de pelotitas del proveedor.

### Flujo de Eventos

| # | Actor | Sistema |
|---|-------|---------|
| 1 | El administrador accede al módulo "Pelotitas" | |
| 2 | | El sistema muestra PelotitasView con lista de movimientos y resumen de stock |
| 3 | El administrador hace clic en "Nueva Operación" | |
| 4 | | El sistema abre modal PelotitasCreate.vue |
| 5 | | El sistema carga lista de Proveedores desde el backend |
| 6 | El administrador selecciona **Tipo: "Compra"** | |
| 7 | | El sistema adapta el formulario mostrando: campo Proveedor, oculta campos de Comprador |
| 8 | El administrador selecciona el **Proveedor** del dropdown | |
| 9 | El administrador ingresa la **Fecha** de la compra | |
| 10 | El administrador ingresa la **Cantidad** de pelotitas | |
| 11 | El administrador ingresa el **Precio Unitario** de compra | |
| 12 | | El sistema calcula automáticamente: total = cantidad × precio_unitario |
| 13 | | El sistema muestra el total calculado en tiempo real |
| 14 | El administrador opcionalmente agrega **Observaciones** | |
| 15 | El administrador hace clic en "Guardar" | |
| 16 | | El sistema valida todos los campos obligatorios |
| 17 | | El sistema construye objeto Pelotita con tipo="compra" |
| 18 | | El sistema envía POST a `/api/pelotitas` |
| 19 | | El backend valida integridad referencial del proveedor |
| 20 | | El backend ejecuta INSERT en tabla PELOTITAS |
| 21 | | El backend actualiza cálculo de stock disponible |
| 22 | | El backend retorna código 201 con el movimiento creado |
| 23 | | El frontend actualiza store y cierra modal |
| 24 | | El sistema muestra mensaje: "Compra registrada exitosamente" |
| 25 | | El sistema refresca lista de movimientos y actualiza resumen de stock |
| 26 | El administrador visualiza la compra en el listado con badge "COMPRA" | |

---

## 7. Flujo Normal - Subproceso B: Registrar Venta

### Trigger/Disparador
Un socio, alumno u otra persona compra pelotitas al club.

### Flujo de Eventos

| # | Actor | Sistema |
|---|-------|---------|
| 1-5 | [Igual que subproceso A, pasos 1-5] | |
| 6 | El administrador selecciona **Tipo: "Venta"** | |
| 7 | | El sistema adapta el formulario mostrando: campos de Comprador, oculta campo Proveedor |
| 8 | El administrador selecciona **Tipo de Comprador** (Socio / Alumno / Otro) | |
| 9 | | El sistema carga dinámicamente la lista correspondiente:<br>- Si "Socio": carga lista de Socios activos<br>- Si "Alumno": carga lista de Alumnos activos<br>- Si "Otro": muestra campo de texto libre |
| 10 | El administrador selecciona el **Comprador** del dropdown O ingresa nombre manual | |
| 11 | El administrador ingresa la **Fecha** de la venta | |
| 12 | El administrador ingresa la **Cantidad** de pelotitas | |
| 13 | El administrador ingresa el **Precio Unitario** de venta | |
| 14 | | El sistema calcula automáticamente: total = cantidad × precio_unitario |
| 15 | | El sistema muestra el total en tiempo real |
| 16 | El administrador opcionalmente agrega **Observaciones** | |
| 17 | El administrador hace clic en "Guardar" | |
| 18 | | El sistema valida que hay stock suficiente para la venta |
| 19 | | El sistema valida todos los campos obligatorios |
| 20 | | El sistema construye objeto Pelotita con tipo="venta" y datos de comprador |
| 21 | | El sistema envía POST a `/api/pelotitas` |
| 22 | | El backend valida stock disponible >= cantidad vendida |
| 23 | | El backend valida integridad referencial (si comprador es socio/alumno) |
| 24 | | El backend ejecuta INSERT en tabla PELOTITAS |
| 25 | | El backend actualiza cálculo de stock disponible (decremento) |
| 26 | | El backend retorna código 201 con el movimiento creado |
| 27 | | El frontend actualiza store y cierra modal |
| 28 | | El sistema muestra mensaje: "Venta registrada exitosamente" |
| 29 | | El sistema refresca lista y resumen mostrando stock actualizado |
| 30 | El administrador visualiza la venta con badge "VENTA" y nombre del comprador | |

---

## 8. Flujos Alternos

### FA-07: Stock Insuficiente para Venta
**Punto de Extensión:** Paso 18 del Subproceso B (Venta)

| # | Descripción |
|---|-------------|
| FA-07.1 | El sistema calcula: stock_disponible = total_compras - total_ventas |
| FA-07.2 | El sistema detecta que cantidad solicitada > stock_disponible |
| FA-07.3 | El sistema muestra mensaje: "Stock insuficiente. Disponible: X unidades" |
| FA-07.4 | El sistema resalta el campo Cantidad en rojo |
| FA-07.5 | El administrador debe reducir la cantidad o cancelar la venta |
| FA-07.6 | Si reduce cantidad, retorna al paso 12 del Subproceso B |

### FA-08: Comprador "Otro" sin Nombre
**Punto de Extensión:** Paso 19 del Subproceso B

| # | Descripción |
|---|-------------|
| FA-08.1 | El administrador seleccionó tipo "Otro" pero dejó el campo nombre vacío |
| FA-08.2 | El sistema valida y detecta que comprador_nombre es NULL o vacío |
| FA-08.3 | El sistema muestra mensaje: "Debe ingresar el nombre del comprador" |
| FA-08.4 | El campo nombre se resalta en rojo |
| FA-08.5 | El administrador debe ingresar el nombre |
| FA-08.6 | Retorna al paso 10 del Subproceso B |

### FA-09: Cantidad o Precio Inválidos
**Punto de Extensión:** Paso 16 de ambos subprocesos

| # | Descripción |
|---|-------------|
| FA-09.1 | El administrador ingresó cantidad <= 0 o precio_unitario <= 0 |
| FA-09.2 | El sistema valida y detecta valores inválidos |
| FA-09.3 | El sistema muestra mensaje: "La cantidad y precio deben ser mayores a cero" |
| FA-09.4 | Los campos se resaltan en rojo |
| FA-09.5 | El administrador debe corregir los valores |

### FA-10: Proveedor No Existe
**Punto de Extensión:** Paso 19 del Subproceso A (Compra)

| # | Descripción |
|---|-------------|
| FA-10.1 | El backend valida el proveedor y detecta que no existe o está inactivo |
| FA-10.2 | El backend retorna código HTTP 400 con mensaje de error |
| FA-10.3 | El frontend muestra: "El proveedor seleccionado no es válido" |
| FA-10.4 | El administrador debe seleccionar otro proveedor o crear uno nuevo |

---

## 9. Reglas de Negocio

| ID | Regla | Descripción |
|----|-------|-------------|
| RN-16 | Tipos de Movimiento | Solo existen dos tipos: "compra" y "venta" |
| RN-17 | Proveedor en Compras | Las compras DEBEN tener un proveedor asociado |
| RN-18 | Comprador en Ventas | Las ventas DEBEN tener un comprador (socio/alumno/otro) |
| RN-19 | Stock No Negativo | El stock disponible nunca puede ser menor a cero |
| RN-20 | Cálculo de Total | total = cantidad × precio_unitario (calculado automáticamente) |
| RN-21 | Valores Positivos | Cantidad, precio_unitario y total deben ser números positivos |
| RN-22 | Tipos de Comprador | Comprador puede ser: "socio", "alumno" u "otro" |
| RN-23 | Nombre Comprador Otro | Si tipo="otro", el campo comprador_nombre es obligatorio |
| RN-24 | Integridad Referencial | Si comprador es socio/alumno, el ID debe existir en su tabla |

---

## 10. Requisitos Especiales

**RNF-08: Cálculo en Tiempo Real**
- El sistema debe calcular y mostrar el precio total instantáneamente mientras el usuario escribe cantidad o precio unitario

**RNF-09: Actualización de Stock**
- El stock debe actualizarse inmediatamente tras cada operación
- El resumen debe mostrar: total compras, total ventas, stock disponible, ganancia total

**RNF-10: Formulario Adaptativo**
- El formulario debe cambiar dinámicamente según el tipo de operación (compra/venta) y tipo de comprador

---

## 11. Diagrama de Estados del Inventario

```
                   ┌─────────────┐
                   │   Inicial   │
                   │  Stock = 0  │
                   └──────┬──────┘
                          │
                   [Compra registrada]
                          │
                          ▼
                   ┌─────────────┐
                   │  Con Stock  │
                   │  Stock > 0  │
                   └──────┬──────┘
                          │
                    ┌─────┴─────┐
                    │           │
         [Compra]   │           │  [Venta]
                    │           │
                    ▼           ▼
            ┌──────────┐  ┌──────────┐
            │ Stock++  │  │ Stock--  │
            └────┬─────┘  └────┬─────┘
                 │             │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │   Stock     │
                 │  Actualizado│
                 └─────────────┘
                        │
                        │ [Stock = 0]
                        ▼
                 ┌─────────────┐
                 │Sin Stock    │
                 │(Bloqueo     │
                 │ ventas)     │
                 └─────────────┘
```

---

## 12. Diagrama de Clases Simplificado (Dominio)

```
┌─────────────────────┐
│     Pelotita        │
├─────────────────────┤
│ - id: int           │
│ - fecha: date       │
│ - tipo: enum        │ ◄────────┐
│ - cantidad: int     │          │
│ - precio_unit: dec  │          │
│ - total: decimal    │          │
│ - observaciones:str │          │
└──────────┬──────────┘          │
           │                     │
    ┌──────┴──────┐              │
    │             │              │
    ▼             ▼              │
┌─────────┐  ┌──────────────────┴───┐
│Proveedor│  │    Comprador         │
├─────────┤  ├──────────────────────┤
│- id:int │  │- tipo: enum          │
│- nombre │  │- id: int (nullable)  │
└─────────┘  │- nombre: string      │
             └──┬────────────┬──────┘
                │            │
                ▼            ▼
           ┌────────┐   ┌────────┐
           │ Socio  │   │ Alumno │
           └────────┘   └────────┘
```

---

## 13. Matriz de Trazabilidad

| Requisito Funcional | Componente Frontend | Componente Backend | Tabla BD | Regla de Negocio |
|---------------------|---------------------|-------------------|----------|------------------|
| Seleccionar tipo operación | PelotitasCreate.vue (select) | - | PELOTITAS.tipo | RN-16 |
| Seleccionar proveedor | PelotitasCreate.vue (select) | - | PELOTITAS.proveedor | RN-17 |
| Seleccionar tipo comprador | PelotitasCreate.vue (select) | - | PELOTITAS.comprador_tipo | RN-22 |
| Cargar lista compradores | usePelotitasStore | socio/alumno controllers | SOCIOS/ALUMNOS | RN-24 |
| Ingresar cantidad | PelotitasCreate.vue (input) | pelotita_model.py | PELOTITAS.cantidad | RN-21 |
| Calcular total | PelotitasCreate.vue (computed) | - | PELOTITAS.total | RN-20 |
| Validar stock | - | pelotita_model.py | - | RN-19 |
| Guardar movimiento | - | pelotita_model.py create() | PELOTITAS (INSERT) | Todas |
| Mostrar resumen stock | PelotitasList.vue | pelotita_model.py get_resumen() | PELOTITAS (aggregate) | RN-19 |

---

## 14. Consulta SQL para Cálculo de Stock

El sistema utiliza la siguiente lógica para calcular el stock en tiempo real:

```sql
-- Stock Disponible
SELECT 
    COALESCE(SUM(CASE WHEN tipo = 'compra' THEN cantidad ELSE 0 END), 0) as total_comprado,
    COALESCE(SUM(CASE WHEN tipo = 'venta' THEN cantidad ELSE 0 END), 0) as total_vendido,
    COALESCE(SUM(CASE WHEN tipo = 'compra' THEN cantidad ELSE -cantidad END), 0) as stock_disponible
FROM PELOTITAS;

-- Ganancia Total
SELECT 
    COALESCE(SUM(CASE WHEN tipo = 'venta' THEN total ELSE 0 END), 0) as ingresos_venta,
    COALESCE(SUM(CASE WHEN tipo = 'compra' THEN total ELSE 0 END), 0) as costo_compra,
    COALESCE(SUM(CASE WHEN tipo = 'venta' THEN total ELSE -total END), 0) as ganancia_neta
FROM PELOTITAS;
```

---

## 15. Extensiones Futuras

- **CU-11: Alertas de Stock Mínimo** - Notificar cuando el stock sea inferior a umbral
- **CU-12: Análisis de Rentabilidad** - Dashboard con margen de ganancia por período
- **CU-13: Gestión de Devoluciones** - Registrar pelotitas devueltas por clientes
- **CU-14: Integración con Proveedores** - Pedidos automáticos cuando stock es bajo

---

# CONCLUSIONES DEL ANÁLISIS

## Importancia de los Casos de Uso Seleccionados

Los tres casos de uso analizados representan el **núcleo operativo** del Sistema SiPePa:

1. **CU-01: Registrar Pago** - Gestión financiera (ingresos)
2. **CU-02: Reservar Turno** - Gestión de recursos (canchas)
3. **CU-03: Gestionar Inventario** - Control de mercancías (pelotitas)

## Complejidad Técnica

| Caso de Uso | Actores | Entidades Relacionadas | Flujos Alternos | Reglas de Negocio | Complejidad |
|-------------|---------|------------------------|-----------------|-------------------|-------------|
| CU-01 | 4 | 4 (PAGOS, SOCIOS, ALUMNOS, PROFESORES) | 6 | 8 | **ALTA** |
| CU-02 | 2 | 2 (TURNOS, SOCIOS) | 5 | 7 | **MEDIA-ALTA** |
| CU-03 | 4 | 4 (PELOTITAS, PROVEEDORES, SOCIOS, ALUMNOS) | 4 | 9 | **ALTA** |

## Patrones UML Aplicados

### Relaciones Identificadas

- **<<include>>**: Validaciones obligatorias dentro de cada caso de uso
- **<<extend>>**: Funcionalidades opcionales (ej: selección de profesor solo en tipo "Clase")
- **Generalización**: Actor Administrador como principal en todos los casos

### Principios SOLID Aplicados

1. **Single Responsibility**: Cada modelo maneja una única entidad de negocio
2. **Open/Closed**: Casos de uso extensibles sin modificar código base
3. **Dependency Inversion**: Frontend depende de abstracciones (stores) no de implementaciones concretas

## Métricas de Calidad

| Métrica | Valor | Observación |
|---------|-------|-------------|
| Cobertura de funcionalidades críticas | 100% | Los 3 CU cubren operaciones esenciales |
| Trazabilidad requisitos → código | Completa | Matriz de trazabilidad documentada |
| Validaciones implementadas | 2 capas | Cliente (UX) y Servidor (seguridad) |
| Manejo de errores | Robusto | Flujos alternos y de excepción definidos |
| Documentación UML | Completa | Diagramas de secuencia, estados y clases |

---

**Analista:** GitHub Copilot (Claude Sonnet 4.5)  
**Fecha de Análisis:** 28 de noviembre de 2025  
**Metodología:** UML 2.5 + Análisis de Sistemas Orientado a Objetos  
**Framework de Referencia:** Larman - Applying UML and Patterns
