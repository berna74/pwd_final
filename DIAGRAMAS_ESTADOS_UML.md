# Diagramas de Estados UML - Sistema SiPePa
## Sistema de Administración de Pelota a Paleta del Club Sol de Mayo

---

## Introducción

Los **Diagramas de Estados** (State Machine Diagrams) en UML modelan el comportamiento dinámico de un objeto a lo largo de su ciclo de vida, mostrando:

- **Estados**: Condiciones o situaciones en las que puede encontrarse un objeto
- **Transiciones**: Cambios entre estados provocados por eventos
- **Eventos**: Acciones que disparan transiciones
- **Acciones**: Operaciones ejecutadas durante transiciones o dentro de estados
- **Guardas**: Condiciones que deben cumplirse para que ocurra una transición

Este documento presenta los diagramas de estados para las **5 entidades principales** del sistema SiPePa que presentan comportamiento dinámico significativo.

---

# 1. DIAGRAMA DE ESTADOS: TURNO

## 1.1. Descripción General

Un **Turno** representa la reserva de una cancha en un horario específico. Durante su ciclo de vida, un turno pasa por varios estados desde su disponibilidad inicial hasta su finalización o cancelación.

## 1.2. Estados Identificados

| Estado | Descripción | Condición de Permanencia |
|--------|-------------|--------------------------|
| **Disponible** | La cancha está libre y puede ser reservada | No hay socio asignado |
| **Reservado** | Un socio ha reservado el turno | Turno confirmado y fecha futura |
| **En Curso** | El turno está siendo utilizado actualmente | Hora actual entre hora_inicio y hora_fin |
| **Completado** | El turno finalizó normalmente | Hora actual > hora_fin |
| **Cancelado** | La reserva fue cancelada antes de su ejecución | Cancelación por administrador o socio |
| **No Presentado** | El socio no se presentó a su turno | Pasó hora_inicio sin check-in |

## 1.3. Eventos y Transiciones

| Evento | Descripción | Parámetros |
|--------|-------------|------------|
| `reservar(socio_id, jugadores[])` | Un socio reserva el turno | ID del socio, lista de jugadores |
| `confirmar()` | Se confirma la reserva | - |
| `iniciar()` | Comienza el horario del turno | - |
| `finalizar()` | Termina el horario del turno | - |
| `cancelar(motivo)` | Se cancela la reserva | Razón de cancelación |
| `marcarNoPresento()` | Se marca ausencia del socio | - |

## 1.4. Diagrama de Estados

```
                           ┌──────────────────┐
                           │  Estado Inicial  │
                           │       ●          │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                   ┌──────▶│   Disponible     │◀──────┐
                   │       ├──────────────────┤       │
                   │       │ entry: marcar    │       │
                   │       │   como libre     │       │
                   │       └────────┬─────────┘       │
                   │                │                  │
                   │                │ reservar(socio_id, jugadores[])
                   │                │ [cancha disponible && socio activo]
                   │                │                  │
                   │                ▼                  │
                   │       ┌──────────────────┐       │
                   │       │    Reservado     │       │
                   │       ├──────────────────┤       │
                   │       │ entry: asignar   │       │
                   │       │   socio y fecha  │       │
                   │       │ do: notificar    │       │
                   │       │   confirmación   │       │
                   │       └────┬───────┬─────┘       │
                   │            │       │             │
                   │  cancelar()│       │ [hora_actual >= hora_inicio]
            [antes │   [antes   │       │   iniciar()
             del   │   del      │       │             │
            turno] │   turno]   │       │             │
                   │            │       ▼             │
                   │            │  ┌──────────────────┐
                   │            │  │    En Curso      │
                   │            │  ├──────────────────┤
                   │            │  │ entry: marcar    │
                   │            │  │   en uso         │
                   │            │  │ do: cronometrar  │
                   │            │  └────────┬─────────┘
                   │            │           │
                   │            │           │ finalizar()
                   │            │           │ [hora_actual >= hora_fin]
                   │            │           │
                   │            │           ▼
                   │            │  ┌──────────────────┐
                   │            │  │   Completado     │◀──────┐
                   │            │  ├──────────────────┤       │
                   │            │  │ entry: liberar   │       │
                   │            │  │   cancha         │       │
                   │            │  │ do: calcular     │       │
                   │            │  │   estadísticas   │       │
                   │            │  └──────────────────┘       │
                   │            │           │                 │
                   │            ▼           │                 │
                   │   ┌──────────────────┐ │                 │
                   └──▶│    Cancelado     │ │                 │
                       ├──────────────────┤ │                 │
                       │ entry: liberar   │ │                 │
                       │   cancha         │ │                 │
                       │ do: notificar    │ │                 │
                       │   cancelación    │ │                 │
                       └──────────────────┘ │                 │
                                │           │                 │
                                │           │                 │
                                │ [hora_actual > hora_inicio  │
                                │  && !check_in]              │
                                │ marcarNoPresento()          │
                                │           │                 │
                                ▼           │                 │
                       ┌──────────────────┐ │                 │
                       │  No Presentado   │─┘                 │
                       ├──────────────────┤                   │
                       │ entry: registrar │                   │
                       │   ausencia       │                   │
                       │ do: penalizar    │                   │
                       │   socio          │                   │
                       └────────┬─────────┘                   │
                                │                             │
                                │ [después de 30 días]        │
                                │ archivar()                  │
                                │                             │
                                └─────────────────────────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │  Estado Final    │
                                     │       ◉          │
                                     └──────────────────┘
```

