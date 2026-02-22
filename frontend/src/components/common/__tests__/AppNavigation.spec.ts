import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import AppNavigation from '../AppNavigation.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/empleados', component: { template: '<div>Empleados</div>' } },
    { path: '/tipos-servicios', component: { template: '<div>Tipos</div>' } },
    { path: '/servicios', component: { template: '<div>Servicios</div>' } },
    { path: '/reportes', component: { template: '<div>Reportes</div>' } },
  ],
});

describe('AppNavigation', () => {
  it('renderiza todos los enlaces de navegación', () => {
    const wrapper = mount(AppNavigation, {
      global: {
        plugins: [router],
      },
    });

    expect(wrapper.text()).toContain('Empleados');
    expect(wrapper.text()).toContain('Tipos de Servicios');
    expect(wrapper.text()).toContain('Servicios');
    expect(wrapper.text()).toContain('Reportes');
  });

  it('aplica estilos horizontales en modo desktop', () => {
    const wrapper = mount(AppNavigation, {
      props: {
        isMobile: false,
      },
      global: {
        plugins: [router],
      },
    });

    const container = wrapper.find('div');
    expect(container.classes()).toContain('flex');
    expect(container.classes()).toContain('space-x-4');
    expect(container.classes()).not.toContain('flex-col');
  });

  it('aplica estilos verticales en modo móvil', () => {
    const wrapper = mount(AppNavigation, {
      props: {
        isMobile: true,
      },
      global: {
        plugins: [router],
      },
    });

    const container = wrapper.find('div');
    expect(container.classes()).toContain('flex');
    expect(container.classes()).toContain('flex-col');
    expect(container.classes()).toContain('space-y-1');
  });

  it('aplica clases de enlace correctas en desktop', () => {
    const wrapper = mount(AppNavigation, {
      props: {
        isMobile: false,
      },
      global: {
        plugins: [router],
      },
    });

    const links = wrapper.findAll('a');
    links.forEach((link) => {
      expect(link.classes()).toContain('text-gray-600');
      expect(link.classes()).toContain('hover:text-blue-600');
      expect(link.classes()).toContain('px-3');
      expect(link.classes()).toContain('py-2');
      expect(link.classes()).toContain('rounded-md');
      expect(link.classes()).toContain('transition');
    });
  });

  it('aplica clases de enlace correctas en móvil', () => {
    const wrapper = mount(AppNavigation, {
      props: {
        isMobile: true,
      },
      global: {
        plugins: [router],
      },
    });

    const links = wrapper.findAll('a');
    links.forEach((link) => {
      expect(link.classes()).toContain('block');
    });
  });

  it('emite evento navigate al hacer clic en móvil', async () => {
    const wrapper = mount(AppNavigation, {
      props: {
        isMobile: true,
      },
      global: {
        plugins: [router],
      },
    });

    const firstLink = wrapper.find('a');
    await firstLink.trigger('click');

    expect(wrapper.emitted('navigate')).toBeTruthy();
    expect(wrapper.emitted('navigate')).toHaveLength(1);
  });

  it('no emite evento navigate al hacer clic en desktop', async () => {
    const wrapper = mount(AppNavigation, {
      props: {
        isMobile: false,
      },
      global: {
        plugins: [router],
      },
    });

    const firstLink = wrapper.find('a');
    await firstLink.trigger('click');

    expect(wrapper.emitted('navigate')).toBeFalsy();
  });

  it('contiene los enlaces correctos con las rutas correctas', () => {
    const wrapper = mount(AppNavigation, {
      global: {
        plugins: [router],
      },
    });

    const links = wrapper.findAll('a');
    expect(links[0].attributes('href')).toBe('/empleados');
    expect(links[1].attributes('href')).toBe('/tipos-servicios');
    expect(links[2].attributes('href')).toBe('/servicios');
    expect(links[3].attributes('href')).toBe('/reportes');
  });

  it('aplica clase active-class cuando la ruta está activa', async () => {
    await router.push('/empleados');
    await router.isReady();

    const wrapper = mount(AppNavigation, {
      global: {
        plugins: [router],
      },
    });

    const empleadosLink = wrapper.findAll('a')[0];
    expect(empleadosLink.classes()).toContain('text-blue-600');
    expect(empleadosLink.classes()).toContain('font-semibold');
  });
});
