# Diagrama de Caso de Uso: Registrar Socio
## Sistema SiPePa - Sistema de Administración de Pelota a Paleta

---

## 1. DIAGRAMA PRINCIPAL DEL CASO DE USO

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        Sistema SiPePa - Módulo Socios                      │
│                                                                            │
│                                                                            │
│                         ┌──────────────────────────┐                       │
│                         │                          │                       │
│                         │   Registrar Socio        │                       │
│                         │      (CU-REG-01)         │                       │
│                         │                          │                       │
│                         └────────┬─────────────────┘                       │
│                                  │                                         │
│                                  │                                         │
│                                  │                                         │
│                         ┌────────┴─────────┐                               │
│                         │                  │                               │
│                         │   <<include>>    │                               │
│                         │                  │                               │
│           ┌─────────────┴──────┐   ┌──────┴──────────────┐                │
│           │                    │   │                     │                │
│           ▼                    │   ▼                     │                │
│   ┌──────────────────┐         │   ┌──────────────────┐  │                │
│   │  Validar Datos   │         │   │ Cargar Listas    │  │                │
│   │   Obligatorios   │         │   │   Auxiliares     │  │                │
│   │  (CU-REG-01.1)   │         │   │ (CU-REG-01.2)    │  │                │
│   └──────────────────┘         │   └──────────────────┘  │                │
│                                │                          │                │
│                                │   <<include>>            │                │
│                                │                          │                │
│                                ▼                          │                │
│                       ┌──────────────────┐                │                │
│                       │ Asignar Profesor │                │                │
│                       │  (CU-REG-01.3)   │                │                │
│                       └──────────────────┘                │                │
│                                │                          │                │
│                                │                          │                │
│                                │ <<extend>>               │                │
│                                │ [profesor != null]       │                │
│                                │                          │                │
│                                ▼                          │                │
│                       ┌──────────────────┐                │                │
│                       │    Asignar       │                │                │
│                       │   Categorías     │                │                │
│                       │ (CU-REG-01.4)    │                │                │
│                       └──────────────────┘                │                │
│                                │                          │                │
│                                │ <<extend>>               │                │
│                                │ [categorías.length > 0]  │                │
│                                │                          │                │
│                                ▼                          │                │
│                       ┌──────────────────┐                │                │
│                       │  Guardar en BD   │                │                │
│                       │ (CU-REG-01.5)    │                │                │
│                       └──────────────────┘                │                │
│                                │                          │                │
│                                │                          │                │
│                                │   <<include>>            │                │
│                                │                          │                │
│                                ▼                          │                │
│                       ┌──────────────────┐                │                │
│                       │ Confirmar        │                │                │
│                       │ Transacción      │                │                │
│                       │ (CU-REG-01.6)    │                │                │
│                       └──────────────────┘                │                │
│                                                                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
        │                                           │
        │                                           │
        │                                           │
        ▼                                           ▼
┌──────────────┐                            ┌──────────────┐
│              │                            │              │
│Administrador │                            │   Sistema    │
│   del Club   │                            │  Base Datos  │
│              │                            │              │
└──────────────┘                            └──────────────┘
  (Actor)                                      (Actor)
  Primario                                    Secundario
```

---

## 2. DIAGRAMA CON ACTORES Y RELACIONES EXTENDIDAS

```
                                ┌────────────────────────────────────────────┐
                                │         Sistema SiPePa                     │
                                │                                            │
                                │                                            │
                                │     ┌──────────────────────┐               │
                                │     │                      │               │
┌──────────────┐                │     │  Registrar Socio    │               │
│              │                │     │                      │               │
│ Administrador│───────────────────▶  │   (Goal Level)      │               │
│   del Club   │  usa            │     │                      │               │
│              │                │     └──────────┬───────────┘               │
└──────────────┘                │                │                           │
    Actor                       │                │                           │
   Principal                    │                │ <<include>>               │
                                │                │                           │
                                │                ▼                           │
                                │     ┌──────────────────────┐               │
                                │     │  Validar DNI Único   │               │
                                │     │                      │               │
┌──────────────┐                │     └──────────────────────┘               │
│              │                │                │                           │
│   Profesor   │ ─ ─ ─ ─ ─ ─ ─ ─│─ ─ ─ ─ ─ ─ ─ ─│─ ─ ─ ─ ─ ─                │
│  (datos de)  │  provee datos  │                │                           │
│              │                │                │ <<include>>               │
└──────────────┘                │                │                           │
    Actor                       │                ▼                           │
  Secundario                    │     ┌──────────────────────┐               │
   (referencia)                 │     │  Validar Email       │               │
                                │     │      Único           │               │
                                │     └──────────────────────┘               │
