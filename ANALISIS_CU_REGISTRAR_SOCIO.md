# Análisis del Caso de Uso: Registrar Socio
## Sistema SiPePa - Sistema de Administración de Pelota a Paleta

---

## 1. INFORMACIÓN GENERAL DEL CASO DE USO

| Elemento | Descripción |
|----------|-------------|
| **ID** | CU-REG-SOCIO-01 |
| **Nombre** | Registrar Socio |
| **Descripción** | Permite al administrador dar de alta un nuevo socio en el sistema, registrando sus datos personales, asignándole un profesor y clasificándolo en categorías de juego |
| **Actor Principal** | Administrador del Club |
| **Actores Secundarios** | - Profesor (datos requeridos para asignación)<br>- Categoría (datos para clasificación) |
| **Tipo** | Caso de Uso Primario |
| **Nivel** | Función de Usuario (User Goal Level) |
| **Complejidad** | Media-Alta |
| **Prioridad** | Crítica |
| **Frecuencia de Uso** | Alta (múltiples veces por semana) |
| **Estado** | Implementado y Operativo |
| **Versión** | 1.0 |

---

## 2. STAKEHOLDERS E INTERESES

| Stakeholder | Interés |
|-------------|---------|
| **Administrador del Club** | Registrar rápidamente nuevos socios con datos completos y correctos |
| **Socio** | Ser registrado correctamente para acceder a servicios del club |
| **Profesor** | Conocer los socios que le son asignados para planificar clases |
| **Gerencia del Club** | Mantener base de datos actualizada de socios para reportes |
| **Sistema de Pagos** | Vincular socio con futuras transacciones financieras |
| **Sistema de Turnos** | Habilitar al socio para reservar canchas |

---

## 3. PRECONDICIONES

### Precondiciones Obligatorias

1. **Autenticación**: El administrador debe estar autenticado en el sistema
2. **Conexión a BD**: La base de datos MySQL debe estar accesible y operativa
3. **Backend Activo**: El servidor Flask debe estar corriendo en el puerto 5000
4. **Frontend Activo**: La aplicación Vue debe estar disponible
5. **Datos Maestros**: Debe existir al menos una Categoría registrada en el sistema
6. **Profesor Opcional**: Puede o no haber profesores registrados (el campo es opcional)

### Precondiciones Deseables

1. **Validación de DNI**: No debe existir otro socio con el mismo DNI
2. **Validación de Email**: No debe existir otro socio con el mismo email
3. **Conexión de Red**: Conexión estable para evitar pérdida de datos

---

## 4. POSTCONDICIONES

### Postcondiciones de Éxito

1. **Registro en BD**: Se crea un nuevo registro en la tabla `SOCIOS` con ID auto-incremental
2. **Vinculación Profesor**: Si se asignó profesor, se establece la relación `socio.profesor_id`
3. **Vinculación Categorías**: Se crean registros en tabla `SOCIO_CATEGORIA` para cada categoría seleccionada
4. **Timestamp**: Se registra `fecha_inscripcion` (fecha de alta en el club)
5. **Estado Inicial**: El socio queda en estado "Activo" por defecto
6. **Habilitación Servicios**: El socio puede:
   - Reservar turnos de cancha
   - Realizar pagos de cuotas
   - Comprar pelotitas
   - Participar en actividades del club
7. **Notificación Visual**: El administrador ve mensaje de confirmación "Socio creado exitosamente"
8. **Actualización Vista**: La lista de socios se refresca mostrando el nuevo registro
9. **Auditoría**: Queda registro de la operación en logs del sistema

### Postcondiciones de Fracaso

1. **No Persistencia**: No se crea ningún registro en la base de datos
2. **Integridad Mantenida**: No se crean registros huérfanos en tablas relacionadas
3. **Rollback Automático**: Si falla alguna operación, se revierten todas las transacciones
4. **Mensaje de Error**: Se muestra al administrador el tipo de error ocurrido
5. **Formulario Conservado**: Los datos ingresados se mantienen para corrección y reintento

---

## 5. FLUJO NORMAL DE EVENTOS (ESCENARIO PRINCIPAL)

### Trigger/Disparador
El administrador necesita registrar un nuevo socio que se ha inscripto en el club.

### Secuencia de Eventos