## 1.5. Tabla de Transiciones

| Estado Origen | Evento | Guarda | Estado Destino | Acción |
|---------------|--------|--------|----------------|--------|
| Disponible | reservar() | cancha disponible && socio activo | Reservado | asignar_socio(), notificar_confirmacion() |
| Reservado | iniciar() | hora_actual >= hora_inicio | En Curso | marcar_en_uso(), iniciar_cronometro() |
| Reservado | cancelar() | antes del turno | Cancelado | liberar_cancha(), notificar_cancelacion() |
| En Curso | finalizar() | hora_actual >= hora_fin | Completado | liberar_cancha(), calcular_estadisticas() |
| Reservado | marcarNoPresento() | hora_actual > hora_inicio && !check_in | No Presentado | registrar_ausencia(), penalizar_socio() |
| Cancelado | - | después de 30 días | [Final] | archivar() |
| Completado | - | después de 30 días | [Final] | archivar() |
| No Presentado | - | después de 30 días | [Final] | archivar() |

## 1.6. Actividades en Estados

### Estado: Reservado
```
entry / asignar_socio_y_fecha()
do / 
  - verificar_disponibilidad_continua()
  - enviar_recordatorio(24h_antes)
  - enviar_recordatorio(1h_antes)
exit / registrar_inicio_o_cancelacion()
```

### Estado: En Curso
```
entry / marcar_cancha_en_uso()
do /
  - cronometrar_tiempo_uso()
  - monitorear_tiempo_extra()
exit / liberar_cancha()
```

### Estado: Completado
```
entry / 
  - liberar_cancha()
  - calcular_tiempo_real_uso()
do /
  - generar_estadisticas()
  - actualizar_historial_socio()
exit / archivar_registro()
```

---

# 2. DIAGRAMA DE ESTADOS: PAGO

## 2.1. Descripción General

Un **Pago** representa una transacción financiera en el club. Su estado refleja el proceso desde el registro inicial hasta la confirmación contable y posible conciliación.

## 2.2. Estados Identificados

| Estado | Descripción | Condición de Permanencia |
|--------|-------------|--------------------------|
| **Pendiente** | Pago registrado pero no confirmado | Esperando confirmación bancaria |
| **Confirmado** | Pago verificado y acreditado | Transacción exitosa |
| **En Revisión** | Pago con inconsistencias que requieren verificación | Diferencias en montos o datos |
| **Rechazado** | Pago no pudo procesarse | Fondos insuficientes, error bancario |
| **Conciliado** | Pago verificado contra extracto bancario | Parte de cierre contable mensual |
| **Anulado** | Pago cancelado o revertido | Devolución procesada |

## 2.3. Diagrama de Estados

