import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import IngresosReport from '../IngresosReport.vue';
import { reportesAPI } from '@/services/api';

// Mock the API
vi.mock('@/services/api', () => ({
  reportesAPI: {
    ingresos: vi.fn(),
  },
}));

describe('IngresosReport', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('renderiza el título y campos de filtro', () => {
    const wrapper = mount(IngresosReport);

    expect(wrapper.text()).toContain('Reporte de Ingresos');
    expect(wrapper.text()).toContain('Fecha Inicio');
    expect(wrapper.text()).toContain('Fecha Fin');
  });

  it('carga ingresos al montar el componente', async () => {
    const mockIngresos = {
      total: 1500.50,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.ingresos).mockResolvedValue({ data: mockIngresos } as any);

    const wrapper = mount(IngresosReport);

    // Esperar a que se complete la carga
    await new Promise(resolve => setTimeout(resolve, 100));

    expect(reportesAPI.ingresos).toHaveBeenCalledWith({});
  });

  it('muestra el total de ingresos con formato monetario', async () => {
    const mockIngresos = {
      total: 1500.50,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.ingresos).mockResolvedValue({ data: mockIngresos } as any);

    const wrapper = mount(IngresosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    // Verificar que el total se muestra con formato de moneda
    expect(wrapper.text()).toContain('$');
    expect(wrapper.text()).toContain('1');
    expect(wrapper.text()).toContain('500');
  });

  it('aplica filtros de fecha al consultar', async () => {
    const mockIngresos = {
      total: 800.00,
      fecha_inicio: '2024-01-01',
      fecha_fin: '2024-01-31',
    };

    vi.mocked(reportesAPI.ingresos).mockResolvedValue({ data: mockIngresos } as any);

    const wrapper = mount(IngresosReport);

    // Establecer fechas
    const inputs = wrapper.findAll('input[type="date"]');
    await inputs[0].setValue('2024-01-01');
    await inputs[1].setValue('2024-01-31');

    // Hacer clic en consultar
    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));

    expect(reportesAPI.ingresos).toHaveBeenCalledWith({
      fecha_inicio: '2024-01-01',
      fecha_fin: '2024-01-31',
    });
  });

  it('limpia filtros y resultado al hacer clic en "Limpiar"', async () => {
    const mockIngresos = {
      total: 1500.50,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.ingresos).mockResolvedValue({ data: mockIngresos } as any);

    const wrapper = mount(IngresosReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    // Establecer fechas
    const inputs = wrapper.findAll('input[type="date"]');
    await inputs[0].setValue('2024-01-01');
    await inputs[1].setValue('2024-01-31');

    // Limpiar
    const buttons = wrapper.findAll('button');
    const limpiarButton = buttons[1];
    await limpiarButton.trigger('click');

    // Verificar que los campos están vacíos
    expect((inputs[0].element as HTMLInputElement).value).toBe('');
    expect((inputs[1].element as HTMLInputElement).value).toBe('');
  });

  it('muestra mensaje de error cuando falla la carga', async () => {
    vi.mocked(reportesAPI.ingresos).mockRejectedValue({
      response: { data: { detail: 'Error de conexión' } },
    });

    const wrapper = mount(IngresosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Error');
  });

  it('deshabilita el botón mientras carga', async () => {
    vi.mocked(reportesAPI.ingresos).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve({ data: { total: 100 } } as any), 1000))
    );

    const wrapper = mount(IngresosReport);

    const button = wrapper.findAll('button')[0];
    
    // Hacer clic para iniciar carga
    await button.trigger('click');
    await wrapper.vm.$nextTick();

    // El botón debe estar deshabilitado
    expect(button.attributes('disabled')).toBeDefined();
  });

  it('muestra "Total General" cuando no hay filtros', async () => {
    const mockIngresos = {
      total: 1500.50,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.ingresos).mockResolvedValue({ data: mockIngresos } as any);

    const wrapper = mount(IngresosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Total General');
  });

  it('muestra período cuando hay filtros de fecha', async () => {
    const mockIngresos = {
      total: 800.00,
      fecha_inicio: '2024-01-01',
      fecha_fin: '2024-01-31',
    };

    vi.mocked(reportesAPI.ingresos).mockResolvedValue({ data: mockIngresos } as any);

    const wrapper = mount(IngresosReport);

    // Establecer fechas
    const inputs = wrapper.findAll('input[type="date"]');
    await inputs[0].setValue('2024-01-01');
    await inputs[1].setValue('2024-01-31');

    // Consultar
    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Período');
  });

  it('aplica estilos responsive correctamente', () => {
    const wrapper = mount(IngresosReport);

    const grid = wrapper.find('.grid');
    expect(grid.exists()).toBe(true);
    expect(grid.classes()).toContain('grid-cols-1');
    expect(grid.classes()).toContain('md:grid-cols-2');
  });

  it('formatea valores monetarios con símbolo de moneda y decimales', async () => {
    const mockIngresos = {
      total: 1234.56,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.ingresos).mockResolvedValue({ data: mockIngresos } as any);

    const wrapper = mount(IngresosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const text = wrapper.text();
    // Verificar que contiene el símbolo de moneda ($)
    expect(text).toContain('$');
    // Verificar que contiene los decimales
    expect(text).toMatch(/1.*234.*56/);
  });

  it('formatea valores monetarios con separadores de miles', async () => {
    const mockIngresos = {
      total: 12345.67,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.ingresos).mockResolvedValue({ data: mockIngresos } as any);

    const wrapper = mount(IngresosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const text = wrapper.text();
    // Verificar formato con separadores (puede ser . o , dependiendo del locale)
    expect(text).toMatch(/12[.,]345/);
  });

  it('formatea valores monetarios con dos decimales', async () => {
    const mockIngresos = {
      total: 100.5,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.ingresos).mockResolvedValue({ data: mockIngresos } as any);

    const wrapper = mount(IngresosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const text = wrapper.text();
    // Verificar que muestra dos decimales (100.50)
    expect(text).toMatch(/100[.,]50/);
  });
});
