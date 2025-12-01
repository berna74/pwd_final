<template>
  <div class="pagos-list">
    <div class="list-header">
      <h2>Registro de Pagos</h2>
      <button @click="$emit('create')" class="btn-create">+ Registrar Pago</button>
    </div>
    
    <div v-if="loading" class="loading">Cargando pagos...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="pagos.length === 0" class="empty">No hay pagos registrados</div>
    
    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Tipo</th>
            <th>Monto</th>
            <th>Fecha Pago</th>
            <th>Período</th>
            <th>Pagado por</th>
            <th>Profesor</th>
            <th>Método</th>
            <th>Observaciones</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pago in pagos" :key="pago.id">
            <td>{{ pago.id }}</td>
            <td>
              <span :class="['badge-tipo', getTipoBadgeClass(pago.tipo)]">
                {{ formatTipo(pago.tipo) }}
              </span>
            </td>
            <td class="monto">${{ formatMonto(pago.monto) }}</td>
            <td>{{ formatDate(pago.fecha_pago) }}</td>
            <td>{{ formatPeriodo(pago.mes, pago.anio) }}</td>
            <td>{{ getBeneficiario(pago) }}</td>
            <td>{{ pago.profesor_nombre || '-' }}</td>
            <td>{{ pago.metodo_pago || '-' }}</td>
            <td class="observaciones">{{ pago.observaciones || '-' }}</td>
            <td class="actions">
              <button @click="$emit('show', pago.id)" class="btn-show">Ver</button>
              <button @click="$emit('edit', pago.id)" class="btn-edit">Editar</button>
              <button @click="handleDelete(pago.id)" class="btn-delete">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { usePagosStore } from '@/stores/pagos'
import { storeToRefs } from 'pinia'
import type { Pago } from '@/interfaces/Pago'

const emit = defineEmits(['create', 'show', 'edit'])
const pagosStore = usePagosStore()
const { pagos, loading, error } = storeToRefs(pagosStore)

onMounted(() => {
  pagosStore.fetchPagos()
})

function formatTipo(tipo: string): string {
  return tipo
}

function getTipoBadgeClass(tipo: string): string {
  const classes: Record<string, string> = {
    'Cuota Social': 'badge-cuota',
    'Abono Mensual': 'badge-mensual',
    'Abono Diario': 'badge-diario',
    'Clase': 'badge-clase'
  }
  return classes[tipo] || 'badge-default'
}

function formatMonto(monto: number): string {
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(monto)
}

function formatDate(dateString: string): string {
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('es-AR')
}

function formatPeriodo(mes: number, anio: number): string {
  const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
  return `${meses[mes - 1]} ${anio}`
}

function getBeneficiario(pago: Pago): string {
  if (pago.socio_nombre) return `Socio: ${pago.socio_nombre}`
  if (pago.alumno_nombre) return `Alumno: ${pago.alumno_nombre}`
  return '-'
}

async function handleDelete(id: number) {
  if (confirm('¿Está seguro de eliminar este pago?')) {
    try {
      await pagosStore.deletePago(id)
    } catch (e) {
      console.error('Error al eliminar pago:', e)
    }
  }
}
</script>

<style scoped>
.pagos-list {
  padding: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  color: #022F9D;
  margin: 0;
}

.btn-create {
  background-color: #022F9D;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-create:hover {
  background-color: #00CDFF;
}

.table-container {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #022F9D;
  color: white;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #CCCCCC;
}

th {
  font-weight: bold;
}

tbody tr:hover {
  background-color: #f5f5f5;
}

.badge-tipo {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  display: inline-block;
}

.badge-cuota {
  background-color: #022F9D;
  color: white;
}

.badge-mensual {
  background-color: #00CDFF;
  color: #000000;
}

.badge-diario {
  background-color: #FFCD00;
  color: #000000;
}

.badge-clase {
  background-color: #28a745;
  color: white;
}

.badge-default {
  background-color: #6c757d;
  color: white;
}

.monto {
  font-weight: bold;
  color: #28a745;
}

.observaciones {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.actions {
  display: flex;
  gap: 5px;
}

.btn-show, .btn-edit, .btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-show {
  background-color: #00CDFF;
  color: white;
}

.btn-show:hover {
  background-color: #00a0cc;
}

.btn-edit {
  background-color: #FFCD00;
  color: #000000;
}

.btn-edit:hover {
  background-color: #ccaa00;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
}

.btn-delete:hover {
  background-color: #c82333;
}

.loading, .error, .empty {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #dc3545;
}
</style>
