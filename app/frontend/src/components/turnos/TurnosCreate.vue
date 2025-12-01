<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h2>Nuevo Turno</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Fecha:</label>
          <input type="date" v-model="formData.fecha" required />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Hora Inicio:</label>
            <input type="time" v-model="formData.hora_inicio" required step="1800" />
          </div>
          <div class="form-group">
            <label>Hora Fin:</label>
            <input type="time" v-model="formData.hora_fin" required step="1800" />
          </div>
        </div>

        <div class="form-group">
          <label>Socio que Reserva (ID):</label>
          <input type="number" v-model.number="formData.socio_reserva_id" min="1" />
        </div>

        <div class="form-group">
          <label>Estado:</label>
          <select v-model="formData.estado" required>
            <option value="disponible">Disponible</option>
            <option value="reservado">Reservado</option>
          </select>
        </div>

        <div class="form-group">
          <label>Jugadores (uno por línea):</label>
          <textarea v-model="jugadoresText" rows="4" placeholder="Nombre Jugador 1&#10;Nombre Jugador 2"></textarea>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="loading">
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
          <button type="button" class="btn-cancel" @click="$emit('close')">Cancelar</button>
        </div>
        
        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useTurnosStore } from '@/stores/turnos'

const emit = defineEmits(['close', 'created'])
const turnosStore = useTurnosStore()

const formData = ref({
  cancha: 'Cancha Principal',
  fecha: '',
  hora_inicio: '',
  hora_fin: '',
  socio_reserva_id: null as number | null,
  estado: 'disponible',
})

const jugadoresText = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  loading.value = true
  error.value = null
  
  try {
    const jugadores = jugadoresText.value
      .split('\n')
      .map(j => j.trim())
      .filter(j => j.length > 0)
    
    await turnosStore.createTurno({
      ...formData.value,
      jugadores
    })
    emit('created')
  } catch (e: any) {
    error.value = e.response?.data?.mensaje || 'Error al crear turno'
  } finally {
    loading.value = false
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
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

h2 {
  color: #022F9D;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #022F9D;
  font-weight: bold;
}

input, select, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #CCCCCC;
  border-radius: 4px;
  font-size: 14px;
}

textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-submit {
  flex: 1;
  background-color: #022F9D;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit:hover:not(:disabled) {
  background-color: #00CDFF;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  flex: 1;
  background-color: #CCCCCC;
  color: #000000;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel:hover {
  background-color: #999999;
}

.error {
  color: #dc3545;
  margin-top: 10px;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 4px;
}
</style>
