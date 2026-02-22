import { describe, it, expect, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import EmpleadoForm from '../EmpleadoForm.vue';
import type { Empleado } from '@/types/models';

describe('EmpleadoForm', () => {
  it('muestra título "Nuevo Empleado" cuando no hay empleado', () => {
    const wrapper = mount(EmpleadoForm);
    expect(wrapper.text()).toContain('Nuevo Empleado');
  });

  it('muestra título "Editar Empleado" cuando hay empleado', () => {
    const mockEmpleado: Empleado = {
      id: 'E001',
      nombre: 'Juan Pérez',
    };

    const wrapper = mount(EmpleadoForm, {
      props: {
        empleado: mockEmpleado,
      },
    });

    expect(wrapper.text()).toContain('Editar Empleado');
  });

  it('carga datos del empleado en modo edición', async () => {
    const mockEmpleado: Empleado = {
      id: 'E001',
      nombre: 'Juan Pérez',
    };

    const wrapper = mount(EmpleadoForm, {
      props: {
        empleado: mockEmpleado,
      },
    });

    // Wait for onMounted to complete
    await wrapper.vm.$nextTick();

    const inputs = wrapper.findAll('input');
    expect((inputs[0].element as HTMLInputElement).value).toBe('E001');
    expect((inputs[1].element as HTMLInputElement).value).toBe('Juan Pérez');
  });

  it('deshabilita el campo ID en modo edición', () => {
    const mockEmpleado: Empleado = {
      id: 'E001',
      nombre: 'Juan Pérez',
    };

    const wrapper = mount(EmpleadoForm, {
      props: {
        empleado: mockEmpleado,
      },
    });

    const idInput = wrapper.findAll('input')[0];
    expect((idInput.element as HTMLInputElement).disabled).toBe(true);
  });

  it('valida que el ID es requerido', async () => {
    const wrapper = mount(EmpleadoForm);

    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.text()).toContain('El ID es requerido');
  });

  it('valida que el nombre es requerido', async () => {
    const wrapper = mount(EmpleadoForm);

    const inputs = wrapper.findAll('input');
    await inputs[0].setValue('E001');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.text()).toContain('El nombre es requerido');
  });

  it('emite evento guardar con datos válidos', async () => {
    const wrapper = mount(EmpleadoForm);

    const inputs = wrapper.findAll('input');
    await inputs[0].setValue('E001');
    await inputs[1].setValue('Juan Pérez');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.emitted('guardar')).toBeTruthy();
    expect(wrapper.emitted('guardar')?.[0]).toEqual([
      {
        id: 'E001',
        nombre: 'Juan Pérez',
      },
    ]);
  });

  it('emite evento cancelar cuando se hace clic en cancelar', async () => {
    const wrapper = mount(EmpleadoForm);

    const buttons = wrapper.findAll('button');
    await buttons[0].trigger('click');

    expect(wrapper.emitted('cancelar')).toBeTruthy();
  });

  it('muestra errores de validación en campos específicos', async () => {
    const wrapper = mount(EmpleadoForm);

    await wrapper.find('form').trigger('submit.prevent');

    const inputs = wrapper.findAll('input');
    expect(inputs[0].classes()).toContain('border-red-500');
    expect(inputs[1].classes()).toContain('border-red-500');
  });
});