┌──────────────┐                │                │                           │
│              │                │                │                           │
│  Categoría   │ ─ ─ ─ ─ ─ ─ ─ ─│─ ─ ─ ─ ─ ─ ─ ─│─ ─ ─ ─ ─ ─                │
│  (datos de)  │  provee datos  │                │                           │
│              │                │                │ <<include>>               │
└──────────────┘                │                │                           │
    Actor                       │                ▼                           │
  Secundario                    │     ┌──────────────────────┐               │
   (referencia)                 │     │   Persistir en BD    │               │
                                │     │                      │               │
                                │     └──────────┬───────────┘               │
┌──────────────┐                │                │                           │
│              │                │                │                           │
│   Sistema    │◀────────────────────────────────┘                           │
│Base de Datos │  almacena      │                                            │
│              │                │                                            │
└──────────────┘                │                                            │
    Actor                       │                                            │
  Secundario                    │                                            │
   (sistema)                    └────────────────────────────────────────────┘
```

---

## 3. DIAGRAMA CON CASOS DE USO RELACIONADOS

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           Sistema SiPePa Completo                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                                                                              │
│   ┌──────────────────┐                 ┌──────────────────┐                 │
│   │  Gestionar       │◀───generalize───│  Registrar       │                 │
│   │  Socios          │                 │  Socio           │                 │
│   │                  │                 │                  │                 │
│   └────────┬─────────┘                 └────────┬─────────┘                 │
│            │                                    │                           │
│            │                                    │                           │
│            │                                    │                           │
│            │                        ┌───────────┴──────────┐                │
│            │                        │                      │                │
│            │                        ▼                      ▼                │
│            │             ┌──────────────────┐  ┌──────────────────┐         │
│            │             │   Actualizar     │  │   Eliminar       │         │
│            │             │   Socio          │  │   Socio          │         │
│            │             │                  │  │                  │         │
│            │             └──────────────────┘  └──────────────────┘         │
│            │                        │                      │                │
│            │                        │                      │                │
│            │                        └──────────┬───────────┘                │
│            │                                   │                            │
│            │                                   │                            │
│            │                                   │ <<include>>                │
│            │                                   │                            │
│            │                                   ▼                            │
│            │                        ┌──────────────────┐                    │
│            │                        │  Consultar       │                    │
│            │                        │  Socio           │                    │
│            │                        │                  │                    │
│            │                        └──────────────────┘                    │
│            │                                                                │
│            │                                                                │
│            │   Casos de Uso Dependientes (usan datos de Socio):            │
│            │                                                                │
│            ├────────────────────┐                                           │
│            │                    │                                           │
│            │                    ▼                                           │
│            │         ┌──────────────────┐                                   │
│            │         │  Registrar Pago  │                                   │
│            │         │                  │                                   │
│            │         └──────────────────┘                                   │
│            │                    │                                           │
│            │                    │ <<include>>                               │
│            │                    │ [requiere socio_id]                       │
│            │                    │                                           │
│            │         ┌──────────▼──────────┐                                │
│            │         │  Reservar Turno     │                                │
│            │         │                     │                                │
│            │         └─────────────────────┘                                │
│            │                    │                                           │
│            │                    │ <<include>>                               │
│            │                    │ [requiere socio_id]                       │
│            │                    │                                           │
│            │         ┌──────────▼──────────┐                                │
│            └────────▶│  Vender Pelotita    │                                │
│                      │                     │                                │
│                      └─────────────────────┘                                │
│                                 │                                           │
│                                 │ <<include>>                               │
│                                 │ [requiere socio_id]                       │
│                                 │                                           │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  │
                          ┌───────┴────────┐
                          │                │
                          │ Administrador  │
                          │                │
                          └────────────────┘
```

---

