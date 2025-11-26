<template>
    <div class="container">
      <h3>Modificar Marca</h3>
      <form @submit.prevent="modificar">
        <div class="input">
          <label for="">Nombre de la marca</label>
          <input type="text" name="" v-model="marca.nombre" />
        </div>
        <div class="botonera">
          <RouterLink :to="{ name: 'marcas_list' }"><button type="button">Volver</button> </RouterLink>
          <button type="submit">Modificar</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
  import { toRefs, onMounted, ref } from 'vue'
  import useMarcaStore from '../../stores/marcas'
  import { useRoute, useRouter } from 'vue-router'
  import type { Marca } from '@/interfaces/Marca'
  
  const route = useRoute()
  const router = useRouter()
  
  const { marcas } = toRefs(useMarcaStore())
  const { update } = useMarcaStore()
  
  const marca = ref<Marca>({
    id: 0,
    nombre: ''
  })
  
  onMounted(() => {
    const id = route.params.id
    console.log(id)
    const marcaEncontrada = marcas.value.find((m) => m.id == parseInt(id as string))
    if (marcaEncontrada) {
      marca.value = { ...marcaEncontrada }
    } else {
      alert('Marca no encontrada')
      router.push({ name: 'marcas_list' })
    }
  })
  
  const modificar = async () => {
    if (!marca.value.nombre) {
      alert('Por favor, complete el nombre')
    } else {
      await update(marca.value)
      router.push({ name: 'marcas_list' })
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
</style>