```
                           ┌──────────────────┐
                           │  Estado Inicial  │
                           │       ●          │
                           └────────┬─────────┘
                                    │
                                    │ registrar(tipo, monto, pagador)
                                    │
                                    ▼
                   ┌────────────────────────────┐
                   │       Pendiente            │
                   ├────────────────────────────┤
                   │ entry: guardar_en_BD()     │
          ┌───────▶│ do: esperar_confirmacion() │◀────────┐
          │        └────┬─────────┬──────────────┘         │
          │             │         │                        │
          │             │         │ [método = efectivo]    │
          │             │         │ confirmar_efectivo()   │
          │             │         │                        │
          │   rechazar()│         │                        │
          │   [error]   │         ▼                        │
          │             │  ┌──────────────────┐            │
          │             │  │   Confirmado     │            │
          │             │  ├──────────────────┤            │
          │             │  │ entry: marcar    │            │
          │             │  │   pagado         │            │
          │             │  │ do: actualizar   │            │
          │             │  │   saldo_socio    │            │
          │             │  └─────┬────────────┘            │
          │             │        │                         │
          │             │        │ solicitar_revision()    │
          │             │        │ [inconsistencia]        │
          │             │        │                         │
          │             │        ▼                         │
          │             │  ┌──────────────────┐            │
          │             │  │   En Revisión    │            │
          │             │  ├──────────────────┤            │
          │             │  │ entry: bloquear  │            │
          │             │  │ do: investigar   │            │
          │             │  └─────┬──────┬─────┘            │
          │             │        │      │                  │
          │             │        │      │ aprobar()        │
          │             │        │      │ [verificado]     │
          │             │        │      └──────────────────┘
          │             │        │
          │             │        │ rechazar()
          │             │        │ [no verificable]
          │             │        │
          │             ▼        ▼
          │        ┌────────────────────┐
          └───────▶│    Rechazado       │
                   ├────────────────────┤
                   │ entry: revertir    │
                   │   operaciones      │
                   │ do: notificar      │
                   │   rechazo          │
                   └────────┬───────────┘
                            │
                            │ anular()
                            │
                            ▼
                   ┌────────────────────┐
                   │     Anulado        │
                   ├────────────────────┤
                   │ entry: generar     │
                   │   nota_credito     │
                   │ do: devolver_monto │
                   └────────────────────┘
                            │
                            │
      ┌─────────────────────┴─────────────────────┐
      │                                            │
      │ [fin de mes]                               │
      │ conciliar()                                │
      │                                            │
      ▼                                            │
┌────────────────────┐                             │
│   Conciliado       │                             │
├────────────────────┤                             │
│ entry: marcar_como │                             │
│   conciliado       │                             │
│ do: incluir_en     │                             │
│   reporte_mensual  │                             │
└────────┬───────────┘                             │
         │                                          │
         │ [después de 5 años]                      │
         │ archivar()                               │
         │                                          │
         └──────────────────────────────────────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │  Estado Final    │
                   │       ◉          │
                   └──────────────────┘
```

## 2.4. Matriz de Transiciones con Guardas

| Origen | Evento | Guarda | Destino | Acción |
|--------|--------|--------|---------|--------|
| Pendiente | confirmar_efectivo() | método = "efectivo" | Confirmado | marcar_pagado(), actualizar_saldo() |
| Pendiente | confirmar_transferencia() | método = "transferencia" && comprobante_valido | Confirmado | marcar_pagado(), vincular_comprobante() |
| Pendiente | rechazar() | error_validacion | Rechazado | revertir_operaciones(), notificar() |
| Confirmado | solicitar_revision() | inconsistencia_detectada | En Revisión | bloquear(), iniciar_investigacion() |
| Confirmado | conciliar() | fin_de_mes && extracto_coincide | Conciliado | marcar_conciliado(), incluir_reporte() |
| En Revisión | aprobar() | verificacion_exitosa | Confirmado | desbloquear(), confirmar_definitivo() |
| En Revisión | rechazar() | verificacion_fallida | Rechazado | revertir(), notificar_error() |
| Confirmado | anular() | solicitud_devolucion && plazo_valido | Anulado | generar_nota_credito(), devolver() |
| Rechazado | anular() | requiere_registro_formal | Anulado | formalizar_rechazo() |