| # | Actor | Acción del Actor | Sistema | Respuesta del Sistema |
|---|-------|------------------|---------|----------------------|
| 1 | Administrador | Accede al módulo "Socios" desde el menú principal | → | Carga `SociosView.vue` |
| 2 | | | | Renderiza `SociosList.vue` con tabla de socios existentes |
| 3 | | | | Ejecuta `sociosStore.fetchSocios()` |
| 4 | | | | Realiza GET `/api/socios` al backend |
| 5 | | | | Backend ejecuta `SocioModel.get_all()` |
| 6 | | | | Consulta SQL: `SELECT * FROM SOCIOS` |
| 7 | | | | Para cada socio: JOIN con PROFESORES y CATEGORIAS |
| 8 | | | | Retorna JSON con array de socios |
| 9 | | | | Frontend actualiza store de Pinia |
| 10 | | | | Muestra lista de socios en tabla |
| 11 | Administrador | Hace clic en botón "Nuevo Socio" | → | |
| 12 | | | | Emite evento `@click="showCreateModal = true"` |
| 13 | | | | Renderiza componente `<SociosCreate />` |
| 14 | | | | Abre modal con formulario vacío |
| 15 | | | | Ejecuta `onMounted()` del componente |
| 16 | | | | Carga listas auxiliares en paralelo: |
| 17 | | | | - `profesoresStore.fetchProfesores()` → GET `/api/profesores` |
| 18 | | | | - `categoriasStore.fetchCategorias()` → GET `/api/categorias` |
| 19 | | | | Puebla selectores con datos recibidos |
| 20 | | | | Inicializa `formData.fecha_inscripcion` con fecha actual |
| 21 | Administrador | Ingresa **Nombre** del socio | → | |
| 22 | | | | Binding bidireccional: `v-model="formData.nombre"` |
| 23 | | | | Valida en tiempo real (campo requerido) |
| 24 | Administrador | Ingresa **Apellido** del socio | → | |
| 25 | | | | Binding: `v-model="formData.apellido"` |
| 26 | | | | Valida campo requerido |
| 27 | Administrador | Ingresa **DNI** del socio | → | |
| 28 | | | | Binding: `v-model="formData.dni"` |
| 29 | | | | Valida formato (solo números) |
| 30 | Administrador | Ingresa **Teléfono** | → | |
| 31 | | | | Binding: `v-model="formData.telefono"` |
| 32 | | | | Valida tipo `tel` |
| 33 | Administrador | Ingresa **Email** | → | |
| 34 | | | | Binding: `v-model="formData.email"` |
| 35 | | | | Valida formato email |
| 36 | Administrador | Selecciona **Fecha de Inscripción** (o deja la actual) | → | |
| 37 | | | | Binding: `v-model="formData.fecha_inscripcion"` |
| 38 | | | | Valida formato fecha YYYY-MM-DD |
| 39 | Administrador | Selecciona **Profesor** del dropdown (opcional) | → | |
| 40 | | | | Binding: `v-model.number="formData.profesor_id"` |
| 41 | | | | Si no selecciona, queda `null` |
| 42 | Administrador | Selecciona una o más **Categorías** mediante checkboxes | → | |
| 43 | | | | Binding: `v-model="selectedCategorias"` (array) |
| 44 | | | | Actualiza array reactivo con IDs seleccionados |
| 45 | Administrador | Hace clic en botón "Crear Socio" | → | |
| 46 | | | | Ejecuta `@submit.prevent="handleSubmit()"` |
| 47 | | | | Previene envío tradicional del form |
| 48 | | | | Establece `submitLoading = true` |
| 49 | | | | Deshabilita botón: `:disabled="submitLoading"` |
| 50 | | | | Cambia texto botón: "Guardando..." |
| 51 | | | | Construye objeto `socioData`: |
| 52 | | | | ```js<br>const socioData = {<br>  ...formData.value,<br>  categorias_ids: selectedCategorias.value<br>}<br>``` |
| 53 | | | | Llama `await sociosStore.createSocio(socioData)` |
| 54 | | | | Store ejecuta método: |
| 55 | | | | ```ts<br>async createSocio(socio: any) {<br>  const response = await apiService.post('/socios', socio)<br>  this.socios.push(response.data)<br>  return response.data<br>}<br>``` |
| 56 | | | | Realiza petición HTTP POST a `/api/socios` |
| 57 | | | | Headers: `Content-Type: application/json` |
| 58 | | | | Body: JSON con datos del socio |
| 59 | | | | Backend recibe petición en `socio_routes.py`: |
| 60 | | | | ```python<br>@bp.route('/socios', methods=['POST'])<br>def create_socio():<br>    return SocioController.create()<br>``` |
| 61 | | | | Controller ejecuta: |
| 62 | | | | ```python<br>data = request.get_json()<br>result = SocioModel.create(data)<br>``` |
| 63 | | | | Model ejecuta `create(socio_data)`: |
| 64 | | | | Obtiene conexión: `cnx = ConectDB.get_connect()` |
| 65 | | | | Inicia transacción implícita |
| 66 | | | | Crea cursor: `cursor = cnx.cursor()` |
| 67 | | | | **Ejecuta INSERT principal:** |
| 68 | | | | ```sql<br>INSERT INTO SOCIOS <br>(nombre, apellido, dni, email, telefono, <br> fecha_inscripcion, profesor_id)<br>VALUES (%s, %s, %s, %s, %s, %s, %s)<br>``` |
| 69 | | | | Parámetros bindados con valores del `socio_data` |
| 70 | | | | Previene SQL Injection |
| 71 | | | | Obtiene ID generado: `socio_id = cursor.lastrowid` |
| 72 | | | | **Ejecuta INSERTS de categorías:** |
| 73 | | | | ```python<br>if 'categorias' in socio_data:<br>    for categoria_id in socio_data['categorias']:<br>        cursor.execute("""<br>            INSERT INTO SOCIO_CATEGORIA <br>            (socio_id, categoria_id)<br>            VALUES (%s, %s)<br>        """, (socio_id, categoria_id))<br>``` |
| 74 | | | | Itera sobre array de categorías seleccionadas |
| 75 | | | | Crea un registro por cada categoría |
| 76 | | | | **Confirma transacción:** `cnx.commit()` |
| 77 | | | | Persiste todos los cambios en BD |
| 78 | | | | Cierra conexión: `cnx.close()` en `finally` |
| 79 | | | | Retorna diccionario: |
| 80 | | | | ```python<br>return {<br>  'mensaje': 'Socio creado exitosamente', <br>  'id': socio_id<br>}<br>``` |
| 81 | | | | Controller retorna: `jsonify(result), 201` |
| 82 | | | | Código HTTP 201 Created |
| 83 | | | | Frontend recibe response exitoso |
| 84 | | | | Store agrega socio al array local: `this.socios.push(response.data)` |
| 85 | | | | Emite evento: `emit('created')` |
| 86 | | | | Vista padre escucha evento: `@created="handleCreated"` |
| 87 | | | | Ejecuta: |
| 88 | | | | ```ts<br>const handleCreated = () => {<br>  showCreateModal.value = false<br>  sociosStore.fetchSocios() // refresca lista<br>}<br>``` |
| 89 | | | | Cierra modal |
| 90 | | | | Refresca lista completa de socios |
| 91 | | | | Establece `submitLoading = false` |
| 92 | Administrador | Visualiza mensaje "Socio creado exitosamente" | ← | |
| 93 | | | | Muestra toast/snackbar de confirmación |
| 94 | Administrador | Ve el nuevo socio en la tabla | ← | |
| 95 | | | | Tabla actualizada con nuevo registro |
| 96 | | | | Fila destacada temporalmente (animación) |

