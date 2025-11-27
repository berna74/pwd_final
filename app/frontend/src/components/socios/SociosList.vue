<template>
  <div class="socios-list">
    <div class="header">
      <h2>Lista de Socios</h2>
      <button @click="showCreateForm = true" class="btn-primary">Nuevo Socio</button>
    </div>

    <div v-if="loading" class="loading">Cargando socios...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="socios-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>DNI</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Fecha Inscripción</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="socio in socios" :key="socio.id">
            <td>{{ socio.id }}</td>
            <td>{{ socio.nombre }}</td>
            <td>{{ socio.apellido }}</td>
            <td>{{ socio.dni }}</td>
            <td>{{ socio.email }}</td>
            <td>{{ socio.telefono }}</td>
            <td>{{ socio.fecha_inscripcion }}</td>
            <td>
              <button @click="confirmDelete(socio.id)" class="btn-delete">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSociosStore } from '@/stores/socios'
import { storeToRefs } from 'pinia'

const sociosStore = useSociosStore()
const { socios, loading, error } = storeToRefs(sociosStore)

const showCreateForm = ref(false)

onMounted(() => {
  sociosStore.fetchSocios()
})

function confirmDelete(id: number) {
  if (confirm('¿Está seguro de que desea eliminar este socio?')) {
    sociosStore.deleteSocio(id)
  }
}
</script>

<style scoped>
.socios-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.socios-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.socios-table th,
.socios-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.socios-table th {
  background-color: #022F9D;
  color: #FFFFFF;
}

.socios-table tr:nth-child(even) {
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