---

# 3. DIAGRAMA DE ESTADOS: SOCIO/ALUMNO

## 3.1. Descripción General

Tanto **Socios** como **Alumnos** comparten un ciclo de vida similar en el sistema, pasando por estados de actividad desde su inscripción hasta su eventual baja.

## 3.2. Estados Identificados

| Estado | Descripción | Condición de Permanencia |
|--------|-------------|--------------------------|
| **Inscripto** | Recién registrado en el sistema | Datos completos, pago inicial pendiente |
| **Activo** | Usuario con cuota al día | Pagos actualizados |
| **Moroso** | Usuario con cuota vencida | Atraso en pagos |
| **Suspendido** | Usuario temporalmente inhabilitado | Acumulación de deuda o falta grave |
| **Inactivo** | Usuario dado de baja | Renuncia o baja administrativa |
| **Reingreso** | Ex-usuario solicitando reactivación | Estado transitorio |

## 3.3. Diagrama de Estados

```
                           ┌──────────────────┐
                           │  Estado Inicial  │
                           │       ●          │
                           └────────┬─────────┘
                                    │
                                    │ inscribir(datos_personales)
                                    │
                                    ▼
                           ┌──────────────────┐
                           │   Inscripto      │
                           ├──────────────────┤
                           │ entry: crear     │
                           │   registro       │
                           │ do: solicitar    │
                           │   pago_inicial   │
                           └────────┬─────────┘
                                    │
                                    │ pagar_inscripcion()
                                    │ [pago confirmado]
                                    │
                                    ▼
                   ┌────────────────────────────┐
          ┌───────▶│        Activo              │◀────────┐
          │        ├────────────────────────────┤         │
          │        │ entry: habilitar_servicios │         │
          │        │ do: monitorear_cuotas      │         │
          │        └────┬─────────┬─────────────┘         │
          │             │         │                       │
          │             │         │ [cuota vencida]       │
          │             │         │ vencer_cuota()        │
          │             │         │                       │
          │ pagar_cuota()         │                       │
          │ [deuda <= 1 mes]      ▼                       │
          │             │  ┌──────────────────┐           │
          │             │  │     Moroso       │           │
          │             │  ├──────────────────┤           │
          │             │  │ entry: enviar    │           │
          │             │  │   notificacion   │           │
          │             │  │ do: acumular     │           │
          │             │  │   recargos       │           │
          │             │  └─────┬──────┬─────┘           │
          │             │        │      │                 │
          │             │        │      │ [deuda > 3 meses]
          │             │        │      │ suspender()     │
          │             │        │      │                 │
          └─────────────┘        │      ▼                 │
                                 │  ┌──────────────────┐  │
                 pagar_cuota()   │  │   Suspendido     │  │
                 [pago total]    │  ├──────────────────┤  │
                                 │  │ entry: bloquear  │  │
                                 │  │   servicios      │  │
                                 │  │ do: notificar    │  │
                                 │  │   suspension     │  │
                                 │  └─────┬──────┬─────┘  │
                                 │        │      │        │
                                 │        │      │ dar_baja()
                                 │        │      │ [renuncia || 
                                 │        │      │  6 meses sin pago]
                 pagar_deuda()   │        │      │        │
                 [pago completo] │        │      │        │
                                 │        │      │        │
                                 └────────┘      │        │
                                          │      │        │
                                          │      ▼        │
                                          │  ┌──────────────────┐
                                          │  │    Inactivo      │
                                          │  ├──────────────────┤
                                          │  │ entry: archivar  │
                                          │  │   historial      │
                                          │  │ do: deshabilitar │
                                          │  │   accesos        │
                                          │  └─────┬──────┬─────┘
                                          │        │      │
                                          │        │      │ [permanente]
                                          │        │      │
                  solicitar_reingreso()   │        │      ▼
                  [dentro de 1 año]       │        │  ┌──────────────────┐
                                          │        │  │  Estado Final    │
                                          │        │  │       ◉          │
                                          │        │  └──────────────────┘
                                          │        │
                                          │        ▼
                                          │  ┌──────────────────┐
                                          └─▶│    Reingreso     │
                                             ├──────────────────┤
                                             │ entry: validar   │
                                             │   datos          │
                                             │ do: verificar    │
                                             │   deudas_previas │
                                             └────────┬─────────┘
                                                      │
                                                      │ aprobar_reingreso()
                                                      │ [deudas saldadas]
                                                      │
                                                      └─────────────────────┐
```

