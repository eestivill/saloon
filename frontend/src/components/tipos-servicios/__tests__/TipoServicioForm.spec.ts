import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import TipoServicioForm from '../TipoServicioForm.vue';
import type { TipoServicio } from '@/types/models';

describe('TipoServicioForm', () => {
  it('muestra título "Nuevo Tipo de Servicio" cuando no hay tipo', () => {
    const wrapper = mount(TipoServicioForm);
    expect(wrapper.text()).toContain('Nuevo Tipo de Servicio');
  });

  it('muestra título "Editar Tipo de Servicio" cuando hay tipo', () => {
    const mockTipo: TipoServicio = {
      nombre: 'Corte Básico',
      descripcion: 'Corte de cabello básico',
      porcentaje_comision: 40,
    };

    const wrapper = mount(TipoServicioForm, {
      props: {
        tipo: mockTipo,
      },
    });

    expect(wrapper.text()).toContain('Editar Tipo de Servicio');
  });

  it('carga datos del tipo de servicio en modo edición', async () => {
    const mockTipo: TipoServicio = {
      nombre: 'Corte Básico',
      descripcion: 'Corte de cabello básico',
      porcentaje_comision: 40,
    };

    const wrapper = mount(TipoServicioForm, {
      props: {
        tipo: mockTipo,
      },
    });

    await wrapper.vm.$nextTick();

    const inputs = wrapper.findAll('input');
    const textarea = wrapper.find('textarea');
    
    expect((inputs[0].element as HTMLInputElement).value).toBe('Corte Básico');
    expect((textarea.element as HTMLTextAreaElement).value).toBe('Corte de cabello básico');
    expect((inputs[1].element as HTMLInputElement).value).toBe('40');
  });

  it('deshabilita el campo nombre en modo edición', () => {
    const mockTipo: TipoServicio = {
      nombre: 'Corte Básico',
      descripcion: 'Corte de cabello básico',
      porcentaje_comision: 40,
    };

    const wrapper = mount(TipoServicioForm, {
      props: {
        tipo: mockTipo,
      },
    });

    const nombreInput = wrapper.findAll('input')[0];
    expect((nombreInput.element as HTMLInputElement).disabled).toBe(true);
  });

  it('valida que el nombre es requerido', async () => {
    const wrapper = mount(TipoServicioForm);

    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.text()).toContain('El nombre es requerido');
  });

  it('valida que la descripción es requerida', async () => {
    const wrapper = mount(TipoServicioForm);

    const inputs = wrapper.findAll('input');
    await inputs[0].setValue('Corte Básico');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.text()).toContain('La descripción es requerida');
  });

  it('valida que el porcentaje está en rango [0-100]', async () => {
    const wrapper = mount(TipoServicioForm);

    const inputs = wrapper.findAll('input');
    const textarea = wrapper.find('textarea');
    
    await inputs[0].setValue('Corte Básico');
    await textarea.setValue('Descripción');
    await inputs[1].setValue('150');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.text()).toContain('El porcentaje debe estar entre 0 y 100');
  });

  it('valida que el porcentaje negativo es inválido', async () => {
    const wrapper = mount(TipoServicioForm);

    const inputs = wrapper.findAll('input');
    const textarea = wrapper.find('textarea');
    
    await inputs[0].setValue('Corte Básico');
    await textarea.setValue('Descripción');
    await inputs[1].setValue('-10');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.text()).toContain('El porcentaje debe estar entre 0 y 100');
  });

  it('emite evento guardar con datos válidos', async () => {
    const wrapper = mount(TipoServicioForm);

    const inputs = wrapper.findAll('input');
    const textarea = wrapper.find('textarea');
    
    await inputs[0].setValue('Corte Básico');
    await textarea.setValue('Corte de cabello básico');
    await inputs[1].setValue('40');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.emitted('guardar')).toBeTruthy();
    expect(wrapper.emitted('guardar')?.[0]).toEqual([
      {
        nombre: 'Corte Básico',
        descripcion: 'Corte de cabello básico',
        porcentaje_comision: 40,
      },
    ]);
  });

  it('emite evento cancelar cuando se hace clic en cancelar', async () => {
    const wrapper = mount(TipoServicioForm);

    const buttons = wrapper.findAll('button');
    await buttons[0].trigger('click');

    expect(wrapper.emitted('cancelar')).toBeTruthy();
  });

  it('muestra errores de validación en campos específicos', async () => {
    const wrapper = mount(TipoServicioForm);

    await wrapper.find('form').trigger('submit.prevent');

    const inputs = wrapper.findAll('input');
    const textarea = wrapper.find('textarea');
    
    expect(inputs[0].classes()).toContain('border-red-500');
    expect(textarea.classes()).toContain('border-red-500');
  });

  it('muestra texto de ayuda para el porcentaje', () => {
    const wrapper = mount(TipoServicioForm);

    expect(wrapper.text()).toContain('Debe estar entre 0 y 100');
  });

  it('acepta porcentajes decimales válidos', async () => {
    const wrapper = mount(TipoServicioForm);

    const inputs = wrapper.findAll('input');
    const textarea = wrapper.find('textarea');
    
    await inputs[0].setValue('Corte Premium');
    await textarea.setValue('Corte de cabello premium');
    await inputs[1].setValue('42.5');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.emitted('guardar')).toBeTruthy();
    expect(wrapper.emitted('guardar')?.[0]).toEqual([
      {
        nombre: 'Corte Premium',
        descripcion: 'Corte de cabello premium',
        porcentaje_comision: 42.5,
      },
    ]);
  });
});
