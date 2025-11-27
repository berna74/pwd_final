<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>Crear Nuevo Profesor</h3>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="nombre">Nombre:</label>
          <input v-model="form.nombre" type="text" id="nombre" required />
        </div>

        <div class="form-group">
          <label for="apellido">Apellido:</label>
          <input v-model="form.apellido" type="text" id="apellido" required />
        </div>

        <div class="form-group">
          <label for="especialidad">Especialidad:</label>
          <input v-model="form.especialidad" type="text" id="especialidad" required />
        </div>

        <div class="form-group">
          <label for="telefono">Teléfono:</label>
          <input v-model="form.telefono" type="tel" id="telefono" required />
        </div>

        <div class="form-group">
          <label for="email">Email:</label>
          <input v-model="form.email" type="email" id="email" required />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary">Crear</button>
          <button type="button" @click="$emit('close')" class="btn-secondary">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useProfesoresStore } from '@/stores/profesores'

const emit = defineEmits(['close', 'created'])
const profesoresStore = useProfesoresStore()

const form = ref({
  nombre: '',
  apellido: '',
  especialidad: '',
  telefono: '',
  email: ''
})

async function handleSubmit() {
  try {
    await profesoresStore.createProfesor(form.value)
    emit('created')
  } catch (error) {
    console.error('Error al crear profesor:', error)
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  min-width: 400px;
  max-width: 600px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-primary,
.btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #022F9D;
  color: #FFFFFF;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #00CDFF;
  color: #000000;
}

.btn-secondary {
  background-color: #CCCCCC;
  color: #000000;
  transition: background-color 0.3s ease;
}

.btn-secondary:hover {
  background-color: #999999;
}
</style>