## 3.4. Reglas de Negocio en Estados

### Estado: Activo
```
Invariantes:
  - cuota al día (atraso <= 10 días)
  - puede reservar turnos
  - puede comprar pelotitas
  - puede participar en torneos

Condiciones de Salida:
  - cuota vencida > 10 días → Moroso
  - solicitud de baja → Inactivo
```

### Estado: Moroso
```
Invariantes:
  - deuda acumulada > 0
  - recargos aplicados según tabla
  - notificaciones enviadas semanalmente
  - acceso restringido (solo pagar cuotas)

Condiciones de Salida:
  - pago total → Activo
  - deuda > 3 meses → Suspendido
```

### Estado: Suspendido
```
Invariantes:
  - servicios completamente bloqueados
  - no puede reservar turnos
  - no puede participar en actividades
  - deuda congelada (sin más recargos)

Condiciones de Salida:
  - pago completo → Activo
  - 6 meses sin pago → Inactivo
```

---

# 4. DIAGRAMA DE ESTADOS: PELOTITA (INVENTARIO)

## 4.1. Descripción General

Una **Pelotita** en el inventario puede estar en diferentes estados dependiendo de su ubicación física y disponibilidad para venta.

## 4.2. Estados Identificados

| Estado | Descripción |
|--------|-------------|
| **En Tránsito** | Pelotitas pedidas al proveedor, aún no recibidas |
| **En Stock** | Pelotitas disponibles para venta |
| **Reservada** | Pelotita apartada para un cliente |
| **Vendida** | Pelotita vendida y entregada |
| **Defectuosa** | Pelotita con defectos de fabricación |

## 4.3. Diagrama de Estados

```
                           ┌──────────────────┐
                           │  Estado Inicial  │
                           │       ●          │
                           └────────┬─────────┘
                                    │
                                    │ realizar_pedido(proveedor, cantidad)
                                    │
                                    ▼
                           ┌──────────────────┐
                           │   En Tránsito    │
                           ├──────────────────┤
                           │ entry: registrar │
                           │   compra         │
                           │ do: rastrear     │
                           │   envío          │
                           └────────┬─────────┘
                                    │
                                    │ recibir_pedido()
                                    │ [inspección OK]
                                    │
                                    ▼
                   ┌────────────────────────────┐
          ┌───────▶│      En Stock              │◀───────┐
          │        ├────────────────────────────┤        │
          │        │ entry: actualizar_stock    │        │
          │        │ do: disponible_para_venta  │        │
          │        └────┬───────────┬───────────┘        │
          │             │           │                    │
          │             │           │ reservar(cliente)  │
          │             │           │                    │
          │             │           ▼                    │
          │             │   ┌──────────────────┐         │
          │             │   │    Reservada     │         │
          │             │   ├──────────────────┤         │
          │             │   │ entry: apartar   │         │
          │             │   │ do: esperar_pago │         │
          │             │   │   (24h límite)   │         │
          │             │   └────┬──────┬──────┘         │
          │             │        │      │                │
          │  cancelar_reserva()  │      │ pagar()        │
          │  [timeout || cliente]│      │ [pago OK]      │
          │             │        │      │                │
          └─────────────┘        │      ▼                │
                                 │  ┌──────────────────┐ │
          detectar_defecto()     │  │     Vendida      │ │
          [en inspección]        │  ├──────────────────┤ │
                                 │  │ entry: registrar │ │
                                 │  │   venta          │ │
                                 │  │ do: actualizar   │ │
                                 │  │   stock          │ │
                                 │  │ exit: generar    │ │
                                 │  │   comprobante    │ │
                                 │  └──────────────────┘ │
                                 │          │            │
                                 │          │ [garantía 7 días]
                                 │          │ reportar_defecto()
                                 ▼          │            │
                        ┌──────────────────┐│            │
                        │   Defectuosa     │◀────────────┘
                        ├──────────────────┤
                        │ entry: retirar   │
                        │   de_stock       │
                        │ do: solicitar    │
                        │   devolucion     │
                        └────────┬─────────┘
                                 │
                                 │ devolver_proveedor()
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Estado Final    │
                        │       ◉          │
                        └──────────────────┘
```

