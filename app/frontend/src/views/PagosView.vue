<template>
  <div class="pagos-view">
    <PagosList @create="showCreate = true" />
    <PagosCreate v-if="showCreate" @close="showCreate = false" @created="handleCreated" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PagosList from '@/components/pagos/PagosList.vue'
import PagosCreate from '@/components/pagos/PagosCreate.vue'

const showCreate = ref(false)

function handleCreated() {
  showCreate.value = false
}
</script>

<style scoped>
.pagos-view {
  padding: 20px;
}
</style>
