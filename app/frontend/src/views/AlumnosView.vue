<template>
  <div class="alumnos-view">
    <AlumnosList @create="showCreate = true" />
    <AlumnosCreate v-if="showCreate" @close="showCreate = false" @created="handleCreated" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AlumnosList from '@/components/alumnos/AlumnosList.vue'
import AlumnosCreate from '@/components/alumnos/AlumnosCreate.vue'

const showCreate = ref(false)

function handleCreated() {
  showCreate.value = false
}
</script>

<style scoped>
.alumnos-view {
  padding: 20px;
}
</style>
