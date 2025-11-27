import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'
import type { Pago } from '@/interfaces/Pago'

export const usePagosStore = defineStore('pagos', () => {
  const pagos = ref<Pago[]>([])
  const pago = ref<Pago | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchPagos() {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get('/pagos/')
      pagos.value = response.data
    } catch (e: any) {
      error.value = e.message
      console.error('Error fetching pagos:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchPago(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/pagos/${id}`)
      pago.value = response.data
    } catch (e: any) {
      error.value = e.message
      console.error('Error fetching pago:', e)
    } finally {
      loading.value = false
    }
  }

  async function createPago(pagoData: Partial<Pago>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/pagos/', pagoData)
      await fetchPagos()
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updatePago(id: number, pagoData: Partial<Pago>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/pagos/${id}`, pagoData)
      await fetchPagos()
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deletePago(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/pagos/${id}`)
      await fetchPagos()
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    pagos,
    pago,
    loading,
    error,
    fetchPagos,
    fetchPago,
    createPago,
    updatePago,
    deletePago
  }
})
