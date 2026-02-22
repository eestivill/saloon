import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import TiposServiciosList from '../TiposServiciosList.vue';
import { useTiposServiciosStore } from '@/stores/tiposServicios';
import TipoServicioCard from '../TipoServicioCard.vue';
import TipoServicioForm from '../TipoServicioForm.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';

// Mock the API
vi.mock('@/services/api', () => ({
  tiposServiciosAPI: {
    listar: vi.fn(() => Promise.resolve({ data: [] })),
    crear: vi.fn(),
    actualizar: vi.fn(),
    eliminar: vi.fn(),
  },
}));

describe('TiposServiciosList', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('muestra spinner mientras carga', () => {
    const store = useTiposServiciosStore();
    store.loading = true;

    const wrapper = mount(TiposServiciosList, {
      global: {
        components: {
          TipoServicioCard,
          TipoServicioForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.findComponent(LoadingSpinner).exists()).toBe(true);
  });

  it('muestra mensaje de error cuando falla', () => {
    const store = useTiposServiciosStore();
    store.loading = false;
    store.error = 'Error al cargar tipos de servicios';

    const wrapper = mount(TiposServiciosList, {
      global: {
        components: {
          TipoServicioCard,
          TipoServicioForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.findComponent(ErrorMessage).exists()).toBe(true);
    expect(wrapper.text()).toContain('Error al cargar tipos de servicios');
  });

  it('muestra mensaje cuando no hay tipos de servicios', () => {
    const store = useTiposServiciosStore();
    store.loading = false;
    store.error = null;
    store.tiposServicios = [];

    const wrapper = mount(TiposServiciosList, {
      global: {
        components: {
          TipoServicioCard,
          TipoServicioForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.text()).toContain('No hay tipos de servicios registrados');
  });

  it('muestra lista de tipos de servicios correctamente', () => {
    const store = useTiposServiciosStore();
    store.loading = false;
    store.error = null;
    store.tiposServicios = [
      { nombre: 'Corte Básico', descripcion: 'Corte de cabello básico', porcentaje_comision: 40 },
      { nombre: 'Tinte Completo', descripcion: 'Tinte de cabello completo', porcentaje_comision: 35 },
    ];

    const wrapper = mount(TiposServiciosList, {
      global: {
        components: {
          TipoServicioCard,
          TipoServicioForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    const cards = wrapper.findAllComponents(TipoServicioCard);
    expect(cards).toHaveLength(2);
  });

  it('muestra botón "Nuevo Tipo de Servicio"', () => {
    const store = useTiposServiciosStore();
    store.loading = false;
    store.error = null;
    store.tiposServicios = [];

    const wrapper = mount(TiposServiciosList, {
      global: {
        components: {
          TipoServicioCard,
          TipoServicioForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.text()).toContain('Nuevo Tipo de Servicio');
  });

  it('muestra formulario cuando se hace clic en "Nuevo Tipo de Servicio"', async () => {
    const store = useTiposServiciosStore();
    store.loading = false;
    store.error = null;
    store.tiposServicios = [];

    const wrapper = mount(TiposServiciosList, {
      global: {
        components: {
          TipoServicioCard,
          TipoServicioForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    await wrapper.find('button').trigger('click');

    expect(wrapper.findComponent(TipoServicioForm).exists()).toBe(true);
  });

  it('aplica grid responsive correctamente', () => {
    const store = useTiposServiciosStore();
    store.loading = false;
    store.error = null;
    store.tiposServicios = [
      { nombre: 'Corte Básico', descripcion: 'Corte de cabello básico', porcentaje_comision: 40 },
      { nombre: 'Tinte Completo', descripcion: 'Tinte de cabello completo', porcentaje_comision: 35 },
    ];

    const wrapper = mount(TiposServiciosList, {
      global: {
        components: {
          TipoServicioCard,
          TipoServicioForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    const grid = wrapper.find('.grid');
    expect(grid.exists()).toBe(true);
    expect(grid.classes()).toContain('grid-cols-1');
    expect(grid.classes()).toContain('md:grid-cols-2');
    expect(grid.classes()).toContain('lg:grid-cols-3');
  });
});
