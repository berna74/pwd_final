<template>
    <div class="container">
      <h3>Modificar Proveedor</h3>
      <form @submit.prevent="modificar">
        <div class="form-group">
          <label for="nombre">Nombre del proveedor</label>
          <input type="text" id="nombre" v-model="proveedor.nombre" />
        </div>
        
        <div class="form-group">
          <label for="telefono">Teléfono</label>
          <input type="text" id="telefono" v-model="proveedor.telefono" />
        </div>
        
        <div class="form-group">
          <label for="direccion">Dirección</label>
          <input type="text" id="direccion" v-model="proveedor.direccion" />
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="proveedor.email" />
        </div>
        
        <div class="botonera">
          <RouterLink :to="{ name: 'proveedores_list' }"><button type="button">Volver</button></RouterLink>
          <button type="submit">Modificar</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, toRefs } from 'vue'
  import useProveedorStore from '../../stores/proveedor'
  import { useRoute, useRouter } from 'vue-router'
  import type { Proveedor } from '@/interfaces/Proveedor'
  
  const route = useRoute()
  const router = useRouter()
  const store = useProveedorStore()
  const { proveedores } = toRefs(store)
  const { update, getAll } = store
  
  const proveedor = ref<Proveedor>({
    id: 0,
    nombre: '',
    telefono: '',
    direccion: '',
    email: ''
  })
  
  onMounted(async () => {
    await getAll()
    const id = route.params.id
    const found = proveedores.value.find((p) => p.id == parseInt(id as string))
    if (found) {
      proveedor.value = { ...found }
    } else {
      alert('Proveedor no encontrado')
      router.push({ name: 'proveedores_list' })
    }
  })
  
  const modificar = async () => {
    if (!proveedor.value.nombre) {
      alert('Por favor, complete el nombre')
      return
    }
    try {
      await update(proveedor.value)
      alert('Proveedor modificado correctamente')
      router.push({ name: 'proveedores_list' })
    } catch (error) {
      console.error('Error al modificar el proveedor:', error)
      alert('Error al modificar el proveedor')
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

h3 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
  font-size: 0.95rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

.botonera {
  display: flex;
  gap: 10px;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

button[type="submit"] {
  background-color: #1976d2;
  color: white;
}

button[type="submit"]:hover {
  background-color: #1565c0;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

button[type="button"] {
  background-color: #f5f5f5;
  color: #333;
}

button[type="button"]:hover {
  background-color: #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
</style>