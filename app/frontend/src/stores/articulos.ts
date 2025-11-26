import type {Articulo} from '@/interfaces/Articulo';
import { defineStore } from 'pinia';
import { ref } from 'vue';
import ApiService from '../services/ApiService';

const url = '/articulos';


const useArticuloStore = defineStore('articulos',  () => {
  const articulos = ref<Array<Articulo>>([]);
  const articulo = ref<Articulo>({
    id: 0,
    descripcion: '',
    precio: 0,
    stock: 0,
    marca_id: 0,
    proveedor_id: 0,
    categoria: ''
  });


   async function getAll() {
    const data = await ApiService.getAll(url);
    if(data) {
      articulos.value = data
     }
  }
         

  async function getOne(id: number) {
    const data = await ApiService.getOne(url, id);
    if(data) {
      articulos.value = data
         }
        }

  async function create(articulo: Articulo) {
    // Transformar el objeto para enviar solo los IDs al backend
    const articuloParaBackend = {
      descripcion: articulo.descripcion,
      precio: articulo.precio,
      stock: articulo.stock,
      marca_id: articulo.marca?.id || 0,
      proveedor_id: articulo.proveedor?.id || 0,
      categorias: articulo.categorias?.map(c => c.id) || []
    };
    const data = await ApiService.create(url, articuloParaBackend);
    if(data) {
      articulos.value = data;
    }
  }
  async function update(articulo: Articulo) {
    if(articulo.id) {
      // Transformar el objeto para enviar solo los IDs al backend
      const articuloParaBackend = {
        descripcion: articulo.descripcion,
        precio: articulo.precio,
        stock: articulo.stock,
        marca_id: articulo.marca?.id || 0,
        proveedor_id: articulo.proveedor?.id || 0,
        categorias: articulo.categorias?.map(c => c.id) || []
      };
      const data = await ApiService.update(url, articulo.id, articuloParaBackend);
      if(data) {
        articulos.value = data;
       }
  }
  }
  async function destroy(id: number) {
    const data = await ApiService.destroy(url, id);
    if(data) {
      articulos.value = data;
    }
  }
  return {articulos, articulo, getAll, getOne, create, update, destroy};
})

export default useArticuloStore