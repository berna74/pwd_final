<template>
  <div class="pelotitas-view">
    <PelotitasList
      @showCreate="showCreateModal = true"
      @showEdit="handleEdit"
      @showView="handleView"
    />
    <PelotitasCreate
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @saved="handleSaved"
    />
    <PelotitasUpdate
      v-if="showEditModal && selectedId"
      :pelotita-id="selectedId"
      @close="showEditModal = false"
      @updated="handleUpdated"
    />
    <PelotitasShow
      v-if="showViewModal && selectedId"
      :pelotita-id="selectedId"
      @close="showViewModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PelotitasList from '@/components/pelotitas/PelotitasList.vue'
import PelotitasCreate from '@/components/pelotitas/PelotitasCreate.vue'
import PelotitasUpdate from '@/components/pelotitas/PelotitasUpdate.vue'
import PelotitasShow from '@/components/pelotitas/PelotitasShow.vue'
import { usePelotitasStore } from '@/stores/pelotitas'

const pelotitasStore = usePelotitasStore()
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showViewModal = ref(false)
const selectedId = ref<number | null>(null)

const handleEdit = (id: number) => {
  selectedId.value = id
  showEditModal.value = true
}

const handleView = (id: number) => {
  selectedId.value = id
  showViewModal.value = true
}

const handleSaved = async () => {
  await pelotitasStore.fetchPelotitas()
  await pelotitasStore.fetchResumen()
}

const handleUpdated = async () => {
  await pelotitasStore.fetchPelotitas()
  await pelotitasStore.fetchResumen()
}
</script>

<style scoped>
.pelotitas-view {
  min-height: 100vh;
  background: #f5f7fa;
}
</style>