## 4.4. Actividades en Estado "En Stock"

```
Estado: En Stock
  entry / 
    - actualizar_cantidad_disponible()
    - calcular_precio_venta()
    - etiquetar_pelotitas()
  
  do /
    - monitorear_nivel_stock()
    - verificar_rotacion()
    - if (stock < minimo_requerido):
        generar_alerta_reposicion()
    - verificar_fecha_vencimiento() // si aplica
  
  exit /
    - decrementar_stock()
    - registrar_movimiento()
```

---

# 5. DIAGRAMA DE ESTADOS COMPUESTO: PROCESO DE RESERVA Y PAGO

## 5.1. Descripción General

Este diagrama muestra la **composición de estados** para el proceso completo de reserva de turno con pago de abono, demostrando cómo los estados de diferentes entidades se coordinan.

## 5.2. Diagrama de Estados Compuesto

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  PROCESO: Reserva de Turno con Pago                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  REGIÓN: Gestión de Turno                                           │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │   [Inicial]                                                          │   │
│  │      │                                                               │   │
│  │      ▼                                                               │   │
│  │  ┌──────────────┐                                                    │   │
│  │  │ Disponible   │                                                    │   │
│  │  └──────┬───────┘                                                    │   │
│  │         │ reservar()                                                 │   │
│  │         ▼                                                            │   │
│  │  ┌──────────────┐                                                    │   │
│  │  │ Reservado    │────────┐                                          │   │
│  │  └──────────────┘        │ [pago_confirmado]                        │   │
│  │                          │                                           │   │
│  └──────────────────────────┼───────────────────────────────────────────┘   │
│                             │                                               │
│                             │ fork                                          │
│                             │                                               │
│         ┌───────────────────┴───────────────────┐                           │
│         │                                       │                           │
│         ▼                                       ▼                           │
│  ┌─────────────────────────────┐   ┌─────────────────────────────┐         │
│  │  REGIÓN: Proceso de Pago    │   │  REGIÓN: Notificaciones     │         │
│  ├─────────────────────────────┤   ├─────────────────────────────┤         │
│  │                             │   │                             │         │
│  │  [Inicial]                  │   │  [Inicial]                  │         │
│  │      │                      │   │      │                      │         │
│  │      ▼                      │   │      ▼                      │         │
│  │  ┌──────────┐               │   │  ┌──────────────┐           │         │
│  │  │Pendiente │               │   │  │ Preparando   │           │         │
│  │  └────┬─────┘               │   │  │ Mensaje      │           │         │
│  │       │ validar()           │   │  └──────┬───────┘           │         │
│  │       ▼                     │   │         │                   │         │
│  │  ┌──────────┐               │   │         ▼                   │         │
│  │  │Confirmado│───────────────┼───┼──▶ ┌──────────┐             │         │
│  │  └──────────┘               │   │    │ Enviando │             │         │
│  │       │                     │   │    └────┬─────┘             │         │
│  │       │                     │   │         │                   │         │
│  │       ▼                     │   │         ▼                   │         │
│  │  ┌──────────┐               │   │    ┌──────────┐             │         │
│  │  │Conciliado│               │   │    │ Enviado  │             │         │
│  │  └──────────┘               │   │    └──────────┘             │         │
│  │       │                     │   │         │                   │         │
│  └───────┼─────────────────────┘   └─────────┼───────────────────┘         │
│          │                                   │                             │
│          └───────────────┬───────────────────┘                             │
│                          │ join                                            │
│                          │                                                 │
│                          ▼                                                 │
│                  ┌──────────────┐                                          │
│                  │ Turno        │                                          │
│                  │ Confirmado   │                                          │
│                  │ Totalmente   │                                          │
│                  └──────────────┘                                          │
│                          │                                                 │
│                          ▼                                                 │
│                      [Final]                                               │
│                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 6. ANÁLISIS AVANZADO: ESTADOS ORTOGONALES

