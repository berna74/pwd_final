<template>
  <div class="container">
  <h2>Marcas</h2>
  <router-link :to="{name: 'marcas_create'}"><button>Crear Marca</button></router-link>
  
  <div v-if="marcas.length === 0" class="empty-message">
    <p>No hay marcas registradas. Crea una nueva marca para comenzar.</p>
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
      <tr v-for="marca in marcas" :key="marca.id">
        <td>{{ marca.id }}</td>
        <td>{{ marca.nombre }}</td>
        <td>
         <router-link v-if="marca.id" :to="{name: 'marcas_show', params: {id: marca.id }}"><button>Mostrar</button></router-link>
         <router-link v-if="marca.id" :to="{name: 'marcas_edit', params: {id: marca.id }}"><button>Editar</button></router-link>
         <button v-if="marca.id" @click.prevent="eliminar(marca.id as number)">Eliminar</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
</template>

<script setup lang="ts">
import useMarcaStore from '@/stores/marcas';
import { onMounted } from 'vue';
import { toRefs } from 'vue';

const {marcas} = toRefs(useMarcaStore());
const { getAll, destroy } = useMarcaStore();

onMounted(async() => {
  await getAll();
});

async function eliminar (id: number) {
  if (confirm('¿Estás seguro de eliminar la marca ' + id + '?')) {
    if (confirm('Esta acción no se puede deshacer. ¿Deseas continuar?')) {
      
      console.log('Eliminando marca con ID:', id);
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
.empty-message {
  margin: 2rem 0;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 4px;
  text-align: center;
  color: #666;
}
</style>