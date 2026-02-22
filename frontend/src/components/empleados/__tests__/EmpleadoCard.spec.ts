import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import EmpleadoCard from '../EmpleadoCard.vue';
import type { Empleado } from '@/types/models';

describe('EmpleadoCard', () => {
  const mockEmpleado: Empleado = {
    id: 'E001',
    nombre: 'Juan Pérez',
  };

  it('muestra la información del empleado correctamente', () => {
    const wrapper = mount(EmpleadoCard, {
      props: {
        empleado: mockEmpleado,
      },
    });

    expect(wrapper.text()).toContain('Juan Pérez');
    expect(wrapper.text()).toContain('ID: E001');
  });

  it('emite evento editar cuando se hace clic en el botón editar', async () => {
    const wrapper = mount(EmpleadoCard, {
      props: {
        empleado: mockEmpleado,
      },
    });

    await wrapper.find('button:first-of-type').trigger('click');

    expect(wrapper.emitted('editar')).toBeTruthy();
    expect(wrapper.emitted('editar')?.[0]).toEqual([mockEmpleado]);
  });

  it('emite evento eliminar cuando se hace clic en el botón eliminar', async () => {
    const wrapper = mount(EmpleadoCard, {
      props: {
        empleado: mockEmpleado,
      },
    });

    const buttons = wrapper.findAll('button');
    await buttons[1].trigger('click');

    expect(wrapper.emitted('eliminar')).toBeTruthy();
    expect(wrapper.emitted('eliminar')?.[0]).toEqual(['E001']);
  });

  it('aplica estilos responsive correctamente', () => {
    const wrapper = mount(EmpleadoCard, {
      props: {
        empleado: mockEmpleado,
      },
    });

    const container = wrapper.find('.bg-white');
    expect(container.exists()).toBe(true);
    expect(container.classes()).toContain('rounded-lg');
    expect(container.classes()).toContain('shadow-md');
  });
});