## 4. DIAGRAMA DETALLADO CON FLUJOS ALTERNOS

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Registrar Socio - Vista Detallada                       │
│                                                                            │
│                                                                            │
│                         ┌──────────────────────────┐                       │
│                         │                          │                       │
│                         │   Registrar Socio        │                       │
│                         │      (Principal)         │                       │
│                         │                          │                       │
│                         └────────┬─────────────────┘                       │
│                                  │                                         │
│                                  │                                         │
│                    ┌─────────────┼─────────────┐                           │
│                    │             │             │                           │
│                    │             │             │                           │
│          <<include>>│   <<include>>│   <<include>>│                         │
│                    │             │             │                           │
│                    ▼             ▼             ▼                           │
│         ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                │
│         │   Abrir      │ │   Cargar     │ │   Ingresar   │                │
│         │   Modal      │ │   Listas     │ │    Datos     │                │
│         └──────────────┘ └──────────────┘ └──────┬───────┘                │
│                                                   │                        │
│                                                   │                        │
│                                          <<include>>│                       │
│                                                   │                        │
│                                                   ▼                        │
│                                          ┌──────────────┐                  │
│                                          │   Validar    │                  │
│                                          │  Formulario  │                  │
│                                          └──────┬───────┘                  │
│                                                 │                          │
│                                                 │                          │
│                    ┌────────────────────────────┼──────────┐               │
│                    │                            │          │               │
│                    │                            │          │               │
│          [válido]  │                   [inválido]│         │ [cancelar]    │
│                    │                            │          │               │
│                    ▼                            ▼          ▼               │
│         ┌──────────────┐              ┌──────────────┐  ┌──────────────┐  │
│         │   Enviar     │              │   Mostrar    │  │   Cancelar   │  │
│         │   al Backend │              │   Errores    │  │   Creación   │  │
│         └──────┬───────┘              └──────────────┘  └──────────────┘  │
│                │                                                           │
│                │ <<include>>                                               │
│                │                                                           │
│                ▼                                                           │
│       ┌──────────────┐                                                     │
│       │  Guardar BD  │                                                     │
│       └──────┬───────┘                                                     │
│              │                                                             │
│              │                                                             │
│    ┌─────────┼──────────┐                                                 │
│    │         │          │                                                 │
│ [éxito]   [error]   [error DB]                                            │
│    │         │          │                                                 │
│    ▼         ▼          ▼                                                 │
│ ┌─────┐  ┌─────┐   ┌─────────┐                                            │
│ │OK   │  │Error│   │Rollback │                                            │
│ │201  │  │400  │   │         │                                            │
│ └──┬──┘  └──┬──┘   └────┬────┘                                            │
│    │        │           │                                                 │
│    │        └─────┬─────┘                                                 │
│    │              │                                                        │
│    │              │ <<extend>>                                             │
│    │              │                                                        │
│    │              ▼                                                        │
│    │     ┌──────────────┐                                                 │
│    │     │   Mostrar    │                                                 │
│    │     │   Mensaje    │                                                 │
│    │     │   Error      │                                                 │
│    │     └──────────────┘                                                 │
│    │                                                                       │
│    │ <<include>>                                                           │
│    │                                                                       │
│    ▼                                                                       │
│ ┌──────────────┐                                                           │
│ │   Cerrar     │                                                           │
│ │   Modal      │                                                           │
│ └──────┬───────┘                                                           │
│        │                                                                   │
│        │ <<include>>                                                       │
│        │                                                                   │
│        ▼                                                                   │
│ ┌──────────────┐                                                           │
│ │  Refrescar   │                                                           │
│ │   Lista      │                                                           │
│ └──────────────┘                                                           │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. DIAGRAMA CON PRECONDICIONES Y POSTCONDICIONES

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         Registrar Socio - Completo                         │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                      PRECONDICIONES                              │     │
│  ├──────────────────────────────────────────────────────────────────┤     │
│  │  ✓ Usuario autenticado como Administrador                       │     │
│  │  ✓ Sistema Backend operativo (Flask en puerto 5000)             │     │
│  │  ✓ Base de datos MySQL accesible                                │     │
│  │  ✓ Al menos 1 categoría registrada en el sistema                │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                  │                                        │
│                                  │                                        │
│                                  ▼                                        │
│              ┌────────────────────────────────────┐                        │
│              │                                    │                        │
│              │      REGISTRAR SOCIO               │                        │
│              │                                    │                        │
│              │  Flujo Principal:                  │                        │
│              │  1. Abrir formulario               │                        │
│              │  2. Cargar listas auxiliares       │                        │
│              │  3. Ingresar datos obligatorios    │                        │
│              │  4. Seleccionar profesor (opt)     │                        │
│              │  5. Seleccionar categorías (opt)   │                        │
│              │  6. Validar formulario             │                        │
│              │  7. Enviar POST /api/socios        │                        │
│              │  8. INSERT en tabla SOCIOS         │                        │
│              │  9. INSERT en SOCIO_CATEGORIA      │                        │
│              │  10. COMMIT transacción            │                        │
│              │  11. Retornar HTTP 201             │                        │
│              │  12. Cerrar modal                  │                        │
│              │  13. Refrescar lista               │                        │
│              │                                    │                        │
│              └────────────────┬───────────────────┘                        │
│                               │                                            │
│                               ▼                                            │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │                    POSTCONDICIONES DE ÉXITO                      │     │
│  ├──────────────────────────────────────────────────────────────────┤     │
│  │  ✓ Nuevo registro en tabla SOCIOS con ID auto-incremental       │     │
│  │  ✓ Relación establecida: socio ──▶ profesor (si asignado)       │     │
│  │  ✓ N registros en SOCIO_CATEGORIA (según selección)             │     │
│  │  ✓ Fecha de inscripción registrada                              │     │
│  │  ✓ Estado inicial = "Activo"                                    │     │
│  │  ✓ Socio puede reservar turnos                                  │     │
│  │  ✓ Socio puede realizar pagos                                   │     │
│  │  ✓ Socio puede comprar pelotitas                                │     │
│  │  ✓ Mensaje de confirmación mostrado                             │     │
│  │  ✓ Lista de socios actualizada                                  │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                            │
│                                                                            │
│                     POSTCONDICIONES DE FRACASO                             │
│                   (en caso de error o cancelación)                         │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │  ✗ No se crea registro en BD                                    │     │
│  │  ✗ No se crean registros huérfanos                              │     │
│  │  ✗ ROLLBACK automático si falla transacción                     │     │
│  │  ✗ Mensaje de error descriptivo mostrado                        │     │
│  │  ✗ Formulario conserva datos para reintento                     │     │
│  │  ✗ Integridad de base de datos mantenida                        │     │
│  └──────────────────────────────────────────────────────────────────┘     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. NOTACIÓN UML ESTÁNDAR - DIAGRAMA SIMPLIFICADO

