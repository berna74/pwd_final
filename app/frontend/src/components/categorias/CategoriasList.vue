<template>
    <div class="container">
    <h2>Categorías</h2>
    <router-link :to="{name: 'categorias_create'}"><button>Crear Categoría</button></router-link>
    
    <div v-if="categorias.length === 0" class="alert alert-info mt-3">
      No hay categorías registradas. Haz clic en "Crear Categoría" para agregar una.
    </div>

    <table v-else class="table table-striped mt-3">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="categoria in categorias" :key="categoria.id">
          <td>{{ categoria.id }}</td>
          <td>{{ categoria.nombre }}</td>
          <td>
           <router-link v-if="categoria.id" :to="{name: 'categorias_show', params: {id: categoria.id }}"><button>Mostrar</button></router-link>
           <router-link v-if="categoria.id" :to="{name: 'categorias_edit', params: {id: categoria.id }}"><button>Editar</button></router-link>
           <button @click.prevent="eliminar(categoria.id as number)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  </template>
  
  <script setup lang="ts">
  import useCategoriaStore from '@/stores/categorias';
  import { onMounted } from 'vue';
  import { toRefs } from 'vue';
  
  const {categorias} = toRefs(useCategoriaStore());
  const { getAll, destroy } = useCategoriaStore();
  
  onMounted(async() => {
    await getAll();
  });
  
  async function eliminar (id: number) {
    if (confirm('¿Estás seguro de eliminar la categoría ' + id + '?')) {
      if (confirm('Esta acción no se puede deshacer. ¿Deseas continuar?')) {
        
        console.log('Eliminando categoría con ID:', id);
      } else {
        console.log('Eliminación cancelada por el usuario.');
        return;
      }
      
         await destroy(id);
         await getAll();
      }
  }
  
  </script>
  
  <style scoped>
   .container {
    max-width: 700px;
    margin: 2rem auto;
    padding: 2rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  button {
    margin: 5px;
  }
  </style>