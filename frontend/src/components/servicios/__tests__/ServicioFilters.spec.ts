import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import ServicioFilters from '../ServicioFilters.vue';
import { useEmpleadosStore } from '@/stores/empleados';

// Mock the API
vi.mock('@/services/api', () => ({
  empleadosAPI: {
    listar: vi.fn(() => Promise.resolve({ data: [] })),
  },
}));

describe('ServicioFilters', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('renderiza todos los campos de filtro', () => {
    const wrapper = mount(ServicioFilters);

    expect(wrapper.text()).toContain('Empleado');
    expect(wrapper.text()).toContain('Fecha Inicio');
    expect(wrapper.text()).toContain('Fecha Fin');
  });

  it('muestra lista de empleados en el select', () => {
    const empleadosStore = useEmpleadosStore();
    empleadosStore.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
      { id: 'E002', nombre: 'María García' },
    ];

    const wrapper = mount(ServicioFilters);

    const select = wrapper.find('select');
    expect(select.exists()).toBe(true);
    
    const options = select.findAll('option');
    // +1 por la opción "Todos los empleados"
    expect(options.length).toBe(3);
    expect(options[0].text()).toBe('Todos los empleados');
    expect(options[1].text()).toBe('Juan Pérez');
    expect(options[2].text()).toBe('María García');
  });

  it('emite evento filtrar con filtros vacíos al inicio', async () => {
    const wrapper = mount(ServicioFilters);

    const button = wrapper.find('button');
    await button.trigger('click');

    expect(wrapper.emitted('filtrar')).toBeTruthy();
    expect(wrapper.emitted('filtrar')?.[0]).toEqual([{}]);
  });

  it('emite evento filtrar con empleado seleccionado', async () => {
    const empleadosStore = useEmpleadosStore();
    empleadosStore.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
    ];

    const wrapper = mount(ServicioFilters);

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    expect(wrapper.emitted('filtrar')).toBeTruthy();
    const emittedFilters = wrapper.emitted('filtrar')?.[0]?.[0] as any;
    expect(emittedFilters.empleado_id).toBe('E001');
  });

  it('emite evento filtrar con rango de fechas', async () => {
    const wrapper = mount(ServicioFilters);

    const inputs = wrapper.findAll('input[type="date"]');
    await inputs[0].setValue('2024-01-01');
    await inputs[1].setValue('2024-01-31');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    expect(wrapper.emitted('filtrar')).toBeTruthy();
    const emittedFilters = wrapper.emitted('filtrar')?.[0]?.[0] as any;
    expect(emittedFilters.fecha_inicio).toBe('2024-01-01');
    expect(emittedFilters.fecha_fin).toBe('2024-01-31');
  });

  it('emite evento filtrar con todos los filtros combinados', async () => {
    const empleadosStore = useEmpleadosStore();
    empleadosStore.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
    ];

    const wrapper = mount(ServicioFilters);

    const select = wrapper.find('select');
    await select.setValue('E001');

    const inputs = wrapper.findAll('input[type="date"]');
    await inputs[0].setValue('2024-01-01');
    await inputs[1].setValue('2024-01-31');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    expect(wrapper.emitted('filtrar')).toBeTruthy();
    const emittedFilters = wrapper.emitted('filtrar')?.[0]?.[0] as any;
    expect(emittedFilters.empleado_id).toBe('E001');
    expect(emittedFilters.fecha_inicio).toBe('2024-01-01');
    expect(emittedFilters.fecha_fin).toBe('2024-01-31');
  });

  it('limpia filtros al hacer clic en "Limpiar"', async () => {
    const empleadosStore = useEmpleadosStore();
    empleadosStore.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
    ];

    const wrapper = mount(ServicioFilters);

    // Establecer filtros
    const select = wrapper.find('select');
    await select.setValue('E001');

    const inputs = wrapper.findAll('input[type="date"]');
    await inputs[0].setValue('2024-01-01');
    await inputs[1].setValue('2024-01-31');

    // Limpiar filtros
    const buttons = wrapper.findAll('button');
    const limpiarButton = buttons[1]; // El segundo botón es "Limpiar"
    await limpiarButton.trigger('click');

    expect(wrapper.emitted('filtrar')).toBeTruthy();
    // El último evento emitido debe ser con filtros vacíos
    const lastEmitted = wrapper.emitted('filtrar')?.slice(-1)[0]?.[0] as any;
    expect(lastEmitted).toEqual({});

    // Verificar que los campos están vacíos
    expect((select.element as HTMLSelectElement).value).toBe('');
    expect((inputs[0].element as HTMLInputElement).value).toBe('');
    expect((inputs[1].element as HTMLInputElement).value).toBe('');
  });

  it('muestra botones "Aplicar Filtros" y "Limpiar"', () => {
    const wrapper = mount(ServicioFilters);

    const buttons = wrapper.findAll('button');
    expect(buttons.length).toBe(2);
    expect(buttons[0].text()).toBe('Aplicar Filtros');
    expect(buttons[1].text()).toBe('Limpiar');
  });

  it('aplica estilos responsive correctamente', () => {
    const wrapper = mount(ServicioFilters);

    const grid = wrapper.find('.grid');
    expect(grid.exists()).toBe(true);
    expect(grid.classes()).toContain('grid-cols-1');
    expect(grid.classes()).toContain('md:grid-cols-3');
  });
});
