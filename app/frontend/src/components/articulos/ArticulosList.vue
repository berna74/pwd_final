<template>
    <div class="container">
    <h2>Artículos</h2>
    <router-link :to="{name: 'articulos_create'}"><button>Crear Artículo</button></router-link>
    
    <div v-if="articulos.length === 0" class="alert alert-info mt-3">
      No hay artículos registrados. Haz clic en "Crear Artículo" para agregar uno.
    </div>

    <table v-else class="table table-striped mt-3">
      <thead>
        <tr>
          <th>ID</th>
          <th>Descripción</th>
          <th>Precio</th>
          <th>Stock</th>
          <th>Marca</th>
          <th>Proveedor</th>          
          <th>Categorías</th>          
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="articulo in articulos" :key="articulo.id">
          <td>{{ articulo.id }}</td>
          <td>{{ articulo.descripcion }}</td>
          <td>{{ articulo.precio }}</td> 
          <td>{{ articulo.stock }}</td>
          <td>{{ articulo.marca?.nombre || 'N/A' }}</td>
          <td>{{ articulo.proveedor?.nombre || 'N/A' }}</td>
          <td>
            <span v-if="articulo.categorias && articulo.categorias.length > 0">
              {{ articulo.categorias.map((c: any) => c.nombre).join(', ') }}
            </span>
            <span v-else>Sin categorías</span>
          </td>         
          <td>
           <router-link v-if="articulo.id" :to="{name: 'articulos_show', params: {id: articulo.id }}"><button>Mostrar</button></router-link>
           <router-link v-if="articulo.id" :to="{name: 'articulos_edit', params: {id: articulo.id }}"><button>Editar</button></router-link>
           <button @click.prevent="eliminar(articulo.id as number)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  </template>
  
  <script setup lang="ts">
  import useArticuloStore from '@/stores/articulos';
  import { onMounted } from 'vue';
  import { toRefs } from 'vue';
  
  const {articulos} = toRefs(useArticuloStore());
  const { getAll, destroy } = useArticuloStore();
  
  onMounted(async() => {
    await getAll();
  });
  
  async function eliminar (id: number) {
    if (confirm('¿Estás seguro de eliminar el artículo ' + id + '?')) {
      if (confirm('Esta acción no se puede deshacer. ¿Deseas continuar?')) {
        console.log('Eliminando artículo con ID:', id);
        await destroy(id);
        await getAll();
      } else {
        console.log('Eliminación cancelada por el usuario.');
      }
    }
  }
  
  </script>
  
  <style scoped>
   .container {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 2rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    overflow-x: auto;
  }

  h2 {
    margin-bottom: 1.5rem;
    color: #333;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.5rem;
  }

  th {
    background-color: #f5f5f5;
    padding: 0.75rem;
    text-align: left;
    font-weight: 600;
    color: #333;
    border-bottom: 2px solid #ddd;
  }

  td {
    padding: 0.75rem;
    border-bottom: 1px solid #eee;
    vertical-align: middle;
  }

  tr:hover {
    background-color: #f9f9f9;
  }

  button {
    margin: 2px;
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  button:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .alert {
    padding: 1rem;
    margin-top: 1rem;
    border-radius: 4px;
    background: #e3f0fc;
    color: #1976d2;
    text-align: center;
  }

  @media (max-width: 1024px) {
    .container {
      padding: 1rem;
    }
    
    table {
      font-size: 0.9rem;
    }
    
    th, td {
      padding: 0.5rem;
    }
  }
  </style>