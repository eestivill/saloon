<template>
  <div id="app" class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader />
    <main class="flex-1 container mx-auto px-4 py-6">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import AppHeader from './components/common/AppHeader.vue';
</script>