```
                         ┌─────────────────┐
                         │  <<use case>>   │
                         │                 │
                         │ Registrar Socio │
                         │                 │
                         └────────┬────────┘
                                  │
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    │                           │
            <<include>>                   <<include>>
                    │                           │
                    │                           │
                    ▼                           ▼
        ┌───────────────────┐       ┌───────────────────┐
        │  <<use case>>     │       │  <<use case>>     │
        │                   │       │                   │
        │ Validar Datos     │       │ Persistir Socio   │
        │                   │       │                   │
        └───────────────────┘       └───────────────────┘




            ┌────────────┐
            │   Actor    │
            │            │
            │Administrador
            │            │
            └─────┬──────┘
                  │
                  │ usa
                  │
                  ▼
        (todos los casos de uso)
```

---

## 7. LEYENDA DE RELACIONES UML

```
┌──────────────────────────────────────────────────────────────────────┐
│                    TIPOS DE RELACIONES EN UML                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. ASOCIACIÓN (Actor ─────▶ Use Case)                              │
│     Actor                    Use Case                                │
│       ○                        (   )                                 │
│       │─────────────────────────▶│                                   │
│     "Actor invoca el caso de uso"                                    │
│                                                                      │
│                                                                      │
│  2. INCLUDE (──<<include>>──▶)                                       │
│     Use Case A              Use Case B                               │
│       (   )                   (   )                                  │
│         │────<<include>>────────▶│                                   │
│     "A siempre ejecuta B (obligatorio)"                              │
│                                                                      │
│                                                                      │
│  3. EXTEND (◀──<<extend>>──)                                         │
│     Use Case A              Use Case B                               │
│       (   )                   (   )                                  │
│         │◀────<<extend>>────────│                                    │
│                [condición]                                           │
│     "B extiende a A si se cumple condición (opcional)"               │
│                                                                      │
│                                                                      │
│  4. GENERALIZACIÓN (────────▶)                                       │
│     Use Case Específico     Use Case General                         │
│       (   )                   (   )                                  │
│         │──────────────────────▶│                                    │
│               (triángulo)                                            │
│     "Específico es un tipo de General (herencia)"                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 8. INTERPRETACIÓN DEL DIAGRAMA

### 8.1. Actor Principal
- **Administrador del Club**: Único actor que puede ejecutar el caso de uso
- Tiene permisos para crear, modificar y eliminar socios
- Accede a través de la interfaz web del sistema

### 8.2. Actores Secundarios
- **Profesor** (datos): Entidad referenciada, no ejecuta el caso de uso
- **Categoría** (datos): Entidad referenciada para clasificación
- **Sistema de Base de Datos**: Actor de sistema que almacena datos

### 8.3. Relaciones <<include>>
Indican sub-casos de uso que **SIEMPRE** se ejecutan:

1. **Validar Datos Obligatorios**: Siempre se valida nombre, apellido, DNI, email, teléfono
2. **Cargar Listas Auxiliares**: Siempre se cargan profesores y categorías disponibles
3. **Guardar en BD**: Siempre se intenta persistir si pasa validaciones
4. **Confirmar Transacción**: Siempre se hace COMMIT o ROLLBACK

### 8.4. Relaciones <<extend>>
Indican sub-casos de uso que **OPCIONALMENTE** se ejecutan:

1. **Asignar Profesor**: Solo si el administrador selecciona un profesor
   - Condición: `profesor_id != null`
   
2. **Asignar Categorías**: Solo si se seleccionan categorías
   - Condición: `categorias.length > 0`

### 8.5. Flujos Alternos Representados
- **Cancelar Creación**: Sale del flujo principal sin guardar
- **Error de Validación**: Muestra errores y permite corrección
- **DNI Duplicado**: Detecta constraint violation y muestra mensaje
- **Error de BD**: Ejecuta rollback y notifica

---

## 9. CASOS DE USO RELACIONADOS (ECOSISTEMA)

### Dependencias Upstream (se ejecutan antes)
- **Autenticar Usuario**: Debe ejecutarse antes para verificar permisos
- **Gestionar Profesores**: Deben existir profesores para asignar
- **Gestionar Categorías**: Deben existir categorías para clasificar

### Dependencias Downstream (usan este caso de uso)
- **Actualizar Socio**: Modifica un socio existente
- **Consultar Socio**: Lee datos de socios registrados
- **Registrar Pago**: Requiere socio_id del socio registrado
- **Reservar Turno**: Requiere socio_id para asignar reserva
- **Vender Pelotita**: Puede venderse a un socio registrado

---

## 10. CARDINALIDAD DE RELACIONES

```
Administrador  1 ────────▶ * Registrar Socio
(un admin puede registrar múltiples socios)

