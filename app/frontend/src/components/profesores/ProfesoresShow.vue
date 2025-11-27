<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>Detalles del Profesor</h3>
      <div v-if="loading">Cargando...</div>
      <div v-else-if="profesor">
        <div class="detail-row">
          <strong>ID:</strong> {{ profesor.id }}
        </div>
        <div class="detail-row">
          <strong>Nombre:</strong> {{ profesor.nombre }} {{ profesor.apellido }}
        </div>
        <div class="detail-row">
          <strong>Especialidad:</strong> {{ profesor.especialidad }}
        </div>
        <div class="detail-row">
          <strong>Teléfono:</strong> {{ profesor.telefono }}
        </div>
        <div class="detail-row">
          <strong>Email:</strong> {{ profesor.email }}
        </div>
        <button @click="$emit('close')" class="btn-close">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useProfesoresStore } from '@/stores/profesores'
import { storeToRefs } from 'pinia'

const props = defineProps<{ id: number }>()
const emit = defineEmits(['close'])

const profesoresStore = useProfesoresStore()
const { profesor, loading } = storeToRefs(profesoresStore)

onMounted(() => {
  profesoresStore.fetchProfesor(props.id)
})
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
}

.detail-row {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.btn-close {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #00CDFF;
  color: #000000;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-close:hover {
  background-color: #022F9D;
  color: #FFFFFF;
}
</style>
