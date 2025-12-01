<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h2>Nuevo Socio</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-row">
          <div class="form-group">
            <label>Nombre:*</label>
            <input type="text" v-model="formData.nombre" required />
          </div>
          <div class="form-group">
            <label>Apellido:*</label>
            <input type="text" v-model="formData.apellido" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>DNI:*</label>
            <input type="text" v-model="formData.dni" required />
          </div>
          <div class="form-group">
            <label>Teléfono:*</label>
            <input type="tel" v-model="formData.telefono" required />
          </div>
        </div>

        <div class="form-group">
          <label>Email:*</label>
          <input type="email" v-model="formData.email" required />
        </div>

        <div class="form-group">
          <label>Fecha de Inscripción:*</label>
          <input type="date" v-model="formData.fecha_inscripcion" required />
        </div>

        <div class="form-group">
          <label>Profesor:</label>
          <select v-model.number="formData.profesor_id">
            <option :value="null">Sin profesor asignado</option>
            <option v-for="prof in profesores" :key="prof.id" :value="prof.id">
              {{ prof.nombre }} {{ prof.apellido }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Categorías:</label>
          <div class="checkbox-group">
            <label v-for="cat in categorias" :key="cat.id" class="checkbox-label">
              <input 
                type="checkbox" 
                :value="cat.id" 
                v-model="selectedCategorias"
              />
              {{ cat.nombre }}
            </label>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="submitLoading">
            {{ submitLoading ? 'Guardando...' : 'Crear Socio' }}
          </button>
          <button type="button" class="btn-cancel" @click="$emit('close')">Cancelar</button>
        </div>
        
        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSociosStore } from '@/stores/socios'
import { useProfesoresStore } from '@/stores/profesores'
import { useCategoriasStore } from '@/stores/categorias'
import { storeToRefs } from 'pinia'

const emit = defineEmits(['close', 'created'])
const sociosStore = useSociosStore()
const profesoresStore = useProfesoresStore()
const categoriasStore = useCategoriasStore()

const { profesores } = storeToRefs(profesoresStore)
const { categorias } = storeToRefs(categoriasStore)

const formData = ref({
  nombre: '',
  apellido: '',
  dni: '',
  email: '',
  telefono: '',
  fecha_inscripcion: new Date().toISOString().split('T')[0],
  profesor_id: null as number | null
})

const selectedCategorias = ref<number[]>([])
const submitLoading = ref(false)
const error = ref<string | null>(null)

onMounted(() => {
  profesoresStore.fetchProfesores()
  categoriasStore.fetchCategorias()
})

async function handleSubmit() {
  submitLoading.value = true
  error.value = null
  
  try {
    const socioData = {
      ...formData.value,
      categorias_ids: selectedCategorias.value
    }
    
    await sociosStore.createSocio(socioData)
    emit('created')
  } catch (e: any) {
    error.value = e.response?.data?.mensaje || 'Error al crear socio'
    console.error('Error completo:', e)
  } finally {
    submitLoading.value = false
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
  max-width: 600px;
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

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #CCCCCC;
  border-radius: 4px;
  font-size: 14px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 5px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-submit, .btn-cancel {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-submit {
  background-color: #022F9D;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background-color: #00CDFF;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: #CCCCCC;
  color: #000000;
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
