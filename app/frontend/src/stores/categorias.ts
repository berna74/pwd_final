import type {Categoria} from '@/interfaces/Categoria';
import { defineStore } from 'pinia';
import { ref } from 'vue';
import ApiService from '../services/ApiService';

const url = '/categorias';

const useCategoriaStore = defineStore('categorias',  () => {
  const categorias = ref<Array<Categoria>>([]);
  const categoria = ref<Categoria>({
    id: 0,
    nombre: ''
  });


   async function getAll() {
    const data = await ApiService.getAll(url);
    if(data) {
      categorias.value = data
     }
  }
         

  async function getOne(id: number) {
    const data = await ApiService.getOne(url, id);
    if(data) {
      categorias.value = data
         }
        }

  async function create(categoria: Categoria) {
    const data = await ApiService.create(url, categoria);
    if(data) {
      categorias.value = data;
    }
  }
  async function update(categoria: Categoria) {
    if(categoria.id) {
      const data = await ApiService.update(url, categoria.id, categoria);
      if(data) {
        categorias.value = data;
      }
    }
  }

  async function destroy(id: number) {
    const data = await ApiService.destroy(url, id);
    if(data) {
      categorias.value = data;
    }
  }
  // Alias para compatibilidad
  const fetchCategorias = getAll;

  return {categorias, categoria, getAll, getOne, create, update, destroy, fetchCategorias};
})

export default useCategoriaStore;
export { useCategoriaStore as useCategoriasStore };