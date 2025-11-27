<template>
  <div class="home-container">
    <h1>🎾 Club de Tenis</h1>
    <p>
      Bienvenido al sistema de administración del Club de Tenis.<br>
      Gestiona socios, turnos, profesores y categorías desde un solo lugar.
    </p>
    <div class="home-grid">
      <router-link to="/socios" class="home-card">
        <v-icon name="fa-users" scale="2" />
        <strong>Socios</strong>
        <small>Gestión de socios del club</small>
      </router-link>
      <router-link to="/alumnos" class="home-card">
        <v-icon name="fa-graduation-cap" scale="2" />
        <strong>Alumnos</strong>
        <small>Gestión de alumnos de clases</small>
      </router-link>
      <router-link to="/turnos" class="home-card">
        <v-icon name="fa-calendar-alt" scale="2" />
        <strong>Turnos</strong>
        <small>Reserva de turnos de cancha</small>
      </router-link>
      <router-link to="/profesores" class="home-card">
        <v-icon name="fa-chalkboard-teacher" scale="2" />
        <strong>Profesores</strong>
        <small>Gestiona los profesores</small>
      </router-link>
      <router-link to="/categorias" class="home-card">
        <v-icon name="fa-folder-open" scale="2" />
        <strong>Categorías</strong>
        <small>Tipos de membresía</small>
      </router-link>
      <router-link to="/pagos" class="home-card">
        <v-icon name="fa-money-bill-wave" scale="2" />
        <strong>Pagos</strong>
        <small>Registro de pagos y abonos</small>
      </router-link>
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
.home-container {
  max-width: 700px;
  margin: 3rem auto;
  padding: 2rem;
  background: #FFFFFF;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(2, 47, 157, 0.15);
  text-align: center;
}
.logo {
  width: 220px;
  margin-bottom: 0.5rem;
}
.home-container h1 {
  margin-bottom: 0.5rem;
  color: #022F9D;
}
.home-container p {
  color: #444;
  margin-bottom: 2rem;
}
.home-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
}
.home-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f6f8fa;
  border-radius: 8px;
  padding: 1.5rem 1rem;
  text-decoration: none;
  color: #e28c41;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  transition: background 0.2s, box-shadow 0.2s;
}
.home-card:hover {
  background: #e3f0fc;
  box-shadow: 0 2px 8px rgba(2,47,157,0.15);
}
.home-card span {
  font-size: 2.2rem;
  margin-bottom: 0.5rem;
}
.home-card strong {
  font-size: 1.1rem;
  margin-bottom: 0.2rem;
}
.home-card small {
  color: #555;
}
</style>