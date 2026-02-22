import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import App from '../App.vue';
import AppHeader from '../components/common/AppHeader.vue';

// Create a mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: { template: '<div>Home</div>' },
    },
  ],
});

describe('App.vue', () => {
  it('renderiza el layout principal correctamente', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router],
        components: {
          AppHeader,
        },
        stubs: {
          RouterView: true,
        },
      },
    });

    expect(wrapper.find('#app').exists()).toBe(true);
    expect(wrapper.findComponent(AppHeader).exists()).toBe(true);
  });

  it('aplica clases de Tailwind para layout', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router],
        components: {
          AppHeader,
        },
        stubs: {
          RouterView: true,
        },
      },
    });

    const appDiv = wrapper.find('#app');
    expect(appDiv.classes()).toContain('min-h-screen');
    expect(appDiv.classes()).toContain('bg-gray-50');
  });

  it('contiene el router-view para contenido dinámico', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router],
        components: {
          AppHeader,
        },
        stubs: {
          RouterView: true,
        },
      },
    });

    expect(wrapper.find('main').exists()).toBe(true);
  });
});