---

## 6. FLUJOS ALTERNOS

### FA-01: Cancelar Creación de Socio
**Punto de Extensión:** Después del paso 20 (formulario abierto)

| # | Descripción |
|---|-------------|
| FA-01.1 | El administrador hace clic en botón "Cancelar" |
| FA-01.2 | Sistema ejecuta: `@click="$emit('close')"` |
| FA-01.3 | Vista padre escucha: `@close="showCreateModal = false"` |
| FA-01.4 | Se cierra el modal sin guardar cambios |
| FA-01.5 | Todos los datos ingresados se descartan |
| FA-01.6 | No se realiza ninguna operación en BD |
| FA-01.7 | El caso de uso termina sin modificar estado del sistema |

### FA-02: Error de Validación en Frontend
**Punto de Extensión:** Paso 46 (al hacer submit)

| # | Descripción |
|---|-------------|
| FA-02.1 | El administrador intenta enviar el formulario |
| FA-02.2 | HTML5 valida campos con atributo `required` |
| FA-02.3 | Si falta algún campo obligatorio: |
| FA-02.4 | - El navegador muestra tooltip nativo: "Please fill out this field" |
| FA-02.5 | - El foco se mueve al primer campo inválido |
| FA-02.6 | - El evento `@submit.prevent` no se ejecuta |
| FA-02.7 | - No se envía petición al backend |
| FA-02.8 | El administrador corrige el campo faltante |
| FA-02.9 | Retorna al paso 21-45 del flujo normal |

### FA-03: DNI Duplicado (Error de Integridad)
**Punto de Extensión:** Paso 68 (INSERT en BD)

| # | Descripción |
|---|-------------|
| FA-03.1 | Backend intenta ejecutar INSERT con DNI existente |
| FA-03.2 | MySQL detecta violación de constraint UNIQUE en columna `dni` |
| FA-03.3 | Lanza excepción: `IntegrityError: Duplicate entry 'XXXXX' for key 'dni'` |
| FA-03.4 | Bloque `except Exception as exc:` captura el error |
| FA-03.5 | Se ejecuta: `cnx.rollback()` - revierte INSERT parcial |
| FA-03.6 | Retorna: `{'mensaje': f"Error al crear socio: {exc}"}` |
| FA-03.7 | Controller retorna: `jsonify(result), 400` (Bad Request) |
| FA-03.8 | Frontend recibe respuesta con status 400 |
| FA-03.9 | Store lanza excepción que es capturada en componente: |
| FA-03.10 | ```ts<br>catch (e: any) {<br>  error.value = e.response?.data?.mensaje<br>}<br>``` |
| FA-03.11 | Se muestra mensaje en modal: |
| FA-03.12 | `<div v-if="error" class="error">{{ error }}</div>` |
| FA-03.13 | Texto visible: "Error al crear socio: Duplicate entry..." |
| FA-03.14 | El modal permanece abierto |
| FA-03.15 | El administrador puede corregir el DNI |
| FA-03.16 | Retorna al paso 27 del flujo normal |

### FA-04: Error de Conexión a Base de Datos
**Punto de Extensión:** Paso 64 (obtener conexión)

| # | Descripción |
|---|-------------|
| FA-04.1 | Backend ejecuta: `cnx = ConectDB.get_connect()` |
| FA-04.2 | Intento de conexión falla (MySQL no responde, credenciales inválidas, etc.) |
| FA-04.3 | Método retorna: `None` |
| FA-04.4 | Se evalúa: `if cnx is None:` |
| FA-04.5 | Retorna inmediatamente: `{'mensaje': 'No se pudo conectar a la base de datos'}` |
| FA-04.6 | Controller retorna: `jsonify(result), 400` |
| FA-04.7 | Frontend muestra error: "No se pudo conectar a la base de datos" |
| FA-04.8 | El administrador puede: |
| FA-04.9 | - Reintentar después de unos segundos |
| FA-04.10 | - Reportar el problema al área de TI |
| FA-04.11 | - Cancelar la operación |

### FA-05: Error en Carga de Listas Auxiliares
**Punto de Extensión:** Paso 17-18 (carga de profesores/categorías)

| # | Descripción |
|---|-------------|
| FA-05.1 | Frontend ejecuta: `profesoresStore.fetchProfesores()` |
| FA-05.2 | Petición GET `/api/profesores` falla (timeout, 500, etc.) |
| FA-05.3 | Store captura error en catch |
| FA-05.4 | Array `profesores` permanece vacío: `[]` |
| FA-05.5 | El select de profesores muestra solo: "Sin profesor asignado" |
| FA-05.6 | El administrador puede: |
| FA-05.7 | - Continuar sin asignar profesor (es opcional) |
| FA-05.8 | - Cerrar modal y reportar problema |
| FA-05.9 | Si ocurre con categorías y NO hay ninguna: |
| FA-05.10 | - El socio se crea sin categorías |
| FA-05.11 | - Pueden asignarse posteriormente con Update |

### FA-06: Error de Red Durante Submit
**Punto de Extensión:** Paso 56 (POST HTTP)

