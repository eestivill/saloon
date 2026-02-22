import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import PagoEmpleadoReport from '../PagoEmpleadoReport.vue';
import { empleadosAPI } from '@/services/api';
import { useEmpleadosStore } from '@/stores/empleados';

// Mock the API
vi.mock('@/services/api', () => ({
  empleadosAPI: {
    listar: vi.fn(),
    obtenerPago: vi.fn(),
  },
}));

describe('PagoEmpleadoReport', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
    
    // Mock empleados list
    vi.mocked(empleadosAPI.listar).mockResolvedValue({
      data: [
        { id: 'E001', nombre: 'Juan Pérez' },
        { id: 'E002', nombre: 'María García' },
      ],
    } as any);
  });

  it('renderiza el título y campos de filtro', () => {
    const wrapper = mount(PagoEmpleadoReport);

    expect(wrapper.text()).toContain('Reporte de Pago a Empleado');
    expect(wrapper.text()).toContain('Empleado');
    expect(wrapper.text()).toContain('Fecha Inicio');
    expect(wrapper.text()).toContain('Fecha Fin');
  });

  it('muestra lista de empleados en el select', async () => {
    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const select = wrapper.find('select');
    expect(select.exists()).toBe(true);
    
    const options = select.findAll('option');
    // +1 por la opción "Seleccione un empleado"
    expect(options.length).toBe(3);
    expect(options[0].text()).toBe('Seleccione un empleado');
    expect(options[1].text()).toBe('Juan Pérez');
    expect(options[2].text()).toBe('María García');
  });

  it('muestra error si no se selecciona empleado al consultar', async () => {
    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    // Hacer clic en consultar sin seleccionar empleado
    const button = wrapper.findAll('button')[0];
    await button.trigger('click');
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Debe seleccionar un empleado');
  });

  it('carga pago del empleado seleccionado', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [
        {
          fecha: '2024-01-15',
          tipo_servicio: 'Corte',
          precio: 25.00,
          comision: 10.00,
        },
      ],
      total: 10.00,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    // Seleccionar empleado
    const select = wrapper.find('select');
    await select.setValue('E001');

    // Consultar
    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));

    expect(empleadosAPI.obtenerPago).toHaveBeenCalledWith('E001', {});
  });

  it('muestra información del empleado y total a pagar', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [
        {
          fecha: '2024-01-15',
          tipo_servicio: 'Corte',
          precio: 25.00,
          comision: 10.00,
        },
      ],
      total: 10.00,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Juan Pérez');
    expect(wrapper.text()).toContain('E001');
    expect(wrapper.text()).toContain('Total a Pagar');
  });

  it('muestra tabla con desglose de servicios', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [
        {
          fecha: '2024-01-15',
          tipo_servicio: 'Corte',
          precio: 25.00,
          comision: 10.00,
        },
        {
          fecha: '2024-01-16',
          tipo_servicio: 'Tinte',
          precio: 50.00,
          comision: 20.00,
        },
      ],
      total: 30.00,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Desglose de Servicios');
    expect(wrapper.text()).toContain('Corte');
    expect(wrapper.text()).toContain('Tinte');
    
    // Verificar que hay una tabla
    const table = wrapper.find('table');
    expect(table.exists()).toBe(true);
  });

  it('muestra encabezados de tabla correctos', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [
        {
          fecha: '2024-01-15',
          tipo_servicio: 'Corte',
          precio: 25.00,
          comision: 10.00,
        },
      ],
      total: 10.00,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const table = wrapper.find('table');
    expect(table.text()).toContain('Fecha');
    expect(table.text()).toContain('Tipo de Servicio');
    expect(table.text()).toContain('Precio');
    expect(table.text()).toContain('Comisión');
  });

  it('muestra mensaje cuando no hay servicios', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [],
      total: 0.00,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('No hay servicios registrados');
  });

  it('aplica filtros de fecha al consultar', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [],
      total: 0.00,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    // Seleccionar empleado
    const select = wrapper.find('select');
    await select.setValue('E001');

    // Establecer fechas
    const inputs = wrapper.findAll('input[type="date"]');
    await inputs[0].setValue('2024-01-01');
    await inputs[1].setValue('2024-01-31');

    // Consultar
    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));

    expect(empleadosAPI.obtenerPago).toHaveBeenCalledWith('E001', {
      fecha_inicio: '2024-01-01',
      fecha_fin: '2024-01-31',
    });
  });

  it('limpia filtros y resultado al hacer clic en "Limpiar"', async () => {
    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    // Seleccionar empleado y establecer fechas
    const select = wrapper.find('select');
    await select.setValue('E001');

    const inputs = wrapper.findAll('input[type="date"]');
    await inputs[0].setValue('2024-01-01');
    await inputs[1].setValue('2024-01-31');

    // Limpiar
    const buttons = wrapper.findAll('button');
    const limpiarButton = buttons[1];
    await limpiarButton.trigger('click');

    // Verificar que los campos están vacíos
    expect((select.element as HTMLSelectElement).value).toBe('');
    expect((inputs[0].element as HTMLInputElement).value).toBe('');
    expect((inputs[1].element as HTMLInputElement).value).toBe('');
  });

  it('muestra mensaje de error cuando falla la carga', async () => {
    vi.mocked(empleadosAPI.obtenerPago).mockRejectedValue({
      response: { data: { detail: 'Error de conexión' } },
    });

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Error');
  });

  it('deshabilita el botón mientras carga', async () => {
    vi.mocked(empleadosAPI.obtenerPago).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve({ 
        data: { empleado_id: 'E001', empleado_nombre: 'Juan', servicios: [], total: 0 } 
      } as any), 1000))
    );

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    
    // Hacer clic para iniciar carga
    await button.trigger('click');
    await wrapper.vm.$nextTick();

    // El botón debe estar deshabilitado
    expect(button.attributes('disabled')).toBeDefined();
  });

  it('formatea valores monetarios correctamente', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [
        {
          fecha: '2024-01-15',
          tipo_servicio: 'Corte',
          precio: 25.50,
          comision: 10.20,
        },
      ],
      total: 10.20,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    // Verificar que se muestra el símbolo de moneda
    expect(wrapper.text()).toContain('$');
  });

  it('aplica estilos responsive correctamente', () => {
    const wrapper = mount(PagoEmpleadoReport);

    const grid = wrapper.find('.grid');
    expect(grid.exists()).toBe(true);
    expect(grid.classes()).toContain('grid-cols-1');
    expect(grid.classes()).toContain('md:grid-cols-3');
  });

  it('muestra vista móvil alternativa para servicios', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [
        {
          fecha: '2024-01-15',
          tipo_servicio: 'Corte',
          precio: 25.00,
          comision: 10.00,
        },
      ],
      total: 10.00,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    // Verificar que existe la vista móvil
    const mobileView = wrapper.find('.md\\:hidden');
    expect(mobileView.exists()).toBe(true);
  });

  it('muestra desglose completo con fecha, tipo, precio y comisión', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [
        {
          fecha: '2024-01-15',
          tipo_servicio: 'Corte Básico',
          precio: 25.00,
          comision: 10.00,
        },
        {
          fecha: '2024-01-20',
          tipo_servicio: 'Tinte Completo',
          precio: 80.00,
          comision: 28.00,
        },
      ],
      total: 38.00,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const text = wrapper.text();
    // Verificar que muestra todos los elementos del desglose
    expect(text).toContain('Corte Básico');
    expect(text).toContain('Tinte Completo');
    expect(text).toContain('25');
    expect(text).toContain('80');
    expect(text).toContain('10');
    expect(text).toContain('28');
    expect(text).toContain('38');
  });

  it('formatea valores monetarios en el desglose con símbolo y decimales', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [
        {
          fecha: '2024-01-15',
          tipo_servicio: 'Corte',
          precio: 1234.56,
          comision: 493.82,
        },
      ],
      total: 493.82,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const text = wrapper.text();
    // Verificar que contiene el símbolo de moneda ($)
    expect(text).toContain('$');
    // Verificar formato con decimales
    expect(text).toMatch(/1.*234.*56/);
    expect(text).toMatch(/493.*82/);
  });

  it('formatea el total a pagar con formato monetario apropiado', async () => {
    const mockDesglose = {
      empleado_id: 'E001',
      empleado_nombre: 'Juan Pérez',
      servicios: [
        {
          fecha: '2024-01-15',
          tipo_servicio: 'Corte',
          precio: 25.00,
          comision: 10.00,
        },
      ],
      total: 10.00,
    };

    vi.mocked(empleadosAPI.obtenerPago).mockResolvedValue({ data: mockDesglose } as any);

    const wrapper = mount(PagoEmpleadoReport);

    await new Promise(resolve => setTimeout(resolve, 100));

    const select = wrapper.find('select');
    await select.setValue('E001');

    const button = wrapper.findAll('button')[0];
    await button.trigger('click');

    await new Promise(resolve => setTimeout(resolve, 100));
    await wrapper.vm.$nextTick();

    const text = wrapper.text();
    // Verificar que el total tiene formato monetario
    expect(text).toContain('Total a Pagar');
    expect(text).toContain('$');
    expect(text).toMatch(/10[.,]00/);
  });
});
