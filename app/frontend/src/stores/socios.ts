import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Socio } from '@/interfaces/Socio'
import ApiService from '@/services/ApiService'

export const useSociosStore = defineStore('socios', () => {
  const socios = ref<Socio[]>([])
  const socio = ref<Socio | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchSocios() {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get('/socios/')
      socios.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar los socios'
    } finally {
      loading.value = false
    }
  }

  async function fetchSocio(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/socios/${id}`)
      socio.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar el socio'
    } finally {
      loading.value = false
    }
  }

  async function createSocio(socioData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/socios/', socioData)
      await fetchSocios()
    } catch (err: any) {
      error.value = err.message || 'Error al crear el socio'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateSocio(id: number, socioData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/socios/${id}`, socioData)
      await fetchSocios()
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar el socio'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteSocio(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/socios/${id}`)
      await fetchSocios()
    } catch (err: any) {
      error.value = err.message || 'Error al eliminar el socio'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    socios,
    socio,
    loading,
    error,
    fetchSocios,
    fetchSocio,
    createSocio,
    updateSocio,
    deleteSocio
  }
})
