<template>
  <div :class="containerClass">
    <router-link
      v-for="link in navigationLinks"
      :key="link.path"
      :to="link.path"
      :class="linkClass"
      active-class="text-blue-600 font-semibold"
      @click="handleNavigate"
    >
      {{ link.label }}
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  isMobile?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  isMobile: false,
});

const emit = defineEmits<{
  navigate: [];
}>();

const navigationLinks = [
  { path: '/empleados', label: 'Empleados' },
  { path: '/tipos-servicios', label: 'Tipos de Servicios' },
  { path: '/servicios', label: 'Servicios' },
  { path: '/reportes', label: 'Reportes' },
];

const containerClass = computed(() => {
  return props.isMobile ? 'flex flex-col space-y-1' : 'flex space-x-4';
});

const linkClass = computed(() => {
  const baseClass = 'text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md transition';
  return props.isMobile ? `${baseClass} block` : baseClass;
});

function handleNavigate() {
  if (props.isMobile) {
    emit('navigate');
  }
}
</script>
