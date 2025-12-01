# Actualización del Módulo de Pagos

## Cambios Realizados

### 1. Tipos de Pago Actualizados
Se actualizaron los tipos de pago disponibles en el sistema:

**Tipos anteriores:**
- `cuota_socio` → Cuota de Socio
- `abono_clase` → Abono de Clase

**Tipos nuevos:**
- `Cuota Social` - Para pagos de cuota social de socios
- `Abono Mensual` - Para abonos mensuales de alumnos
- `Abono Diario` - Para abonos diarios de alumnos
- `Clase` - Para pagos de clases individuales (requiere profesor)

### 2. Campo Profesor Agregado
Se agregó el campo `profesor_id` a la tabla PAGOS para identificar al profesor cuando el tipo de pago es "Clase".

#### Base de Datos
- **Nueva columna:** `profesor_id INT NULL`
- **Foreign Key:** Relacionada con `PROFESORES(id)` con `ON DELETE SET NULL`

#### Backend (Python/Flask)
- **Archivos modificados:**
  - `/app/backend/app/modules/pagos/pago_model.py`
    - Agregado `profesor_id` al modelo
    - Agregado `profesor_nombre` para mostrar el nombre del profesor
    - Actualizado `get_all()` con JOIN a tabla PROFESORES
    - Actualizado `get_by_id()` con JOIN a tabla PROFESORES
    - Actualizado `create()` para incluir profesor_id
    - Actualizado `update()` para incluir profesor_id

#### Frontend (Vue 3/TypeScript)
- **Archivos modificados:**
  
  1. `/frontend/src/interfaces/Pago.ts`
     - Agregado `profesor_id: number | null`
     - Agregado `profesor_nombre: string`

  2. `/frontend/src/components/pagos/PagosCreate.vue`
     - Actualizado formulario con nuevos tipos de pago
     - Agregado selector de profesor (visible solo cuando tipo = "Clase")
     - Importado `useProfesoresStore`
     - Actualizada lógica de validación según tipo de pago

  3. `/frontend/src/components/pagos/PagosList.vue`
     - Agregada columna "Profesor" en la tabla
     - Actualizada función `formatTipo()` para nuevos tipos
     - Actualizada función `getTipoBadgeClass()` con nuevos estilos
     - Agregados badges con colores específicos:
       - Cuota Social: Azul (#022F9D)
       - Abono Mensual: Cyan (#00CDFF)
       - Abono Diario: Amarillo (#FFCD00)
       - Clase: Verde (#28a745)

### 3. Migración de Datos
Se ejecutó el script `migrate_pagos.py` que:
- Agregó la columna `profesor_id` a la tabla PAGOS
- Creó la foreign key hacia PROFESORES
- Actualizó 9 registros existentes mapeando los valores antiguos a los nuevos

### 4. Lógica de Negocio

**Según el tipo de pago se requiere:**

| Tipo de Pago | Socio | Alumno | Profesor |
|-------------|-------|--------|----------|
| Cuota Social | ✓ Requerido | - | - |
| Abono Mensual | - | ✓ Requerido | - |
| Abono Diario | - | ✓ Requerido | - |
| Clase | - | ✓ Requerido | ✓ Requerido |

## Archivos Creados

1. `/app/backend/update_pagos_table.sql` - Script SQL para migración manual
2. `/app/backend/migrate_pagos.py` - Script Python para migración automatizada

## Testing

### Backend
```bash
# Verificar endpoint
curl http://localhost:5000/pagos/

# Debe retornar:
# - profesor_id: null o ID del profesor
# - profesor_nombre: null o nombre del profesor
# - tipo: "Cuota Social", "Abono Mensual", "Abono Diario" o "Clase"
```

### Frontend
1. Abrir formulario de registro de pagos
2. Verificar que aparecen los 4 tipos de pago
3. Seleccionar tipo "Clase"
4. Verificar que aparece el selector de profesor
5. Completar y guardar

## Estado Actual
✅ Migración de base de datos completada
✅ Backend actualizado y funcionando
✅ Frontend actualizado
✅ Servidor Flask reiniciado con cambios
✅ 9 registros existentes migrados correctamente

## Próximos Pasos Sugeridos
- Crear componente de edición de pagos (PagosUpdate.vue)
- Crear componente de visualización detallada (PagosShow.vue)
- Agregar filtros por tipo de pago en la lista
- Agregar reporte de pagos por profesor
