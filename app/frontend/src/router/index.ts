import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import marcas_routes from './marcas_routes'
import articulos_routes from './articulos_routes'
import categorias_routes from './categorias_routes'
import proveedores_routes from './proveedores_routes'

// Asegúrate de que los nombres de las rutas estén en minúscula
// y que los componentes se importen correctamente.

const routes = [
  { path: '/', name: 'home', component: HomeView }, // nombre en minúscula
  ...marcas_routes,
  ...articulos_routes,
  ...categorias_routes,
  ...proveedores_routes 
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router