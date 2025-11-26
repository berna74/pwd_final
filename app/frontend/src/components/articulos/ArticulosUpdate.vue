  <template>
    <div class="container">
      <h3>Modificar Artículo</h3>
      <form @submit.prevent="modificar">
        <div class="input">
          <label for="">Descripción del artículo</label>
          <input type="text" name="" v-model="articulo.descripcion" />
          
          <label for="">Precio</label>
          <input type="number" name="" v-model="articulo.precio" step="0.01" />
          
          <label for="">Stock</label>
          <input type="number" name="" v-model="articulo.stock" />
          
          <label for="">Marca</label>
          <select v-if="articulo.marca" v-model="articulo.marca.id">
            <option :value="0">Seleccione una marca</option>
            <option v-for="marca in marcas" :key="marca.id" :value="marca.id">
              {{ marca.nombre }}
            </option>
          </select>
          
          <label for="">Proveedor</label>
          <select v-if="articulo.proveedor" v-model="articulo.proveedor.id">
            <option :value="0">Seleccione un proveedor</option>
            <option v-for="proveedor in proveedores" :key="proveedor.id" :value="proveedor.id">
              {{ proveedor.nombre }}
            </option>
          </select>
          
          <label for="categorias">Categorías (mantener Ctrl/Cmd para seleccionar múltiples)</label>
          <select id="categorias" v-model="categoriasSeleccionadas" multiple size="5">
            <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
              {{ categoria.nombre }}
            </option>
          </select>
        </div>
        <div class="botonera">
          <RouterLink :to="{ name: 'articulos_list' }"><button type="button">Volver</button></RouterLink>
          <button type="submit">Modificar</button>
        </div>
      </form>
    </div>
  </template>  <script setup lang="ts">
  import { ref, onMounted, toRefs } from 'vue'
  import useArticuloStore from '../../stores/articulos'
  import useCategoriaStore from '@/stores/categorias'
  import useMarcaStore from '@/stores/marcas'
  import useProveedorStore from '@/stores/proveedor'
  import { useRoute, useRouter } from 'vue-router'
  import type { Articulo } from '@/interfaces/Articulo'
  
  const route = useRoute()
  const router = useRouter()
  const store = useArticuloStore()
  const categoriaStore = useCategoriaStore()
  const marcaStore = useMarcaStore()
  const proveedorStore = useProveedorStore()
  const { articulos } = toRefs(store)
  const { update, getAll } = store
  const { categorias } = toRefs(categoriaStore)
  const { marcas } = toRefs(marcaStore)
  const { proveedores } = toRefs(proveedorStore)
  
  const categoriasSeleccionadas = ref<number[]>([])
  
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
    await Promise.all([
      getAll(),
      categoriaStore.getAll(),
      marcaStore.getAll(),
      proveedorStore.getAll()
    ])
    
    const id = route.params.id
    const found = articulos.value.find((a) => a.id == parseInt(id as string))
    if (found) {
      // Aseguro que marca y proveedor tengan valores por defecto si son undefined
      articulo.value = { 
        ...found,
        marca: found.marca || { id: 0, nombre: '' },
        proveedor: found.proveedor || { id: 0, nombre: '' },
        categorias: found.categorias || []
      }
      // Cargo las categorías seleccionadas
      categoriasSeleccionadas.value = articulo.value.categorias.map(c => c.id)
    } else {
      alert('Artículo no encontrado')
      router.push({ name: 'articulos_list' })
    }
  })
  
  const modificar = async () => {
    if (!articulo.value.descripcion) {
      alert('Por favor, complete la descripción')
      return
    }
    try {
      // Actualizo las categorías con las seleccionadas
      articulo.value.categorias = categoriasSeleccionadas.value.map(id => {
        const cat = categorias.value.find(c => c.id === id)
        return cat || { id, nombre: '' }
      })
      
      await update(articulo.value)
      alert('Artículo modificado correctamente')
      router.push({ name: 'articulos_list' })
    } catch (error) {
      console.error('Error al modificar el artículo:', error)
      alert('Hubo un error al modificar el artículo')
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

.input {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
  font-size: 0.95rem;
}

.input input,
.input select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.input input:focus,
.input select:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

.input select {
  cursor: pointer;
  background-color: white;
}

.input select[multiple] {
  min-height: 140px;
  padding: 0.5rem;
  cursor: pointer;
}

.input select[multiple] option {
  padding: 0.5rem;
  margin: 0.15rem 0;
  border-radius: 3px;
  cursor: pointer;
}

.input select[multiple] option:hover {
  background: #f5f5f5;
}

.input select[multiple] option:checked {
  background: #1976d2;
  color: white;
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
}
</style>