<template>
    <div class="container">
      <h2>Crear Artículo</h2>
      <form @submit.prevent="crear">
        <div class="form-group">
          <label for="descripcion">Descripción del artículo</label>
          <input type="text" id="descripcion" v-model="nuevoArticulo.descripcion" placeholder="Ingrese la descripción" />
        </div>
        
        <div class="form-group">
          <label for="precio">Precio</label>
          <input type="number" id="precio" v-model="nuevoArticulo.precio" placeholder="Ingrese el precio" step="0.01" />
        </div>
        
        <div class="form-group">
          <label for="stock">Stock</label>
          <input type="number" id="stock" v-model="nuevoArticulo.stock" placeholder="Ingrese el stock" />
        </div>
        
        <div class="form-group">
          <label for="marca">Marca</label>
          <select id="marca" v-model="nuevoArticulo.marca.id">
            <option :value="0">Seleccione una marca</option>
            <option v-for="marca in marcas" :key="marca.id" :value="marca.id">
              {{ marca.nombre }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="proveedor">Proveedor</label>
          <select id="proveedor" v-model="nuevoArticulo.proveedor.id">
            <option :value="0">Seleccione un proveedor</option>
            <option v-for="proveedor in proveedores" :key="proveedor.id" :value="proveedor.id">
              {{ proveedor.nombre }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="categorias">Categorías (mantener Ctrl/Cmd para seleccionar múltiples)</label>
          <select id="categorias" v-model="categoriasSeleccionadas" multiple size="5">
            <option v-for="categoria in categorias" :key="categoria.id" :value="categoria.id">
              {{ categoria.nombre }}
            </option>
          </select>
        </div>
        
        <div class="botonera">
          <router-link :to="{ name: 'articulos_list' }">
            <button type="button">Volver</button>
          </router-link>
          <button type="submit">Guardar</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import useArticuloStore from '@/stores/articulos';
  import useCategoriaStore from '@/stores/categorias';
  import useMarcaStore from '@/stores/marcas';
  import useProveedorStore from '@/stores/proveedor';
  import type { Articulo } from '@/interfaces/Articulo';
  import { toRefs } from 'vue';
  
  const router = useRouter();
  const { create } = useArticuloStore();
  const categoriaStore = useCategoriaStore();
  const marcaStore = useMarcaStore();
  const proveedorStore = useProveedorStore();
  const { categorias } = toRefs(categoriaStore);
  const { marcas } = toRefs(marcaStore);
  const { proveedores } = toRefs(proveedorStore);
  
  const categoriasSeleccionadas = ref<number[]>([]);
  
  const nuevoArticulo = ref<Articulo>({
    id: 0,
    descripcion: '',
    precio: 0,
    stock: 0,
    marca: { id: 0, nombre: '' },
    proveedor: { id: 0, nombre: '' },
    categorias: []
  });
  
  onMounted(async () => {
    await categoriaStore.getAll();
    await marcaStore.getAll();
    await proveedorStore.getAll();
  });
  
  const crear = async () => { 
    if (!nuevoArticulo.value.descripcion) {
      alert('Por favor, ingrese una descripción para el artículo.');
      return;
    }
  
    try {
      // Asigno las categorías seleccionadas
      nuevoArticulo.value.categorias = categoriasSeleccionadas.value.map(id => {
        const cat = categorias.value.find(c => c.id === id);
        return cat || { id, nombre: '' };
      });
      
      await create(nuevoArticulo.value); 
      router.push({ name: 'articulos_list' });
    } catch (error) {
      console.error('Error al crear el artículo:', error);
      alert('Hubo un error al crear el artículo. Por favor, inténtalo de nuevo.');
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

  h2 {
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
  
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
    box-sizing: border-box;
  }
  
  .form-group input:focus,
  .form-group select:focus {
    outline: none;
    border-color: #1976d2;
    box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
  }

  .form-group select {
    cursor: pointer;
    background-color: white;
  }
  
  .form-group select[multiple] {
    min-height: 140px;
    padding: 0.5rem;
    cursor: pointer;
  }
  
  .form-group select[multiple] option {
    padding: 0.5rem;
    margin: 0.15rem 0;
    border-radius: 3px;
    cursor: pointer;
  }
  
  .form-group select[multiple] option:hover {
    background: #f5f5f5;
  }
  
  .form-group select[multiple] option:checked {
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