## 6.1. Descripción

Los **estados ortogonales** (o concurrentes) permiten que un objeto esté en múltiples estados simultáneamente en diferentes regiones independientes. En SiPePa, esto aplica a entidades complejas.

## 6.2. Ejemplo: Socio con Estados Ortogonales

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ENTIDAD: Socio                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────┬─────────────────────────────────┐ │
│  │  REGIÓN: Estado Administrativo       │  REGIÓN: Estado de Pago         │ │
│  ├─────────────────────────────────────┼─────────────────────────────────┤ │
│  │                                      │                                 │ │
│  │  ┌──────────┐                        │  ┌──────────┐                   │ │
│  │  │ Activo   │◀────┐                  │  │ Al Día   │◀────┐             │ │
│  │  └────┬─────┘     │                  │  └────┬─────┘     │             │ │
│  │       │           │                  │       │           │             │ │
│  │       ▼           │                  │       ▼           │             │ │
│  │  ┌──────────┐     │                  │  ┌──────────┐     │             │ │
│  │  │Suspendido│─────┘                  │  │ Moroso   │─────┘             │ │
│  │  └──────────┘                        │  └──────────┘                   │ │
│  │                                      │                                 │ │
│  └─────────────────────────────────────┴─────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  REGIÓN: Estado de Categoría                                          │ │
│  ├───────────────────────────────────────────────────────────────────────┤ │
│  │                                                                        │ │
│  │  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     │ │
│  │  │Principiante  │  │Intermedio│  │ Avanzado │  │ Profesional      │ │
│  │  └────┬─────┘     └────┬─────┘     └────┬─────┘     └──────────┘     │ │
│  │       │ ascender()     │ ascender()     │ ascender()                 │ │
│  │       └────────────────┴────────────────┘                            │ │
│  │                                                                        │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  Ejemplos de Estados Combinados:                                           │
│  - (Activo, Al Día, Intermedio)                                            │
│  - (Activo, Moroso, Principiante)                                          │
│  - (Suspendido, Moroso, Avanzado)                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6.3. Interpretación de Estados Combinados

| Estado Administrativo | Estado de Pago | Estado de Categoría | Acciones Permitidas |
|----------------------|----------------|---------------------|---------------------|
| Activo | Al Día | Principiante | Reservar turnos nivel básico, participar clases, comprar pelotitas |
| Activo | Moroso | Intermedio | Solo pagar deuda, no puede reservar turnos |
| Suspendido | Moroso | Avanzado | Ninguna acción hasta regularización |
| Activo | Al Día | Profesional | Todas las acciones + torneos profesionales |

---

# 7. TABLA COMPARATIVA DE COMPLEJIDAD

| Entidad | Cantidad de Estados | Cantidad de Transiciones | Complejidad | Estados Compuestos |
|---------|---------------------|--------------------------|-------------|-------------------|
| Turno | 6 | 10 | Alta | No |
| Pago | 6 | 12 | Alta | No |
| Socio/Alumno | 6 | 9 | Media-Alta | Sí (ortogonales) |
| Pelotita | 5 | 8 | Media | No |
| Proceso Reserva+Pago | 3 regiones | 15 | Muy Alta | Sí (compuesto) |

---

# 8. PATRONES DE DISEÑO IDENTIFICADOS

## 8.1. Patrón State

El sistema implementa el **Patrón State** de forma implícita en varias entidades:

```typescript
interface TurnoState {
  reservar(): void
  cancelar(): void
  iniciar(): void
  finalizar(): void
}

class DisponibleState implements TurnoState {
  reservar() { /* transición a Reservado */ }
  cancelar() { throw new Error("No se puede cancelar") }
  iniciar() { throw new Error("No se puede iniciar") }
  finalizar() { throw new Error("No se puede finalizar") }
}

class ReservadoState implements TurnoState {
  reservar() { throw new Error("Ya está reservado") }
  cancelar() { /* transición a Cancelado */ }
  iniciar() { /* transición a EnCurso */ }
  finalizar() { throw new Error("Aún no inició") }
}
```

