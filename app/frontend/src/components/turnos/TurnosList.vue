<template>
  <div class="turnos-list">
    <div class="header">
      <h2>Lista de Turnos</h2>
      <button @click="showCreateForm = true" class="btn-primary">Nuevo Turno</button>
    </div>

    <TurnosCreate v-if="showCreateForm" @close="showCreateForm = false" @created="handleCreated" />

    <div v-if="loading" class="loading">Cargando turnos...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="turnos-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Fecha</th>
            <th>Horario</th>
            <th>Estado</th>
            <th>Reservado por</th>
            <th>Jugadores</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="turno in turnos" :key="turno.id">
            <td>{{ turno.id }}</td>
            <td>{{ formatDate(turno.fecha) }}</td>
            <td>{{ turno.hora_inicio }} - {{ turno.hora_fin }}</td>
            <td>
              <span :class="['estado', turno.estado]">{{ turno.estado }}</span>
            </td>
            <td>{{ turno.socio_reserva_nombre || '-' }}</td>
            <td>{{ turno.jugadores.join(', ') || '-' }}</td>
            <td>
              <button @click="viewTurno(turno.id)" class="btn-view">Ver</button>
              <button @click="editTurno(turno.id)" class="btn-edit">Editar</button>
              <button @click="confirmDelete(turno.id)" class="btn-delete">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <TurnosShow v-if="showingTurnoId" :id="showingTurnoId" @close="showingTurnoId = null" />
    <TurnosUpdate v-if="editingTurnoId" :id="editingTurnoId" @close="editingTurnoId = null" @updated="handleUpdated" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTurnosStore } from '@/stores/turnos'
import { storeToRefs } from 'pinia'
import TurnosCreate from './TurnosCreate.vue'
import TurnosShow from './TurnosShow.vue'
import TurnosUpdate from './TurnosUpdate.vue'

const turnosStore = useTurnosStore()
const { turnos, loading, error } = storeToRefs(turnosStore)

const showCreateForm = ref(false)
const showingTurnoId = ref<number | null>(null)
const editingTurnoId = ref<number | null>(null)

onMounted(() => {
  turnosStore.fetchTurnos()
})

function formatDate(dateString: string) {
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('es-AR')
}

function viewTurno(id: number) {
  showingTurnoId.value = id
}

function editTurno(id: number) {
  editingTurnoId.value = id
}

async function confirmDelete(id: number) {
  if (confirm('¿Está seguro de que desea eliminar este turno?')) {
    try {
      await turnosStore.deleteTurno(id)
    } catch (e) {
      alert('Error al eliminar el turno')
    }
  }
}

function handleCreated() {
  showCreateForm.value = false
  turnosStore.fetchTurnos()
}

function handleUpdated() {
  editingTurnoId.value = null
  turnosStore.fetchTurnos()
}
</script>

<style scoped>
.turnos-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  color: #022F9D;
  margin: 0;
}

.turnos-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.turnos-table th,
.turnos-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #CCCCCC;
}

.turnos-table th {
  background-color: #022F9D;
  color: white;
  font-weight: bold;
}

.turnos-table tr:hover {
  background-color: #f5f5f5;
}

.estado {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: bold;
}

.estado.disponible {
  background-color: #4CAF50;
  color: white;
}

.estado.reservado {
  background-color: #FFCD00;
  color: #000000;
}

.btn-primary {
  background-color: #022F9D;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary:hover {
  background-color: #00CDFF;
}

.btn-view {
  background-color: #00CDFF;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.btn-edit {
  background-color: #FFCD00;
  color: #000000;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-view:hover,
.btn-edit:hover,
.btn-delete:hover {
  opacity: 0.8;
}

.loading,
.error {
  text-align: center;
  padding: 20px;
  font-size: 16px;
}

.error {
  color: #dc3545;
}
</style>
