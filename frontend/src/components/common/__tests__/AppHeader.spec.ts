import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import AppHeader from '../AppHeader.vue';
import AppNavigation from '../AppNavigation.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/empleados', component: { template: '<div>Empleados</div>' } },
  ],
});

describe('AppHeader', () => {
  it('renderiza el título del salón', () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router],
        components: {
          AppNavigation,
        },
      },
    });

    expect(wrapper.text()).toContain('Salón de Peluquería');
  });

  it('muestra el botón hamburger en móvil', () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router],
        components: {
          AppNavigation,
        },
      },
    });

    const hamburgerButton = wrapper.find('button[aria-label="Toggle menu"]');
    expect(hamburgerButton.exists()).toBe(true);
    expect(hamburgerButton.classes()).toContain('md:hidden');
  });

  it('muestra navegación desktop oculta en móvil', () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router],
        components: {
          AppNavigation,
        },
      },
    });

    const desktopNav = wrapper.findAllComponents(AppNavigation)[0];
    expect(desktopNav.classes()).toContain('hidden');
    expect(desktopNav.classes()).toContain('md:flex');
  });

  it('alterna el menú móvil al hacer clic en hamburger', async () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router],
        components: {
          AppNavigation,
        },
      },
    });

    const hamburgerButton = wrapper.find('button[aria-label="Toggle menu"]');
    
    // Inicialmente el menú móvil no debe estar visible
    expect(wrapper.findAllComponents(AppNavigation).length).toBe(1);

    // Click para abrir
    await hamburgerButton.trigger('click');
    expect(wrapper.findAllComponents(AppNavigation).length).toBe(2);

    // Click para cerrar
    await hamburgerButton.trigger('click');
    expect(wrapper.findAllComponents(AppNavigation).length).toBe(1);
  });

  it('cambia el icono del hamburger cuando el menú está abierto', async () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router],
        components: {
          AppNavigation,
        },
      },
    });

    const hamburgerButton = wrapper.find('button[aria-label="Toggle menu"]');
    const svg = hamburgerButton.find('svg');

    // Inicialmente muestra el icono de hamburger (3 líneas)
    let paths = svg.findAll('path');
    expect(paths[0].attributes('d')).toContain('M4 6h16M4 12h16M4 18h16');

    // Después de hacer clic, muestra el icono de X
    await hamburgerButton.trigger('click');
    paths = svg.findAll('path');
    expect(paths[0].attributes('d')).toContain('M6 18L18 6M6 6l12 12');
  });

  it('cierra el menú móvil al navegar', async () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router],
        components: {
          AppNavigation,
        },
      },
    });

    const hamburgerButton = wrapper.find('button[aria-label="Toggle menu"]');
    
    // Abrir menú
    await hamburgerButton.trigger('click');
    expect(wrapper.findAllComponents(AppNavigation).length).toBe(2);

    // Emitir evento de navegación desde el componente móvil
    const mobileNav = wrapper.findAllComponents(AppNavigation)[1];
    await mobileNav.vm.$emit('navigate');

    // El menú debe cerrarse
    await wrapper.vm.$nextTick();
    expect(wrapper.findAllComponents(AppNavigation).length).toBe(1);
  });

  it('aplica estilos responsive correctamente', () => {
    const wrapper = mount(AppHeader, {
      global: {
        plugins: [router],
        components: {
          AppNavigation,
        },
      },
    });

    const nav = wrapper.find('nav');
    expect(nav.classes()).toContain('bg-white');
    expect(nav.classes()).toContain('shadow-md');

    const container = wrapper.find('.container');
    expect(container.exists()).toBe(true);
    expect(container.classes()).toContain('mx-auto');
  });
});
