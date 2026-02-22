import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import ServiciosList from '../ServiciosList.vue';
import { useServiciosStore } from '@/stores/servicios';
import { useEmpleadosStore } from '@/stores/empleados';
import ServicioCard from '../ServicioCard.vue';
import ServicioForm from '../ServicioForm.vue';
import ServicioFilters from '../ServicioFilters.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';

// Mock the API
vi.mock('@/services/api', () => ({
  serviciosAPI: {
    listar: vi.fn(() => Promise.resolve({ data: [] })),
    crear: vi.fn(),
    eliminar: vi.fn(),
  },
  empleadosAPI: {
    listar: vi.fn(() => Promise.resolve({ data: [] })),
  },
  tiposServiciosAPI: {
    listar: vi.fn(() => Promise.resolve({ data: [] })),
  },
}));

describe('ServiciosList', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('muestra spinner mientras carga', () => {
    const store = useServiciosStore();
    store.loading = true;

    const wrapper = mount(ServiciosList, {
      global: {
        components: {
          ServicioCard,
          ServicioForm,
          ServicioFilters,
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
    const store = useServiciosStore();
    store.loading = false;
    store.error = 'Error al cargar servicios';

    const wrapper = mount(ServiciosList, {
      global: {
        components: {
          ServicioCard,
          ServicioForm,
          ServicioFilters,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.findComponent(ErrorMessage).exists()).toBe(true);
    expect(wrapper.text()).toContain('Error al cargar servicios');
  });

  it('muestra mensaje cuando no hay servicios', () => {
    const store = useServiciosStore();
    store.loading = false;
    store.error = null;
    store.servicios = [];

    const wrapper = mount(ServiciosList, {
      global: {
        components: {
          ServicioCard,
          ServicioForm,
          ServicioFilters,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.text()).toContain('No hay servicios registrados');
  });

  it('muestra servicios correctamente', () => {
    const store = useServiciosStore();
    const empleadosStore = useEmpleadosStore();
    
    store.loading = false;
    store.error = null;
    store.servicios = [
      {
        id: 'S001',
        fecha: '2024-01-15',
        empleado_id: 'E001',
        tipo_servicio: 'Corte',
        precio: 25.0,
        comision_calculada: 10.0,
      },
      {
        id: 'S002',
        fecha: '2024-01-16',
        empleado_id: 'E002',
        tipo_servicio: 'Tinte',
        precio: 50.0,
        comision_calculada: 17.5,
      },
    ];

    empleadosStore.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
      { id: 'E002', nombre: 'María García' },
    ];

    const wrapper = mount(ServiciosList, {
      global: {
        components: {
          ServicioCard,
          ServicioForm,
          ServicioFilters,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    // En móvil muestra cards
    const cards = wrapper.findAllComponents(ServicioCard);
    expect(cards.length).toBeGreaterThan(0);
  });

  it('ordena servicios por fecha descendente', () => {
    const store = useServiciosStore();
    store.loading = false;
    store.error = null;
    store.servicios = [
      {
        id: 'S001',
        fecha: '2024-01-15',
        empleado_id: 'E001',
        tipo_servicio: 'Corte',
        precio: 25.0,
        comision_calculada: 10.0,
      },
      {
        id: 'S002',
        fecha: '2024-01-20',
        empleado_id: 'E002',
        tipo_servicio: 'Tinte',
        precio: 50.0,
        comision_calculada: 17.5,
      },
      {
        id: 'S003',
        fecha: '2024-01-10',
        empleado_id: 'E001',
        tipo_servicio: 'Peinado',
        precio: 30.0,
        comision_calculada: 12.0,
      },
    ];

    const wrapper = mount(ServiciosList, {
      global: {
        components: {
          ServicioCard,
          ServicioForm,
          ServicioFilters,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    const cards = wrapper.findAllComponents(ServicioCard);
    
    // Verificar que el primer servicio es el más reciente (2024-01-20)
    expect(cards[0].props('servicio').id).toBe('S002');
    // El segundo es 2024-01-15
    expect(cards[1].props('servicio').id).toBe('S001');
    // El tercero es 2024-01-10
    expect(cards[2].props('servicio').id).toBe('S003');
  });

  it('muestra botón "Registrar Servicio"', () => {
    const store = useServiciosStore();
    store.loading = false;
    store.error = null;
    store.servicios = [];

    const wrapper = mount(ServiciosList, {
      global: {
        components: {
          ServicioCard,
          ServicioForm,
          ServicioFilters,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.text()).toContain('Registrar Servicio');
  });

  it('muestra formulario cuando se hace clic en "Registrar Servicio"', async () => {
    const store = useServiciosStore();
    store.loading = false;
    store.error = null;
    store.servicios = [];

    const wrapper = mount(ServiciosList, {
      global: {
        components: {
          ServicioCard,
          ServicioForm,
          ServicioFilters,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    const button = wrapper.find('button');
    await button.trigger('click');

    expect(wrapper.findComponent(ServicioForm).exists()).toBe(true);
  });

  it('muestra componente de filtros', () => {
    const store = useServiciosStore();
    store.loading = false;
    store.error = null;
    store.servicios = [];

    const wrapper = mount(ServiciosList, {
      global: {
        components: {
          ServicioCard,
          ServicioForm,
          ServicioFilters,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    expect(wrapper.findComponent(ServicioFilters).exists()).toBe(true);
  });

  it('muestra tabla en pantallas grandes y cards en móvil', () => {
    const store = useServiciosStore();
    store.loading = false;
    store.error = null;
    store.servicios = [
      {
        id: 'S001',
        fecha: '2024-01-15',
        empleado_id: 'E001',
        tipo_servicio: 'Corte',
        precio: 25.0,
        comision_calculada: 10.0,
      },
    ];

    const wrapper = mount(ServiciosList, {
      global: {
        components: {
          ServicioCard,
          ServicioForm,
          ServicioFilters,
          LoadingSpinner,
          ErrorMessage,
        },
        stubs: {
          teleport: true,
        },
      },
    });

    // Tabla para desktop (hidden en móvil)
    const table = wrapper.find('table');
    expect(table.exists()).toBe(true);
    expect(table.classes()).toContain('min-w-full');

    // Grid de cards para móvil (hidden en desktop)
    const mobileGrid = wrapper.find('.md\\:hidden');
    expect(mobileGrid.exists()).toBe(true);
  });
});
