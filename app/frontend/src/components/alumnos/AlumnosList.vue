<template>
  <div class="alumnos-list">
    <div class="list-header">
      <h2>Lista de Alumnos</h2>
      <button @click="$emit('create')" class="btn-create">+ Nuevo Alumno</button>
    </div>
    
    <div v-if="loading" class="loading">Cargando alumnos...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="alumnos.length === 0" class="empty">No hay alumnos registrados</div>
    
    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>DNI</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Profesor</th>
            <th>Nivel</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alumno in alumnos" :key="alumno.id">
            <td>{{ alumno.id }}</td>
            <td>{{ alumno.nombre }} {{ alumno.apellido }}</td>
            <td>{{ alumno.dni }}</td>
            <td>{{ alumno.email }}</td>
            <td>{{ alumno.telefono }}</td>
            <td>{{ alumno.profesor?.nombre }} {{ alumno.profesor?.apellido }}</td>
            <td>{{ alumno.nivel }}</td>
            <td>
              <span :class="['badge', alumno.activo ? 'badge-active' : 'badge-inactive']">
                {{ alumno.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="actions">
              <button @click="$emit('show', alumno.id)" class="btn-show">Ver</button>
              <button @click="$emit('edit', alumno.id)" class="btn-edit">Editar</button>
              <button @click="handleDelete(alumno.id)" class="btn-delete">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAlumnosStore } from '@/stores/alumnos'
import { storeToRefs } from 'pinia'

const emit = defineEmits(['create', 'show', 'edit'])
const alumnosStore = useAlumnosStore()
const { alumnos, loading, error } = storeToRefs(alumnosStore)

onMounted(() => {
  alumnosStore.fetchAlumnos()
})

async function handleDelete(id: number) {
  if (confirm('¿Está seguro de eliminar este alumno?')) {
    try {
      await alumnosStore.deleteAlumno(id)
    } catch (e) {
      console.error('Error al eliminar alumno:', e)
    }
  }
}
</script>

<style scoped>
.alumnos-list {
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

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.badge-active {
  background-color: #28a745;
  color: white;
}

.badge-inactive {
  background-color: #6c757d;
  color: white;
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