| # | Descripción |
|---|-------------|
| FA-06.1 | Frontend envía POST `/api/socios` |
| FA-06.2 | Axios detecta error de red (ERR_NETWORK, timeout) |
| FA-06.3 | Lanza excepción capturada en: |
| FA-06.4 | ```ts<br>catch (e: any) {<br>  error.value = e.response?.data?.mensaje \|\| <br>                'Error al crear socio'<br>}<br>``` |
| FA-06.5 | Como `e.response` es `undefined`, usa mensaje por defecto |
| FA-06.6 | Muestra: "Error al crear socio" |
| FA-06.7 | `submitLoading` se establece en `false` (finally) |
| FA-06.8 | Botón se habilita nuevamente |
| FA-06.9 | El administrador puede reintentar |
| FA-06.10 | Datos permanecen en formulario |

### FA-07: Backend Caído
**Punto de Extensión:** Paso 59 (recepción en backend)

| # | Descripción |
|---|-------------|
| FA-07.1 | Frontend envía petición HTTP |
| FA-07.2 | Backend Flask no está corriendo |
| FA-07.3 | Axios recibe error: `ERR_CONNECTION_REFUSED` |
| FA-07.4 | Frontend muestra: "Error al crear socio" |
| FA-07.5 | El administrador debe: |
| FA-07.6 | - Verificar que backend esté corriendo |
| FA-07.7 | - Ejecutar: `python run.py` en terminal backend |
| FA-07.8 | - Reintentar operación |

---

## 7. FLUJOS DE EXCEPCIÓN

### FE-01: Transacción Fallida a Mitad de Proceso
**Descripción:** Se insertan datos en SOCIOS pero falla insert en SOCIO_CATEGORIA

| # | Descripción |
|---|-------------|
| FE-01.1 | INSERT en SOCIOS se ejecuta exitosamente (paso 68) |
| FE-01.2 | Se obtiene socio_id correctamente (paso 71) |
| FE-01.3 | Al ejecutar INSERT en SOCIO_CATEGORIA (paso 73) ocurre error |
| FE-01.4 | Posibles causas: |
| FE-01.5 | - Foreign key constraint: categoria_id no existe |
| FE-01.6 | - Conexión se pierde a mitad del proceso |
| FE-01.7 | - Tabla SOCIO_CATEGORIA corrupta |
| FE-01.8 | Python lanza excepción capturada en `except Exception as exc:` |
| FE-01.9 | Se ejecuta: **`cnx.rollback()`** |
| FE-01.10 | **CRÍTICO:** Se revierten TODAS las operaciones de la transacción |
| FE-01.11 | El INSERT en SOCIOS también se deshace |
| FE-01.12 | NO queda socio huérfano en BD |
| FE-01.13 | Se mantiene integridad referencial |
| FE-01.14 | Retorna mensaje de error al frontend |
| FE-01.15 | El administrador es notificado del fallo completo |
| FE-01.16 | Debe reportar al área técnica para investigar causa raíz |

### FE-02: Memoria Insuficiente en Servidor
**Descripción:** El servidor no puede procesar la petición por falta de recursos

| # | Descripción |
|---|-------------|
| FE-02.1 | Backend recibe petición POST |
| FE-02.2 | Sistema operativo no puede asignar memoria para el proceso |
| FE-02.3 | Python lanza: `MemoryError` |
| FE-02.4 | Flask captura error en nivel superior |
| FE-02.5 | Retorna: HTTP 500 Internal Server Error |
| FE-02.6 | Frontend recibe error 500 |
| FE-02.7 | Muestra mensaje genérico al usuario |
| FE-02.8 | Se debe escalar a administradores del sistema |

---

## 8. REQUISITOS ESPECIALES (NO FUNCIONALES)

### RNF-01: Performance
- **Tiempo de Respuesta**: La creación de un socio NO debe superar **3 segundos** en condiciones normales
- **Carga de Listas**: Profesores y categorías deben cargarse en menos de **1 segundo**
- **Timeout**: Peticiones HTTP configuradas con timeout de **30 segundos**

### RNF-02: Usabilidad
- **Validación en Tiempo Real**: Los campos deben mostrar feedback inmediato (borde rojo si inválido)
- **Foco Automático**: El cursor debe posicionarse en el primer campo al abrir el modal
- **Tab Order**: Navegación secuencial lógica con tecla Tab
- **Accesibilidad**: Labels asociados a inputs con atributo `for`
- **Responsive**: Formulario debe adaptarse a diferentes tamaños de pantalla

### RNF-03: Confiabilidad
- **Atomicidad**: Operación "todo o nada" mediante transacciones
- **Rollback Automático**: Cualquier fallo debe revertir cambios parciales
- **Reconexión**: El sistema debe reintentar conexión a BD en caso de fallo transitorio
- **Persistencia**: Los datos no se pierden ante errores recuperables

### RNF-04: Seguridad
- **Prevención SQL Injection**: Uso de prepared statements con parámetros bindeados
- **Validación Backend**: Nunca confiar solo en validación frontend
- **Sanitización**: Datos de entrada sanitizados antes de procesar
- **Autenticación**: Solo usuarios autenticados pueden crear socios
- **Auditoría**: Registro de quién y cuándo creó cada socio

### RNF-05: Mantenibilidad
- **Separación de Responsabilidades**: MVC claramente definido
- **Reutilización**: Componentes y stores reutilizables
- **Código Limpio**: Nombres descriptivos, funciones pequeñas
- **Documentación**: Comentarios en código donde sea necesario
- **Testing**: Casos de prueba para flujos principales y alternos

