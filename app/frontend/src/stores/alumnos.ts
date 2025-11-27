import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'
import type { Alumno } from '@/interfaces/Alumno'

export const useAlumnosStore = defineStore('alumnos', () => {
  const alumnos = ref<Alumno[]>([])
  const alumno = ref<Alumno | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAlumnos() {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get('/alumnos/')
      alumnos.value = response.data
    } catch (e: any) {
      error.value = e.message
      console.error('Error fetching alumnos:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchAlumno(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/alumnos/${id}`)
      alumno.value = response.data
    } catch (e: any) {
      error.value = e.message
      console.error('Error fetching alumno:', e)
    } finally {
      loading.value = false
    }
  }

  async function createAlumno(alumnoData: Partial<Alumno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/alumnos/', alumnoData)
      await fetchAlumnos()
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateAlumno(id: number, alumnoData: Partial<Alumno>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/alumnos/${id}`, alumnoData)
      await fetchAlumnos()
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteAlumno(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/alumnos/${id}`)
      await fetchAlumnos()
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    alumnos,
    alumno,
    loading,
    error,
    fetchAlumnos,
    fetchAlumno,
    createAlumno,
    updateAlumno,
    deleteAlumno
  }
})
