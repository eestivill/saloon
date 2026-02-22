import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import ServicioCard from '../ServicioCard.vue';
import { useEmpleadosStore } from '@/stores/empleados';
import type { Servicio } from '@/types/models';

// Mock the API
vi.mock('@/services/api', () => ({
  empleadosAPI: {
    listar: vi.fn(() => Promise.resolve({ data: [] })),
  },
}));

describe('ServicioCard', () => {
  const mockServicio: Servicio = {
    id: 'S001',
    fecha: '2024-01-15',
    empleado_id: 'E001',
    tipo_servicio: 'Corte Básico',
    precio: 25.50,
    comision_calculada: 10.20,
  };

  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('muestra información del servicio correctamente', () => {
    const empleadosStore = useEmpleadosStore();
    empleadosStore.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
    ];

    const wrapper = mount(ServicioCard, {
      props: {
        servicio: mockServicio,
      },
    });

    expect(wrapper.text()).toContain('Corte Básico');
    expect(wrapper.text()).toContain('Juan Pérez');
    expect(wrapper.text()).toContain('$25.50');
    expect(wrapper.text()).toContain('$10.20');
  });

  it('formatea la fecha correctamente', () => {
    const wrapper = mount(ServicioCard, {
      props: {
        servicio: mockServicio,
      },
    });

    // La fecha debe estar formateada en español
    const text = wrapper.text();
    expect(text).toMatch(/ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic/i);
  });

  it('muestra el ID del empleado si no se encuentra el nombre', () => {
    const empleadosStore = useEmpleadosStore();
    empleadosStore.empleados = []; // Sin empleados

    const wrapper = mount(ServicioCard, {
      props: {
        servicio: mockServicio,
      },
    });

    expect(wrapper.text()).toContain('E001');
  });

  it('muestra el precio con dos decimales', () => {
    const wrapper = mount(ServicioCard, {
      props: {
        servicio: {
          ...mockServicio,
          precio: 25,
        },
      },
    });

    expect(wrapper.text()).toContain('$25.00');
  });

  it('muestra la comisión con dos decimales', () => {
    const wrapper = mount(ServicioCard, {
      props: {
        servicio: {
          ...mockServicio,
          comision_calculada: 10,
        },
      },
    });

    expect(wrapper.text()).toContain('$10.00');
  });

  it('emite evento eliminar al hacer clic en el botón', async () => {
    const wrapper = mount(ServicioCard, {
      props: {
        servicio: mockServicio,
      },
    });

    const button = wrapper.find('button');
    await button.trigger('click');

    expect(wrapper.emitted('eliminar')).toBeTruthy();
    expect(wrapper.emitted('eliminar')?.[0]).toEqual(['S001']);
  });

  it('muestra botón de eliminar', () => {
    const wrapper = mount(ServicioCard, {
      props: {
        servicio: mockServicio,
      },
    });

    const button = wrapper.find('button');
    expect(button.exists()).toBe(true);
    expect(button.text()).toBe('Eliminar');
  });

  it('aplica estilos de tarjeta correctamente', () => {
    const wrapper = mount(ServicioCard, {
      props: {
        servicio: mockServicio,
      },
    });

    const card = wrapper.find('.bg-white.rounded-lg.shadow-md');
    expect(card.exists()).toBe(true);
  });

  it('muestra todos los campos requeridos', () => {
    const empleadosStore = useEmpleadosStore();
    empleadosStore.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
    ];

    const wrapper = mount(ServicioCard, {
      props: {
        servicio: mockServicio,
      },
    });

    // Verificar que muestra todos los campos
    expect(wrapper.text()).toContain('Empleado:');
    expect(wrapper.text()).toContain('Precio:');
    expect(wrapper.text()).toContain('Comisión:');
  });

  it('maneja precios grandes correctamente', () => {
    const wrapper = mount(ServicioCard, {
      props: {
        servicio: {
          ...mockServicio,
          precio: 1234.56,
          comision_calculada: 432.10,
        },
      },
    });

    expect(wrapper.text()).toContain('$1234.56');
    expect(wrapper.text()).toContain('$432.10');
  });

  it('maneja precios pequeños correctamente', () => {
    const wrapper = mount(ServicioCard, {
      props: {
        servicio: {
          ...mockServicio,
          precio: 0.50,
          comision_calculada: 0.20,
        },
      },
    });

    expect(wrapper.text()).toContain('$0.50');
    expect(wrapper.text()).toContain('$0.20');
  });
});