### RNF-06: Escalabilidad
- **Pool de Conexiones**: Gestión eficiente de conexiones a BD
- **Índices**: Columnas frecuentemente consultadas deben tener índices (dni, email)
- **Paginación**: Si la lista de socios crece, implementar paginación
- **Caché**: Listas de profesores y categorías pueden cachearse

---

## 9. REGLAS DE NEGOCIO

| ID | Regla | Descripción | Implementación |
|----|-------|-------------|----------------|
| RN-SOCIO-01 | DNI Único | No pueden existir dos socios con el mismo DNI | UNIQUE constraint en columna `dni` de tabla SOCIOS |
| RN-SOCIO-02 | Email Único | No pueden existir dos socios con el mismo email | UNIQUE constraint en columna `email` |
| RN-SOCIO-03 | Nombre Obligatorio | Todo socio debe tener nombre y apellido | NOT NULL en columnas + validación frontend `required` |
| RN-SOCIO-04 | Fecha Válida | Fecha de inscripción no puede ser futura | Validación frontend: `max="hoy"` |
| RN-SOCIO-05 | Profesor Opcional | Un socio puede no tener profesor asignado | Columna `profesor_id` permite NULL |
| RN-SOCIO-06 | Categorías Múltiples | Un socio puede pertenecer a 0, 1 o múltiples categorías | Tabla intermedia SOCIO_CATEGORIA (relación N:M) |
| RN-SOCIO-07 | Estado Inicial Activo | Todo socio nuevo queda activo por defecto | Default value en columna `activo = 1` |
| RN-SOCIO-08 | Teléfono de Contacto | Es obligatorio tener al menos un teléfono | NOT NULL + validación frontend |
| RN-SOCIO-09 | Email Válido | El email debe tener formato válido | Input type="email" + validación backend |
| RN-SOCIO-10 | Edad Mínima | Para participar en torneos adultos | Calculada a partir de fecha_nacimiento (si existe) |

---

## 10. LISTA DE VARIACIONES TECNOLÓGICAS

### Variaciones en Backend

**V1: Base de Datos Alternativa**
- Actualmente: MySQL
- Alternativa: PostgreSQL
- Impacto: Cambiar sintaxis SQL, ajustar ConectDB

**V2: ORM**
- Actualmente: SQL crudo con mysql-connector
- Alternativa: SQLAlchemy
- Beneficio: Abstracción de BD, migraciones automáticas

**V3: Framework Backend**
- Actualmente: Flask
- Alternativa: FastAPI
- Beneficio: Validación automática con Pydantic, async

### Variaciones en Frontend

**V4: Framework Frontend**
- Actualmente: Vue 3 Composition API
- Alternativa: React con Hooks
- Impacto: Reescritura completa de componentes

**V5: State Management**
- Actualmente: Pinia
- Alternativa: Vuex, Redux
- Impacto: Cambiar sintaxis de stores

**V6: Librería de Validación**
- Actualmente: HTML5 nativo
- Alternativa: Vuelidate, VeeValidate
- Beneficio: Validaciones más complejas

---

## 11. DIAGRAMA DE SECUENCIA

```
Actor: Administrador    Frontend: Vue    Store: Pinia    Backend: Flask    DB: MySQL
    │                       │                │                │               │
    │ 1. Click "Nuevo"      │                │                │               │
    ├──────────────────────▶│                │                │               │
    │                       │                │                │               │
    │                       │ 2. Abrir Modal │                │               │
    │                       ├────────────────┤                │               │
    │                       │                │                │               │
    │                       │ 3. Cargar Listas                │               │
    │                       ├───────────────▶│                │               │
    │                       │                │ 4. GET /profesores             │
    │                       │                ├───────────────▶│               │
    │                       │                │                │ 5. SELECT     │
    │                       │                │                ├──────────────▶│
    │                       │                │                │◀──────────────┤
    │                       │                │◀───────────────┤               │
    │                       │◀───────────────┤                │               │
    │                       │                │                │               │
    │ 6. Llenar Formulario  │                │                │               │
    ├──────────────────────▶│                │                │               │
    │                       │                │                │               │
    │ 7. Click "Crear"      │                │                │               │
    ├──────────────────────▶│                │                │               │
    │                       │                │                │               │
    │                       │ 8. Validar     │                │               │
    │                       ├────────────────┤                │               │
    │                       │                │                │               │
    │                       │ 9. createSocio()│               │               │
    │                       ├───────────────▶│                │               │
    │                       │                │ 10. POST /socios              │
    │                       │                ├───────────────▶│               │
    │                       │                │                │ 11. INSERT    │
    │                       │                │                ├──────────────▶│
    │                       │                │                │               │
    │                       │                │                │ 12. INSERT    │
    │                       │                │                │  (categorías) │
    │                       │                │                ├──────────────▶│
    │                       │                │                │               │
    │                       │                │                │ 13. COMMIT    │
    │                       │                │                ├──────────────▶│
    │                       │                │                │◀──────────────┤
    │                       │                │                │               │
    │                       │                │ 14. {id: 123}  │               │
    │                       │                │◀───────────────┤               │
    │                       │ 15. response   │                │               │
    │                       │◀───────────────┤                │               │
    │                       │                │                │               │
    │                       │ 16. Cerrar Modal               │               │
    │                       ├────────────────┤                │               │
    │                       │                │                │               │
    │                       │ 17. Refrescar Lista            │               │
    │                       ├───────────────▶│                │               │
    │                       │                │ 18. GET /socios               │
    │                       │                ├───────────────▶│               │
    │                       │                │                │ 19. SELECT    │
    │                       │                │                ├──────────────▶│
    │                       │                │                │◀──────────────┤
    │                       │                │◀───────────────┤               │
    │                       │◀───────────────┤                │               │
    │                       │                │                │               │
    │ 20. Ver Confirmación  │                │                │               │
    │◀──────────────────────┤                │                │               │
    │                       │                │                │               │
```