Registrar Socio  1 ────────▶ 0..1 Profesor
(un socio puede tener 0 o 1 profesor)

Registrar Socio  1 ────────▶ 0..* Categoría
(un socio puede tener 0 o múltiples categorías)

Registrar Socio  * ────────▶ 1 Sistema BD
(múltiples registros usan el mismo sistema de BD)
```

---

## 11. DIAGRAMA EN NOTACIÓN IDEF0 (Alternativa)

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                        Control (Reglas de Negocio)                 │
│                    ┌─────────────────────────────┐                 │
│                    │ - DNI único                 │                 │
│                    │ - Email único               │                 │
│                    │ - Campos obligatorios       │                 │
│                    │ - Profesor opcional         │                 │
│                    └──────────────┬──────────────┘                 │
│                                   │                                │
│                                   ▼                                │
│   Inputs                ┌─────────────────┐              Outputs  │
│  ─────────────────────▶ │                 │ ─────────────────────▶│
│                         │   REGISTRAR     │                        │
│  • Datos personales     │     SOCIO       │  • ID socio generado   │
│  • Profesor (opcional)  │                 │  • Registro en BD      │
│  • Categorías (opcionales)│   (A0)        │  • Confirmación        │
│                         │                 │  • Lista actualizada   │
│  ─────────────────────▶ └─────────────────┘ ─────────────────────▶│
│                                   ▲                                │
│                                   │                                │
│                        Mecanismos (Recursos)                       │
│                    ┌──────────────┴──────────────┐                 │
│                    │ - Administrador             │                 │
│                    │ - Sistema Web (Vue + Flask) │                 │
│                    │ - Base de datos MySQL       │                 │
│                    └─────────────────────────────┘                 │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 12. PUNTOS DE EXTENSIÓN DEL CASO DE USO

| Punto de Extensión | Ubicación en el Flujo | Condición | Caso de Uso que Extiende |
|--------------------|----------------------|-----------|---------------------------|
| Validación Adicional | Después de validación básica | DNI formato inválido | Validar Formato DNI |
| Duplicación de Email | Antes de guardar | Email ya existe | Notificar Email Duplicado |
| Asignación de Nivel | Después de crear socio | Categorías seleccionadas | Calcular Nivel Promedio |
| Generación de Credencial | Después de crear socio | Creación exitosa | Generar Credencial PDF |
| Envío de Bienvenida | Después de crear socio | Email válido | Enviar Email Bienvenida |
| Auditoría | En cualquier momento | Operación crítica | Registrar Auditoría |

---

**Analista:** GitHub Copilot (Claude Sonnet 4.5)  
**Fecha:** 29 de noviembre de 2025  
**Estándar:** UML 2.5 - Use Case Diagrams  
**Herramienta:** Diagramas ASCII con notación estándar  
**Referencia:** OMG UML Specification + Jacobson - Use Case Modeling
