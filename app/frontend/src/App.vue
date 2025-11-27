<template>
  <nav>
    <RouterLink :to="{ name: 'home' }">🎾 Club de Tenis</RouterLink>
    <RouterLink :to="{ name: 'socios' }">Socios</RouterLink>
    <RouterLink :to="{ name: 'alumnos' }">Alumnos</RouterLink>
    <RouterLink :to="{ name: 'turnos' }">Turnos</RouterLink>
    <RouterLink :to="{ name: 'profesores' }">Profesores</RouterLink>
    <RouterLink :to="{ name: 'categorias_list' }">Categorías</RouterLink>
    <RouterLink :to="{ name: 'pagos' }">Pagos</RouterLink>
  </nav>
  <main>
    <RouterView />
  </main>
</template>

<style>
nav {
  background: #022F9D;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  height: 4rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

nav a {
  color: #FFFFFF;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

nav a:hover {
  color: #00CDFF;
}

nav a.router-link-exact-active {
  color: #FFCD00;
  font-weight: 600;
}

.logo {
  width: 3.5rem; /* Ajusta el tamaño del logo */
  height: auto;
  margin: 0 1rem; /* Espacio entre el logo y los enlaces */
}
</style>