<template>
  <div class="profesores-list">
    <div class="header">
      <h2>Lista de Profesores</h2>
      <button @click="showCreateForm = true" class="btn-primary">Nuevo Profesor</button>
    </div>

    <ProfesoresCreate v-if="showCreateForm" @close="showCreateForm = false" @created="handleCreated" />

    <div v-if="loading" class="loading">Cargando profesores...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="profesores-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Especialidad</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="profesor in profesores" :key="profesor.id">
            <td>{{ profesor.id }}</td>
            <td>{{ profesor.nombre }}</td>
            <td>{{ profesor.apellido }}</td>
            <td>{{ profesor.especialidad }}</td>
            <td>{{ profesor.telefono }}</td>
            <td>{{ profesor.email }}</td>
            <td>
              <button @click="viewProfesor(profesor.id)" class="btn-view">Ver</button>
              <button @click="editProfesor(profesor.id)" class="btn-edit">Editar</button>
              <button @click="confirmDelete(profesor.id)" class="btn-delete">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <ProfesoresShow v-if="showingProfesorId" :id="showingProfesorId" @close="showingProfesorId = null" />
    <ProfesoresUpdate v-if="editingProfesorId" :id="editingProfesorId" @close="editingProfesorId = null" @updated="handleUpdated" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useProfesoresStore } from '@/stores/profesores'
import { storeToRefs } from 'pinia'
import ProfesoresCreate from './ProfesoresCreate.vue'
import ProfesoresShow from './ProfesoresShow.vue'
import ProfesoresUpdate from './ProfesoresUpdate.vue'

const profesoresStore = useProfesoresStore()
const { profesores, loading, error } = storeToRefs(profesoresStore)

const showCreateForm = ref(false)
const showingProfesorId = ref<number | null>(null)
const editingProfesorId = ref<number | null>(null)

onMounted(() => {
  profesoresStore.fetchProfesores()
})

function viewProfesor(id: number) {
  showingProfesorId.value = id
}

function editProfesor(id: number) {
  editingProfesorId.value = id
}

function confirmDelete(id: number) {
  if (confirm('¿Está seguro de que desea eliminar este profesor?')) {
    profesoresStore.deleteProfesor(id)
  }
}

function handleCreated() {
  showCreateForm.value = false
  profesoresStore.fetchProfesores()
}

function handleUpdated() {
  editingProfesorId.value = null
  profesoresStore.fetchProfesores()
}
</script>

<style scoped>
.profesores-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.profesores-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.profesores-table th,
.profesores-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.profesores-table th {
  background-color: #022F9D;
  color: #FFFFFF;
}

.profesores-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.btn-primary {
  background-color: #022F9D;
  color: #FFFFFF;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #00CDFF;
  color: #000000;
}

.btn-primary:hover {
  background-color: #011f6b;
}

.btn-view {
  background-color: #00CDFF;
  color: #000000;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  margin-right: 5px;
  transition: background-color 0.3s ease;
}

.btn-view:hover {
  background-color: #022F9D;
  color: #FFFFFF;
}

.btn-edit {
  background-color: #FFCD00;
  color: #000000;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  margin-right: 5px;
  transition: background-color 0.3s ease;
}

.btn-edit:hover {
  background-color: #022F9D;
  color: #FFFFFF;
}

.btn-delete {
  background-color: #f44336;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.loading,
.error {
  padding: 20px;
  text-align: center;
}

.error {
  color: #f44336;
}
</style>