## 8.2. Patrón Observer

Los estados emiten eventos que pueden ser observados:

```typescript
class Turno {
  private estado: TurnoState
  private observers: Observer[] = []
  
  cambiarEstado(nuevoEstado: TurnoState) {
    this.estado = nuevoEstado
    this.notificarObservadores()
  }
  
  notificarObservadores() {
    this.observers.forEach(obs => obs.actualizar(this))
  }
}
```

---

# 9. CONCLUSIONES Y RECOMENDACIONES

## 9.1. Resumen del Análisis

Los diagramas de estados desarrollados revelan:

1. **Complejidad de Negocio**: El sistema tiene lógica de negocio significativa, especialmente en:
   - Gestión de turnos con múltiples estados y validaciones
   - Proceso de pagos con conciliación bancaria
   - Ciclo de vida completo de socios/alumnos

2. **Puntos Críticos**:
   - Transiciones de Turno (Reservado → En Curso requiere validación temporal)
   - Pago (Pendiente → Confirmado debe ser atómico)
   - Socio/Alumno (Moroso → Suspendido tiene implicaciones legales)

3. **Oportunidades de Automatización**:
   - Transiciones temporales (turno que inicia automáticamente)
   - Notificaciones basadas en cambios de estado
   - Conciliación automática de pagos

## 9.2. Implementación Recomendada

### Base de Datos
```sql
-- Tabla de auditoría de cambios de estado
CREATE TABLE AUDITORIA_ESTADOS (
  id INT PRIMARY KEY AUTO_INCREMENT,
  entidad VARCHAR(50) NOT NULL,
  entidad_id INT NOT NULL,
  estado_anterior VARCHAR(50),
  estado_nuevo VARCHAR(50) NOT NULL,
  evento VARCHAR(100),
  usuario VARCHAR(100),
  fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  observaciones TEXT
);
```

### Backend (Python)
```python
class EstadoMixin:
    """Mixin para agregar gestión de estados a modelos"""
    
    def cambiar_estado(self, nuevo_estado: str, evento: str, usuario: str):
        estado_anterior = self.estado
        
        # Validar transición
        if not self._transicion_valida(estado_anterior, nuevo_estado):
            raise ValueError(f"Transición inválida: {estado_anterior} -> {nuevo_estado}")
        
        # Ejecutar acciones de salida del estado anterior
        self._on_exit(estado_anterior)
        
        # Cambiar estado
        self.estado = nuevo_estado
        
        # Ejecutar acciones de entrada al nuevo estado
        self._on_entry(nuevo_estado)
        
        # Auditar cambio
        self._auditar_cambio(estado_anterior, nuevo_estado, evento, usuario)
```

### Frontend (Vue 3)
```typescript
// Composable para gestión de estados
export function useEstadoMachine<T>(
  estadoInicial: T,
  transiciones: Map<T, T[]>
) {
  const estado = ref<T>(estadoInicial)
  
  function puedeTransicionar(nuevoEstado: T): boolean {
    const estadosPermitidos = transiciones.get(estado.value)
    return estadosPermitidos?.includes(nuevoEstado) ?? false
  }
  
  function transicionar(nuevoEstado: T, evento: string) {
    if (!puedeTransicionar(nuevoEstado)) {
      throw new Error(`Transición no permitida: ${estado.value} -> ${nuevoEstado}`)
    }
    
    const estadoAnterior = estado.value
    estado.value = nuevoEstado
    
    // Emitir evento
    emit('estadoCambiado', {
      anterior: estadoAnterior,
      nuevo: nuevoEstado,
      evento
    })
  }
  
  return { estado, puedeTransicionar, transicionar }
}
```

---

**Analista:** GitHub Copilot (Claude Sonnet 4.5)  
**Fecha de Análisis:** 29 de noviembre de 2025  
**Metodología:** UML 2.5 - State Machine Diagrams  
**Framework de Referencia:** OMG UML Specification + Martin Fowler - UML Distilled
