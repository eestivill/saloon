import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import BeneficiosReport from '../BeneficiosReport.vue';
import { reportesAPI } from '@/services/api';

// Mock the API
vi.mock('@/services/api', () => ({
  reportesAPI: {
    beneficios: vi.fn(),
  },
}));

describe('BeneficiosReport', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('renderiza el título y campos de filtro', () => {
    const wrapper = mount(BeneficiosReport);

    expect(wrapper.text()).toContain('Reporte de Beneficios');
    expect(wrapper.text()).toContain('Fecha Inicio');
    expect(wrapper.text()).toContain('Fecha Fin');
  });

  it('carga beneficios al montar el componente', async () => {
    const mockBeneficios = {
      ingresos: 2000.00,
      comisiones: 800.00,
      beneficios: 1200.00,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    expect(reportesAPI.beneficios).toHaveBeenCalledWith({});
  });

  it('muestra ingresos, comisiones y beneficios con formato monetario', async () => {
    const mockBeneficios = {
      ingresos: 2000.00,
      comisiones: 800.00,
      beneficios: 1200.00,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Ingresos');
    expect(wrapper.text()).toContain('Comisiones');
    expect(wrapper.text()).toContain('Beneficios');
    expect(wrapper.text()).toContain('$');
  });

  it('muestra las tres tarjetas de métricas', async () => {
    const mockBeneficios = {
      ingresos: 2000.00,
      comisiones: 800.00,
      beneficios: 1200.00,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    // Verificar que hay tres tarjetas de métricas
    const cards = wrapper.findAll('.bg-blue-50, .bg-orange-50, .bg-green-50');
    expect(cards.length).toBeGreaterThanOrEqual(3);
  });

  it('muestra desglose detallado', async () => {
    const mockBeneficios = {
      ingresos: 2000.00,
      comisiones: 800.00,
      beneficios: 1200.00,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Desglose');
    expect(wrapper.text()).toContain('Ingresos Totales');
    expect(wrapper.text()).toContain('Comisiones Pagadas');
    expect(wrapper.text()).toContain('Beneficio Neto');
  });

  it('calcula y muestra el margen de beneficio', async () => {
    const mockBeneficios = {
      ingresos: 2000.00,
      comisiones: 800.00,
      beneficios: 1200.00,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Margen de Beneficio');
    // Margen = (1200 / 2000) * 100 = 60%
    expect(wrapper.text()).toContain('60');
  });

  it('aplica filtros de fecha al consultar', async () => {
    const mockBeneficios = {
      ingresos: 1500.00,
      comisiones: 600.00,
      beneficios: 900.00,
      fecha_inicio: '2024-01-01',
      fecha_fin: '2024-01-31',
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    // Establecer fechas
    const inputs = wrapper.findAll('input[type="date"]');
    await inputs[0].setValue('2024-01-01');
    await inputs[1].setValue('2024-01-31');

    // Consultar
    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));

    expect(reportesAPI.beneficios).toHaveBeenCalledWith({
      fecha_inicio: '2024-01-01',
      fecha_fin: '2024-01-31',
    });
  });

  it('limpia filtros y resultado al hacer clic en "Limpiar"', async () => {
    const mockBeneficios = {
      ingresos: 2000.00,
      comisiones: 800.00,
      beneficios: 1200.00,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

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
    vi.mocked(reportesAPI.beneficios).mockRejectedValue({
      response: { data: { detail: 'Error de conexión' } },
    });

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Error');
  });

  it('deshabilita el botón mientras carga', async () => {
    vi.mocked(reportesAPI.beneficios).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve({ 
        data: { ingresos: 100, comisiones: 40, beneficios: 60 } 
      } as any), 1000))
    );

    const wrapper = mount(BeneficiosReport);

    const button = wrapper.findAll('button')[0];
    
    // Hacer clic para iniciar carga
    await button.trigger('click');
    await wrapper.vm.$nextTick();

    // El botón debe estar deshabilitado
    expect(button.attributes('disabled')).toBeDefined();
  });

  it('muestra color verde para margen alto (>= 50%)', async () => {
    const mockBeneficios = {
      ingresos: 2000.00,
      comisiones: 800.00,
      beneficios: 1200.00, // 60% margen
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const html = wrapper.html();
    expect(html).toContain('text-green-600');
  });

  it('aplica estilos responsive correctamente', () => {
    const wrapper = mount(BeneficiosReport);

    const grid = wrapper.find('.grid');
    expect(grid.exists()).toBe(true);
    expect(grid.classes()).toContain('grid-cols-1');
    expect(grid.classes()).toContain('md:grid-cols-2');
  });

  it('muestra "Total General" cuando no hay filtros', async () => {
    const mockBeneficios = {
      ingresos: 2000.00,
      comisiones: 800.00,
      beneficios: 1200.00,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Total General');
  });

  it('calcula beneficios correctamente como ingresos menos comisiones', async () => {
    const mockBeneficios = {
      ingresos: 5000.00,
      comisiones: 2000.00,
      beneficios: 3000.00,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const text = wrapper.text();
    // Verificar que muestra los tres valores
    expect(text).toContain('5');
    expect(text).toContain('000');
    expect(text).toContain('2');
    expect(text).toContain('3');
  });

  it('formatea valores monetarios con símbolo de moneda y decimales', async () => {
    const mockBeneficios = {
      ingresos: 1234.56,
      comisiones: 234.56,
      beneficios: 1000.00,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const text = wrapper.text();
    // Verificar que contiene el símbolo de moneda ($)
    expect(text).toContain('$');
    // Verificar que contiene decimales
    expect(text).toMatch(/1.*234.*56/);
  });

  it('formatea valores monetarios con separadores de miles', async () => {
    const mockBeneficios = {
      ingresos: 12345.67,
      comisiones: 5000.00,
      beneficios: 7345.67,
      fecha_inicio: null,
      fecha_fin: null,
    };

    vi.mocked(reportesAPI.beneficios).mockResolvedValue({ data: mockBeneficios } as any);

    const wrapper = mount(BeneficiosReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const text = wrapper.text();
    // Verificar formato con separadores
    expect(text).toMatch(/12[.,]345/);
  });
});
