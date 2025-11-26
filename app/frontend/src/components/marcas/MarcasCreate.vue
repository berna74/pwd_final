<template>
  <div class="container">
    <h2>Crear Marca</h2>
    <form @submit.prevent="crear">
      <label for="">Nueva Marca</label>
      <input type="text" name="" v-model="nuevaMarca.nombre" />
      <div class="botonera">
        <router-link :to="{ name: 'marcas_list' }">
          <button type="button">Volver</button>
        </router-link>
        <button type="submit">Guardar</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import useMarcaStore from '@/stores/marcas';
import type { Marca } from '@/interfaces/Marca';

const router = useRouter();
const { create } = useMarcaStore(); 

const nuevaMarca = ref<Marca>({
  id: 0,
  nombre: ''
});

const crear = async () => { 
  if (!nuevaMarca.value.nombre) {
    alert('Por favor, ingrese un nombre para la marca.');
    return;
  }

  try {
    await create(nuevaMarca.value); 
    router.push({ name: 'marcas_list' });
  } catch (error) {
    console.error('Error al crear la marca:', error);
    alert('Hubo un error al crear la marca. Por favor, inténtalo de nuevo.');
  }
};
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

.botonera {
  display: flex;
  gap: 10px;
  margin-top: 1rem;
}

button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>