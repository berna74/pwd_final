import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Profesor } from '@/interfaces/Profesor'
import ApiService from '@/services/ApiService'

export const useProfesoresStore = defineStore('profesores', () => {
  const profesores = ref<Profesor[]>([])
  const profesor = ref<Profesor | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchProfesores() {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get('/profesores/')
      profesores.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar los profesores'
    } finally {
      loading.value = false
    }
  }

  async function fetchProfesor(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/profesores/${id}`)
      profesor.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar el profesor'
    } finally {
      loading.value = false
    }
  }

  async function createProfesor(profesorData: Omit<Profesor, 'id'>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/profesores/', profesorData)
      await fetchProfesores()
    } catch (err: any) {
      error.value = err.message || 'Error al crear el profesor'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateProfesor(id: number, profesorData: Partial<Profesor>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/profesores/${id}`, profesorData)
      await fetchProfesores()
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar el profesor'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteProfesor(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/profesores/${id}`)
      await fetchProfesores()
    } catch (err: any) {
      error.value = err.message || 'Error al eliminar el profesor'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    profesores,
    profesor,
    loading,
    error,
    fetchProfesores,
    fetchProfesor,
    createProfesor,
    updateProfesor,
    deleteProfesor
  }
})
