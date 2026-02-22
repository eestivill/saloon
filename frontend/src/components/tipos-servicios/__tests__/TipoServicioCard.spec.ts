import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import TipoServicioCard from '../TipoServicioCard.vue';
import type { TipoServicio } from '@/types/models';

describe('TipoServicioCard', () => {
  const mockTipoServicio: TipoServicio = {
    nombre: 'Corte Básico',
    descripcion: 'Corte de cabello básico',
    porcentaje_comision: 40,
  };

  it('muestra la información del tipo de servicio correctamente', () => {
    const wrapper = mount(TipoServicioCard, {
      props: {
        tipo: mockTipoServicio,
      },
    });

    expect(wrapper.text()).toContain('Corte Básico');
    expect(wrapper.text()).toContain('Corte de cabello básico');
    expect(wrapper.text()).toContain('Comisión: 40%');
  });

  it('emite evento editar cuando se hace clic en el botón editar', async () => {
    const wrapper = mount(TipoServicioCard, {
      props: {
        tipo: mockTipoServicio,
      },
    });

    await wrapper.find('button:first-of-type').trigger('click');

    expect(wrapper.emitted('editar')).toBeTruthy();
    expect(wrapper.emitted('editar')?.[0]).toEqual([mockTipoServicio]);
  });

  it('emite evento eliminar cuando se hace clic en el botón eliminar', async () => {
    const wrapper = mount(TipoServicioCard, {
      props: {
        tipo: mockTipoServicio,
      },
    });

    const buttons = wrapper.findAll('button');
    await buttons[1].trigger('click');

    expect(wrapper.emitted('eliminar')).toBeTruthy();
    expect(wrapper.emitted('eliminar')?.[0]).toEqual(['Corte Básico']);
  });

  it('aplica estilos responsive correctamente', () => {
    const wrapper = mount(TipoServicioCard, {
      props: {
        tipo: mockTipoServicio,
      },
    });

    const container = wrapper.find('.bg-white');
    expect(container.exists()).toBe(true);
    expect(container.classes()).toContain('rounded-lg');
    expect(container.classes()).toContain('shadow-md');
  });

  it('muestra el porcentaje de comisión con badge verde', () => {
    const wrapper = mount(TipoServicioCard, {
      props: {
        tipo: mockTipoServicio,
      },
    });

    const badge = wrapper.find('.bg-green-100');
    expect(badge.exists()).toBe(true);
    expect(badge.classes()).toContain('text-green-800');
    expect(badge.text()).toContain('40%');
  });
});
