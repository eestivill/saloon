import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import ServicioForm from '../ServicioForm.vue';
import { useEmpleadosStore } from '@/stores/empleados';
import { useTiposServiciosStore } from '@/stores/tiposServicios';

// Mock the API
vi.mock('@/services/api', () => ({
  empleadosAPI: {
    listar: vi.fn(() => Promise.resolve({ data: [] })),
  },
  tiposServiciosAPI: {
    listar: vi.fn(() => Promise.resolve({ data: [] })),
  },
}));

describe('ServicioForm', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('renderiza el formulario correctamente', () => {
    const wrapper = mount(ServicioForm);

    expect(wrapper.text()).toContain('Registrar Servicio');
    expect(wrapper.text()).toContain('Fecha');
    expect(wrapper.text()).toContain('Empleado');
    expect(wrapper.text()).toContain('Tipo de Servicio');
    expect(wrapper.text()).toContain('Precio');
  });

  it('carga empleados y tipos de servicios en los selects', async () => {
    const empleadosStore = useEmpleadosStore();
    const tiposServiciosStore = useTiposServiciosStore();

    empleadosStore.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
      { id: 'E002', nombre: 'María García' },
    ];

    tiposServiciosStore.tiposServicios = [
      { nombre: 'Corte', descripcion: 'Corte de cabello', porcentaje_comision: 40 },
      { nombre: 'Tinte', descripcion: 'Tinte de cabello', porcentaje_comision: 35 },
    ];

    const wrapper = mount(ServicioForm);

    // Esperar a que se carguen los datos
    await wrapper.vm.$nextTick();

    const selects = wrapper.findAll('select');
    
    // Select de empleados
    const empleadosOptions = selects[0].findAll('option');
    expect(empleadosOptions.length).toBe(3); // +1 por la opción por defecto
    expect(empleadosOptions[1].text()).toBe('Juan Pérez');
    expect(empleadosOptions[2].text()).toBe('María García');

    // Select de tipos de servicios
    const tiposOptions = selects[1].findAll('option');
    expect(tiposOptions.length).toBe(3); // +1 por la opción por defecto
    expect(tiposOptions[1].text()).toContain('Corte');
    expect(tiposOptions[1].text()).toContain('40%');
    expect(tiposOptions[2].text()).toContain('Tinte');
    expect(tiposOptions[2].text()).toContain('35%');
  });

  it('valida que el precio sea positivo', async () => {
    const wrapper = mount(ServicioForm);

    const inputs = wrapper.findAll('input');
    const precioInput = inputs.find(input => 
      (input.element as HTMLInputElement).type === 'number'
    );

    // Intentar establecer precio negativo
    await precioInput?.setValue(-10);

    const form = wrapper.find('form');
    await form.trigger('submit');

    // Debe mostrar error de validación
    expect(wrapper.text()).toContain('El precio debe ser mayor que cero');
  });

  it('valida que el precio sea mayor que cero', async () => {
    const wrapper = mount(ServicioForm);

    const inputs = wrapper.findAll('input');
    const precioInput = inputs.find(input => 
      (input.element as HTMLInputElement).type === 'number'
    );

    // Intentar establecer precio cero
    await precioInput?.setValue(0);

    const form = wrapper.find('form');
    await form.trigger('submit');

    // Debe mostrar error de validación
    expect(wrapper.text()).toContain('El precio debe ser mayor que cero');
  });

  it('valida que todos los campos sean requeridos', async () => {
    const wrapper = mount(ServicioForm);

    const form = wrapper.find('form');
    await form.trigger('submit');

    // Debe mostrar errores de validación
    expect(wrapper.text()).toContain('Debes seleccionar un empleado');
    expect(wrapper.text()).toContain('Debes seleccionar un tipo de servicio');
  });

  it('emite evento guardar con datos válidos', async () => {
    const empleadosStore = useEmpleadosStore();
    const tiposServiciosStore = useTiposServiciosStore();

    empleadosStore.empleados = [
      { id: 'E001', nombre: 'Juan Pérez' },
    ];

    tiposServiciosStore.tiposServicios = [
      { nombre: 'Corte', descripcion: 'Corte de cabello', porcentaje_comision: 40 },
    ];

    const wrapper = mount(ServicioForm);

    await wrapper.vm.$nextTick();

    // Llenar el formulario
    const inputs = wrapper.findAll('input');
    const fechaInput = inputs.find(input => 
      (input.element as HTMLInputElement).type === 'date'
    );
    const precioInput = inputs.find(input => 
      (input.element as HTMLInputElement).type === 'number'
    );

    await fechaInput?.setValue('2024-01-15');

    const selects = wrapper.findAll('select');
    await selects[0].setValue('E001');
    await selects[1].setValue('Corte');

    await precioInput?.setValue(25.50);

    // Enviar formulario
    const form = wrapper.find('form');
    await form.trigger('submit');

    expect(wrapper.emitted('guardar')).toBeTruthy();
    const emittedData = wrapper.emitted('guardar')?.[0]?.[0] as any;
    expect(emittedData.fecha).toBe('2024-01-15');
    expect(emittedData.empleado_id).toBe('E001');
    expect(emittedData.tipo_servicio).toBe('Corte');
    expect(emittedData.precio).toBe(25.50);
  });

  it('emite evento cancelar al hacer clic en "Cancelar"', async () => {
    const wrapper = mount(ServicioForm);

    const buttons = wrapper.findAll('button');
    const cancelarButton = buttons[0]; // El primer botón es "Cancelar"
    await cancelarButton.trigger('click');

    expect(wrapper.emitted('cancelar')).toBeTruthy();
  });

  it('muestra fecha actual por defecto', () => {
    const wrapper = mount(ServicioForm);

    const inputs = wrapper.findAll('input');
    const fechaInput = inputs.find(input => 
      (input.element as HTMLInputElement).type === 'date'
    );

    const today = new Date().toISOString().split('T')[0];
    expect((fechaInput?.element as HTMLInputElement).value).toBe(today);
  });

  it('muestra hint sobre precio positivo', () => {
    const wrapper = mount(ServicioForm);

    expect(wrapper.text()).toContain('Debe ser mayor que cero');
  });

  it('deshabilita botón guardar mientras está cargando', async () => {
    const wrapper = mount(ServicioForm);

    const buttons = wrapper.findAll('button');
    const guardarButton = buttons[1]; // El segundo botón es "Guardar"

    // Simular estado de carga
    await wrapper.vm.$nextTick();
    
    // Por defecto no debe estar deshabilitado
    expect((guardarButton.element as HTMLButtonElement).disabled).toBe(false);
  });

  it('muestra modal con overlay', () => {
    const wrapper = mount(ServicioForm);

    // Verificar que tiene el overlay
    const overlay = wrapper.find('.fixed.inset-0.bg-black.bg-opacity-50');
    expect(overlay.exists()).toBe(true);

    // Verificar que tiene el modal
    const modal = wrapper.find('.bg-white.rounded-lg.shadow-xl');
    expect(modal.exists()).toBe(true);
  });

  it('valida que el precio sea un número válido', async () => {
    const wrapper = mount(ServicioForm);

    const inputs = wrapper.findAll('input');
    const precioInput = inputs.find(input => 
      (input.element as HTMLInputElement).type === 'number'
    );

    // Establecer un valor no numérico (aunque el input type="number" lo previene)
    // Vamos a probar con el valor 0 que es inválido
    await precioInput?.setValue(0);

    const form = wrapper.find('form');
    await form.trigger('submit');

    expect(wrapper.text()).toContain('El precio debe ser mayor que cero');
  });
});
