<template>
  <nav class="bg-white shadow-md">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <router-link to="/" class="flex items-center gap-2 text-xl font-bold text-gray-800 hover:text-blue-600 transition-colors">
          <img src="@/assets/logo.svg" alt="SM" class="h-8 w-auto" />
          <span>Stephany Mondragón</span>
        </router-link>

        <button
          @click="toggleMenu"
          class="md:hidden text-gray-600 hover:text-blue-600 focus:outline-none"
          aria-label="Toggle menu"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              v-if="!isMenuOpen"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>

        <AppNavigation :is-mobile="false" class="hidden md:flex" />
      </div>

      <AppNavigation
        v-if="isMenuOpen"
        :is-mobile="true"
        class="md:hidden pb-4"
        @navigate="closeMenu"
      />
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import AppNavigation from './AppNavigation.vue';

const isMenuOpen = ref(false);

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value;
}

function closeMenu() {
  isMenuOpen.value = false;
}
</script>
