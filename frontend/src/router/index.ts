import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/empleados',
      name: 'empleados',
      component: () => import('@/views/EmpleadosView.vue'),
    },
    {
      path: '/servicios',
      name: 'servicios',
      component: () => import('@/views/ServiciosView.vue'),
    },
    {
      path: '/tipos-servicios',
      name: 'tipos-servicios',
      component: () => import('@/views/TiposServiciosView.vue'),
    },
    {
      path: '/reportes',
      name: 'reportes',
      component: () => import('@/views/ReportesView.vue'),
    },
  ],
});

export default router;
