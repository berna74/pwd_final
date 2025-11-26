<template>
    
    <div class="container" v-if="articulo.id">
    <h2>Detalle del Artículo</h2>
    <div class="details">
        <p><strong>ID:</strong> {{ articulo.id }}</p>
        <p><strong>Descripción:</strong> {{ articulo.descripcion }}</p>
        <p><strong>Precio:</strong> ${{ articulo.precio }}</p>
        <p><strong>Stock:</strong> {{ articulo.stock }}</p>
        <p><strong>Marca:</strong> {{ articulo.marca?.nombre }}</p>
        <p><strong>Proveedor:</strong> {{ articulo.proveedor?.nombre }}</p>
        <p><strong>Categorías:</strong> {{ articulo.categorias?.map(c => c.nombre).join(', ') }}</p>
      </div>
  
      <RouterLink :to="{ name: 'articulos_list' }"><button>Volver</button> </RouterLink>
    </div>
    <div v-else class="container">
        <p>Cargando artículo...</p>
    </div>
  </template>
  
  <script setup lang="ts">
  import { toRefs, onMounted, ref } from 'vue'
  import useArticuloStore from '../../stores/articulos'
  import { useRoute } from 'vue-router'
  import type { Articulo } from '@/interfaces/Articulo'
  
  const route = useRoute()
  const articuloStore = useArticuloStore()
  const { articulos } = toRefs(articuloStore)
  const { getAll } = articuloStore
  
  const articulo = ref<Articulo>({
    id: 0,
    descripcion: '',
    precio: 0,
    stock: 0,
    marca: { id: 0, nombre: '' },
    proveedor: { id: 0, nombre: '' },
    categorias: []
  })
  
  onMounted(async () => {
    await getAll()
    const id = route.params.id
    const found = articulos.value.find((a) => a.id == parseInt(id as string))
    if (found) {
      articulo.value = found
    }
  })
</script>
<style scoped>
.container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
</style>