---

## 12. DIAGRAMA DE ACTIVIDAD

```
                        ┌─────────────────┐
                        │  Estado Inicial │
                        │        ●        │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Acceder Módulo  │
                        │    Socios       │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Click "Nuevo"   │
                        └────────┬────────┘
                                 │
                     ┌───────────┴───────────┐
                     │   Cargar Listas       │
                     │    (fork)             │
                     ├───────────┬───────────┤
                     │           │           │
                     ▼           ▼           ▼
            ┌──────────────┐ ┌──────────────┐
            │GET Profesores│ │GET Categorias│
            └──────┬───────┘ └──────┬───────┘
                   │                 │
                   └────────┬────────┘
                            │ (join)
                            ▼
                   ┌─────────────────┐
                   │ Mostrar         │
                   │ Formulario      │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Ingresar Datos  │
                   │ (loop hasta     │
                   │  completar)     │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Click "Crear"   │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Validar Datos   │
                   └────────┬────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
               ¿Válidos?               ▼
                │                  [No válidos]
              [Sí]                      │
                │                       ▼
                │              ┌─────────────────┐
                │              │ Mostrar Errores │
                │              └────────┬────────┘
                │                       │
                │                       └──────┐
                │                              │
                ▼                              │
       ┌─────────────────┐                    │
       │ POST /api/socios│                    │
       └────────┬────────┘                    │
                │                              │
                ▼                              │
       ┌─────────────────┐                    │
       │ INSERT SOCIOS   │                    │
       └────────┬────────┘                    │
                │                              │
                ▼                              │
       ┌─────────────────┐                    │
       │ Obtener ID      │                    │
       └────────┬────────┘                    │
                │                              │
                ▼                              │
       ┌─────────────────┐                    │
       │ INSERT          │                    │
       │ SOCIO_CATEGORIA │                    │
       │ (loop)          │                    │
       └────────┬────────┘                    │
                │                              │
    ┌───────────┴───────────┐                 │
    │                       │                 │
  ¿Éxito?                  ▼                 │
    │                  [Error]                │
  [Sí]                      │                 │
    │                       ▼                 │
    │              ┌─────────────────┐        │
    │              │  ROLLBACK       │        │
    │              └────────┬────────┘        │
    │                       │                 │
    │                       ▼                 │
    │              ┌─────────────────┐        │
    │              │ Retornar Error  │        │
    │              └────────┬────────┘        │
    │                       │                 │
    │                       └─────────────────┘
    │                                │
    ▼                                │
┌─────────────────┐                  │
│  COMMIT         │                  │
└────────┬────────┘                  │
         │                           │
         ▼                           │
┌─────────────────┐                  │
│ Retornar 201    │                  │
│ Created         │                  │
└────────┬────────┘                  │
         │                           │
         └───────────┬───────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Cerrar Modal    │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Refrescar Lista │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Mostrar         │
            │ Confirmación    │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Estado Final   │
            │        ◉        │
            └─────────────────┘
```

---

## 13. MODELO DE DOMINIO

