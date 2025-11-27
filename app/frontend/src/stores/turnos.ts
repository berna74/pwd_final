import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Turno } from '@/interfaces/Turno'
import ApiService from '@/services/ApiService'

export const useTurnosStore = defineStore('turnos', () => {
  const turnos = ref<Turno[]>([])
  const turno = ref<Turno | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchTurnos() {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get('/turnos/')
      turnos.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Error al cargar turnos'
      console.error('Error fetching turnos:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchTurno(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/turnos/${id}`)
      turno.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Error al cargar turno'
      console.error('Error fetching turno:', e)
    } finally {
      loading.value = false
    }
  }

  async function createTurno(turnoData: Partial<Turno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/turnos/', turnoData)
      await fetchTurnos()
    } catch (e: any) {
      error.value = e.message || 'Error al crear turno'
      console.error('Error creating turno:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateTurno(id: number, turnoData: Partial<Turno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/turnos/${id}`, turnoData)
      await fetchTurnos()
    } catch (e: any) {
      error.value = e.message || 'Error al actualizar turno'
      console.error('Error updating turno:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteTurno(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/turnos/${id}`)
      await fetchTurnos()
    } catch (e: any) {
      error.value = e.message || 'Error al eliminar turno'
      console.error('Error deleting turno:', e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    turnos,
    turno,
    loading,
    error,
    fetchTurnos,
    fetchTurno,
    createTurno,
    updateTurno,
    deleteTurno
  }
})
