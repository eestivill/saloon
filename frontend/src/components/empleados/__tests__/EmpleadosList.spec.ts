import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import EmpleadosList from '../EmpleadosList.vue';
import { useEmpleadosStore } from '@/stores/empleados';
import EmpleadoCard from '../EmpleadoCard.vue';
import EmpleadoForm from '../EmpleadoForm.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';

// Mock the API
vi.mock('@/services/api', () => ({
  empleadosAPI: {
    listar: vi.fn(() => Promise.resolve({ data: [] })),
    crear: vi.fn(),
    actualizar: vi.fn(),
    eliminar: vi.fn(),
  },
}));

describe('EmpleadosList', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('muestra spinner mientras carga', () => {
    const store = useEmpleadosStore();
    store.loading = true;

    const wrapper = mount(EmpleadosList, {
      global: {
        components: {
          EmpleadoCard,
          EmpleadoForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          // Prevent onMounted from running
          teleport: true,
        },
      },
    });

    expect(wrapper.findComponent(LoadingSpinner).exists()).toBe(true);
  });

  it('muestra mensaje de error cuando falla', () => {
    const store = useEmpleadosStore();
    store.loading = false;
    store.error = 'Error al cargar empleados';

    const wrapper = mount(EmpleadosList, {
      global: {
        components: {
          EmpleadoCard,
          EmpleadoForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.findComponent(ErrorMessage).exists()).toBe(true);
    expect(wrapper.text()).toContain('Error al cargar empleados');
  });

  it('muestra mensaje cuando no hay empleados', () => {
    const store = useEmpleadosStore();
    store.loading = false;
    store.error = null;
    store.empleados = [];

    const wrapper = mount(EmpleadosList, {
      global: {
        components: {
          EmpleadoCard,
          EmpleadoForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.text()).toContain('No hay empleados registrados');
  });

  it('muestra lista de empleados correctamente', () => {
    const store = useEmpleadosStore();
    store.loading = false;
    store.error = null;
    store.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
      { id: 'E002', nombre: 'María García' },
    ];

    const wrapper = mount(EmpleadosList, {
      global: {
        components: {
          EmpleadoCard,
          EmpleadoForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    const cards = wrapper.findAllComponents(EmpleadoCard);
    expect(cards).toHaveLength(2);
  });

  it('muestra botón "Nuevo Empleado"', () => {
    const store = useEmpleadosStore();
    store.loading = false;
    store.error = null;
    store.empleados = [];

    const wrapper = mount(EmpleadosList, {
      global: {
        components: {
          EmpleadoCard,
          EmpleadoForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.text()).toContain('Nuevo Empleado');
  });

  it('muestra formulario cuando se hace clic en "Nuevo Empleado"', async () => {
    const store = useEmpleadosStore();
    store.loading = false;
    store.error = null;
    store.empleados = [];

    const wrapper = mount(EmpleadosList, {
      global: {
        components: {
          EmpleadoCard,
          EmpleadoForm,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    await wrapper.find('button').trigger('click');

    expect(wrapper.findComponent(EmpleadoForm).exists()).toBe(true);
  });

  it('aplica grid responsive correctamente', () => {
    const store = useEmpleadosStore();
    store.loading = false;
    store.error = null;
    store.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
      { id: 'E002', nombre: 'María García' },
    ];

    const wrapper = mount(EmpleadosList, {
      global: {
        components: {
          EmpleadoCard,
          EmpleadoForm,
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