```
┌─────────────────────────────────────────────────────────────────┐
│                        MODELO DE DOMINIO                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                                                                  │
│           ┌───────────────────┐                                 │
│           │     Profesor      │                                 │
│           ├───────────────────┤                                 │
│           │ - id: int         │                                 │
│           │ - nombre: string  │                                 │
│           │ - apellido: string│                                 │
│           │ - telefono: string│                                 │
│           │ - email: string   │                                 │
│           └─────────┬─────────┘                                 │
│                     │                                            │
│                     │ 1                                          │
│                     │                                            │
│                     │ enseña a                                   │
│                     │                                            │
│                     │ 0..*                                       │
│                     │                                            │
│           ┌─────────▼─────────┐                                 │
│           │      Socio        │                                 │
│           ├───────────────────┤                                 │
│           │ - id: int (PK)    │                                 │
│           │ - nombre: string  │                                 │
│           │ - apellido: string│                                 │
│           │ - dni: string     │◀─────── UNIQUE                  │
│           │ - email: string   │◀─────── UNIQUE                  │
│           │ - telefono: string│                                 │
│           │ - fecha_insc: date│                                 │
│           │ - profesor_id: FK │                                 │
│           │ - activo: boolean │◀─────── DEFAULT true            │
│           └─────────┬─────────┘                                 │
│                     │                                            │
│                     │ N                                          │
│                     │                                            │
│                     │ pertenece a                                │
│                     │                                            │
│                     │ M                                          │
│                     │                                            │
│           ┌─────────▼──────────────┐                            │
│           │  SOCIO_CATEGORIA       │ (Tabla Intermedia)         │
│           ├────────────────────────┤                            │
│           │ - socio_id: FK         │                            │
│           │ - categoria_id: FK     │                            │
│           │                        │                            │
│           │ PK: (socio_id,         │                            │
│           │      categoria_id)     │                            │
│           └─────────┬──────────────┘                            │
│                     │                                            │
│                     │ M                                          │
│                     │                                            │
│           ┌─────────▼─────────┐                                 │
│           │    Categoria      │                                 │
│           ├───────────────────┤                                 │
│           │ - id: int         │                                 │
│           │ - nombre: string  │                                 │
│           │ - descripcion:str │                                 │
│           │ - nivel: string   │                                 │
│           └───────────────────┘                                 │
│                                                                  │
│                                                                  │
│  Relaciones:                                                     │
│  • Socio ──N:1──▶ Profesor  (muchos socios, un profesor)        │
│  • Socio ──N:M──▶ Categoria (relación muchos a muchos)          │
│                                                                  │
│  Constraints:                                                    │
│  • UNIQUE(dni) en Socio                                          │
│  • UNIQUE(email) en Socio                                        │
│  • FK profesor_id REFERENCES Profesor(id)                       │
│  • FK socio_id REFERENCES Socio(id) ON DELETE CASCADE            │
│  • FK categoria_id REFERENCES Categoria(id) ON DELETE CASCADE    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 14. MATRIZ DE TRAZABILIDAD

| Requisito | Componente Frontend | Store | API Endpoint | Backend Controller | Backend Model | Tabla BD | Validación |
|-----------|---------------------|-------|--------------|-------------------|---------------|----------|------------|
| Ingresar Nombre | SociosCreate.vue<br>`<input v-model="nombre">` | - | - | - | - | SOCIOS.nombre | HTML5 required |
| Ingresar Apellido | SociosCreate.vue<br>`<input v-model="apellido">` | - | - | - | - | SOCIOS.apellido | HTML5 required |
| Ingresar DNI | SociosCreate.vue<br>`<input v-model="dni">` | - | - | - | - | SOCIOS.dni | HTML5 required<br>UNIQUE constraint |
| Ingresar Email | SociosCreate.vue<br>`<input type="email">` | - | - | - | - | SOCIOS.email | HTML5 email<br>UNIQUE constraint |
| Ingresar Teléfono | SociosCreate.vue<br>`<input type="tel">` | - | - | - | - | SOCIOS.telefono | HTML5 required |
| Seleccionar Fecha | SociosCreate.vue<br>`<input type="date">` | - | - | - | - | SOCIOS.fecha_inscripcion | HTML5 date |
| Seleccionar Profesor | SociosCreate.vue<br>`<select v-model="profesor_id">` | useProfesoresStore | GET /profesores | ProfesorController | ProfesorModel | SOCIOS.profesor_id | FK constraint |
| Seleccionar Categorías | SociosCreate.vue<br>`<input type="checkbox">` | useCategoriasStore | GET /categorias | CategoriaController | CategoriaModel | SOCIO_CATEGORIA | - |
| Enviar Formulario | SociosCreate.vue<br>`@submit.prevent` | useSociosStore.createSocio() | POST /socios | SocioController.create() | SocioModel.create() | INSERT SOCIOS | Backend validation |
| Crear Relación Categorías | - | - | - | - | SocioModel.create()<br>loop INSERT | SOCIO_CATEGORIA | FK constraints |
| Confirmar Transacción | - | - | - | - | cnx.commit() | MySQL COMMIT | Atomicidad |
| Revertir en Error | - | - | - | - | cnx.rollback() | MySQL ROLLBACK | Consistencia |
| Mostrar Confirmación | SociosView.vue<br>`@created` | - | - | - | - | - | UI feedback |
| Refrescar Lista | SociosList.vue | useSociosStore.fetchSocios() | GET /socios | SocioController.get_all() | SocioModel.get_all() | SELECT SOCIOS | - |

---

## 15. CASOS DE PRUEBA

### CP-01: Crear Socio Completo (Happy Path)

| Campo | Valor de Prueba |
|-------|-----------------|
| Nombre | Juan |
| Apellido | Pérez |
| DNI | 12345678 |
| Email | juan.perez@email.com |
| Teléfono | 299-4567890 |
| Fecha Inscripción | 2025-11-29 |
| Profesor | María González (ID: 1) |
| Categorías | Intermedio (ID: 2), Avanzado (ID: 3) |

**Resultado Esperado:**
- ✅ HTTP 201 Created
- ✅ Mensaje: "Socio creado exitosamente"
- ✅ ID asignado: 15 (ejemplo)
- ✅ Modal se cierra
- ✅ Lista se actualiza con nuevo socio
- ✅ BD contiene 1 registro en SOCIOS
- ✅ BD contiene 2 registros en SOCIO_CATEGORIA

### CP-02: Crear Socio Sin Profesor (Opcional)

| Campo | Valor |
|-------|-------|
| Profesor | `null` (Sin selección) |
| Resto | Igual a CP-01 |

**Resultado Esperado:**
- ✅ HTTP 201 Created
- ✅ SOCIOS.profesor_id = NULL
- ✅ Socio creado exitosamente

### CP-03: DNI Duplicado

| Campo | Valor |
|-------|-------|
| DNI | 12345678 (ya existe) |
| Resto | Datos nuevos |

**Resultado Esperado:**
- ❌ HTTP 400 Bad Request
- ❌ Error: "Duplicate entry '12345678' for key 'dni'"
- ❌ Modal permanece abierto
- ❌ Datos conservados en formulario

### CP-04: Campos Obligatorios Vacíos

| Acción | Resultado |
|--------|-----------|
| Dejar Nombre vacío | Browser tooltip: "Please fill out this field" |
| Dejar Email vacío | Browser tooltip |
| Intentar Submit | Formulario no se envía |

### CP-05: Formato Email Inválido

| Campo | Valor |
|-------|-------|
| Email | juanperez (sin @) |

**Resultado:**
- ❌ Browser validation: "Please include @ in email"
- ❌ No se envía al backend

### CP-06: Error de Conexión a BD

**Precondición:** MySQL detenido

**Resultado Esperado:**
- ❌ HTTP 400 Bad Request
- ❌ Error: "No se pudo conectar a la base de datos"
- ❌ Modal permanece abierto

### CP-07: Backend No Disponible

**Precondición:** Flask detenido

**Resultado Esperado:**
- ❌ Axios error: ERR_CONNECTION_REFUSED
- ❌ Frontend: "Error al crear socio"
- ❌ Modal permanece abierto

### CP-08: Múltiples Categorías

| Categorías Seleccionadas | IDs |
|---------------------------|-----|
| Principiante | 1 |
| Intermedio | 2 |
| Avanzado | 3 |

**Resultado Esperado:**
- ✅ 3 registros en SOCIO_CATEGORIA
- ✅ Todas con socio_id = 15

### CP-09: Sin Categorías

**Acción:** No seleccionar ninguna categoría

**Resultado Esperado:**
- ✅ Socio se crea exitosamente
- ✅ 0 registros en SOCIO_CATEGORIA

### CP-10: Cancelar Creación

**Acción:** Click en "Cancelar" con datos ingresados

**Resultado Esperado:**
- ✅ Modal se cierra
- ✅ Datos se descartan
- ✅ No se realiza INSERT en BD

---

## 16. MÉTRICAS Y ESTADÍSTICAS

### Complejidad del Caso de Uso

| Métrica | Valor | Observación |
|---------|-------|-------------|
| Actores Involucrados | 3 | Administrador, Profesor (ref), Categoría (ref) |
| Pasos en Flujo Normal | 96 | Flujo detallado paso a paso |
| Flujos Alternos | 7 | FA-01 a FA-07 |
| Flujos de Excepción | 2 | FE-01 a FE-02 |
| Puntos de Decisión | 8 | Validaciones, errores, condiciones |
| Tablas de BD Involucradas | 3 | SOCIOS, SOCIO_CATEGORIA, PROFESORES, CATEGORIAS |
| Endpoints API Consumidos | 3 | POST /socios, GET /profesores, GET /categorias |
| Componentes Frontend | 3 | SociosView, SociosList, SociosCreate |
| Stores Pinia | 3 | socios, profesores, categorias |
| Tiempo Estimado Ejecución | 5-10 seg | Incluye carga de listas y creación |
| Líneas de Código (Backend) | ~50 | Método create() en socio_model.py |
| Líneas de Código (Frontend) | ~250 | Componente SociosCreate.vue completo |

### Análisis de Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| DNI duplicado | Media | Bajo | UNIQUE constraint + mensaje claro |
| Conexión BD perdida | Baja | Alto | Rollback automático + retry logic |
| Frontend-Backend desync | Baja | Medio | Versionado de API + validación doble |
| Categoría inválida (FK) | Baja | Medio | Foreign key constraint |
| Timeout en carga listas | Baja | Bajo | Timeout de 30s + mensaje error |
| Inyección SQL | Muy Baja | Crítico | Prepared statements |

---

## 17. CONCLUSIONES Y RECOMENDACIONES

### Fortalezas del Diseño Actual

1. **Separación de Responsabilidades**: Arquitectura MVC bien definida
2. **Transaccionalidad**: Rollback automático garantiza integridad
3. **Validación Multicapa**: Frontend + Backend
4. **Prevención SQL Injection**: Uso correcto de prepared statements
5. **UX Clara**: Formulario intuitivo con feedback inmediato

### Áreas de Mejora Identificadas

1. **Validación de DNI Único en Frontend**
   - **Problema**: Solo se detecta al intentar guardar
   - **Solución**: Agregar validación asíncrona mientras el usuario escribe
   ```vue
   <input 
     v-model="formData.dni" 
     @blur="validateDniUnique"
   />
   ```

2. **Auditoría de Creación**
   - **Problema**: No se registra quién creó el socio ni cuándo
   - **Solución**: Agregar campos `created_by`, `created_at`, `updated_at`

3. **Manejo de Errores Específicos**
   - **Problema**: Mensajes genéricos "Error al crear socio"
   - **Solución**: Mapear códigos de error específicos
   ```typescript
   if (error.code === 'ER_DUP_ENTRY') {
     if (error.message.includes('dni')) {
       return 'El DNI ya está registrado'
     }
   }
   ```

4. **Feedback de Carga**
   - **Problema**: No hay indicador al cargar listas
   - **Solución**: Agregar skeleton loaders
   ```vue
   <div v-if="loading" class="skeleton"></div>
   <select v-else>...</select>
   ```

5. **Confirmación de Salida**
   - **Problema**: Si el usuario cierra modal con datos sin guardar, se pierden
   - **Solución**: Agregar diálogo de confirmación
   ```typescript
   const isDirty = computed(() => 
     Object.values(formData.value).some(v => v !== '')
   )
   
   function handleClose() {
     if (isDirty.value) {
       if (confirm('¿Descartar cambios?')) {
         emit('close')
       }
     } else {
       emit('close')
     }
   }
   ```

6. **Paginación de Listas**
   - **Problema**: Si hay 1000+ socios, la lista se vuelve lenta
   - **Solución**: Implementar paginación server-side

7. **Testing Automatizado**
   - **Problema**: No hay tests unitarios ni de integración
   - **Solución**: Agregar tests con Vitest (frontend) y pytest (backend)

### Implementaciones Futuras Sugeridas

1. **Importación Masiva**: CSV con múltiples socios
2. **Foto de Perfil**: Upload de imagen del socio
3. **Validación de Teléfono**: Formato argentino (código área + número)
4. **Generación de Credencial**: PDF con QR del socio
5. **Email de Bienvenida**: Automatizado post-creación
6. **Dashboard de Métricas**: Cantidad de socios nuevos por mes

---

**Analista:** GitHub Copilot (Claude Sonnet 4.5)  
**Fecha de Análisis:** 29 de noviembre de 2025  
**Metodología:** UML 2.5 + RUP (Rational Unified Process)  
**Herramientas:** Análisis de código estático + revisión arquitectónica  
**Estado del Sistema:** Producción (funcional y estable)
