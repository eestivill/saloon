# Requirements Document

## Introduction

Sistema de gestión para salón de peluquería que permite registrar servicios realizados, calcular ingresos totales y gestionar el pago a empleados basado en comisiones por servicio.

## Glossary

- **Sistema**: La aplicación de gestión del salón de peluquería
- **Servicio**: Un tratamiento o procedimiento de peluquería realizado a un cliente (corte, tinte, peinado, etc.)
- **Tipo_de_Servicio**: Categoría de servicio con nombre y porcentaje de comisión asociado (ej: Corte Básico 40%, Tinte Completo 35%)
- **Empleado**: Persona que trabaja en el salón y realiza servicios a clientes
- **Ingreso**: Monto monetario recibido por un servicio realizado
- **Comisión**: Porcentaje del precio del servicio que corresponde al empleado que lo realizó, definido por el Tipo_de_Servicio
- **Registro_de_Servicio**: Información completa de un servicio incluyendo fecha, empleado, tipo de servicio y precio

## Requirements

### Requirement 1: Gestionar Empleados

**User Story:** Como administrador del salón, quiero gestionar la información de los empleados, para poder asignarles servicios y calcular sus pagos.

#### Acceptance Criteria

1. THE Sistema SHALL permitir crear un Empleado con nombre e identificador único
2. THE Sistema SHALL validar que el identificador del Empleado sea único
3. WHEN se intenta crear un Empleado con identificador duplicado, THE Sistema SHALL retornar un mensaje de error
4. THE Sistema SHALL permitir consultar la lista de todos los empleados registrados
5. THE Sistema SHALL permitir actualizar la información de un Empleado existente

### Requirement 2: Gestionar Tipos de Servicios

**User Story:** Como administrador del salón, quiero gestionar los tipos de servicios disponibles con sus porcentajes de comisión, para definir cuánto gana cada empleado por cada tipo de servicio realizado.

#### Acceptance Criteria

1. THE Sistema SHALL permitir crear un Tipo_de_Servicio con nombre, descripción y porcentaje de comisión
2. THE Sistema SHALL validar que el porcentaje de comisión esté entre 0 y 100
3. THE Sistema SHALL validar que el nombre del Tipo_de_Servicio sea único
4. WHEN se intenta crear un Tipo_de_Servicio con nombre duplicado, THE Sistema SHALL retornar un mensaje de error
5. THE Sistema SHALL permitir consultar la lista de todos los tipos de servicios registrados
6. THE Sistema SHALL permitir actualizar el porcentaje de comisión de un Tipo_de_Servicio existente
7. WHEN se registra un servicio, THE Sistema SHALL utilizar el porcentaje de comisión del Tipo_de_Servicio asociado

### Requirement 3: Registrar Servicios Realizados

**User Story:** Como administrador del salón, quiero registrar cada servicio realizado, para mantener un historial completo de las operaciones del negocio.

#### Acceptance Criteria

1. WHEN un servicio es completado, THE Sistema SHALL crear un Registro_de_Servicio con fecha, empleado asignado, tipo de servicio y precio
2. THE Sistema SHALL validar que el precio del servicio sea mayor que cero
3. THE Sistema SHALL validar que el empleado asignado exista en el sistema
4. THE Sistema SHALL validar que el Tipo_de_Servicio asignado exista en el sistema
5. WHEN se intenta registrar un servicio con datos incompletos, THE Sistema SHALL retornar un mensaje de error descriptivo
6. THE Sistema SHALL almacenar todos los Registros_de_Servicio de forma persistente

### Requirement 4: Consultar Ingresos y beneficios del Salón

**User Story:** Como administrador del salón, quiero conocer los ingresos totales y el beneficio, para evaluar el desempeño financiero del negocio.

#### Acceptance Criteria

1. THE Sistema SHALL calcular los ingresos totales sumando el precio de todos los servicios registrados
2. WHEN se solicitan ingresos por período, THE Sistema SHALL calcular la suma de servicios dentro del rango de fechas especificado AND THE Sistema SHALL calcular los beneficios como la suma de servicios restando la suma de pagos a empleados dentro del rango de fechas especificado
3. THE Sistema SHALL mostrar los ingresos con formato monetario apropiado
  AND THE Sistema SHALL mostrar los beneficios con formato monetario apropiado
4. WHEN no existen servicios registrados, THE Sistema SHALL retornar un ingreso de cero
5. THE Sistema SHALL calcular los ingresos en tiempo real basándose en los Registros_de_Servicio actuales

### Requirement 5: Calcular Pagos a Empleados

**User Story:** Como administrador del salón, quiero calcular automáticamente lo que debo pagar a cada empleado, para facilitar el proceso de nómina.

#### Acceptance Criteria

1. THE Sistema SHALL calcular el pago de un Empleado multiplicando el precio de cada servicio realizado por el porcentaje de comisión del Tipo_de_Servicio asociado
2. WHEN se solicita el pago de un Empleado, THE Sistema SHALL sumar todas las comisiones de sus servicios registrados
3. WHEN se solicita el pago por período, THE Sistema SHALL calcular la suma de comisiones dentro del rango de fechas especificado
4. THE Sistema SHALL mostrar el desglose de servicios realizados por el Empleado junto con el total a pagar
5. WHEN un Empleado no tiene servicios registrados, THE Sistema SHALL retornar un pago de cero

### Requirement 6: Consultar Servicios por Empleado

**User Story:** Como administrador del salón, quiero ver todos los servicios realizados por un empleado específico, para evaluar su desempeño individual.

#### Acceptance Criteria

1. WHEN se solicitan servicios de un Empleado, THE Sistema SHALL retornar todos los Registros_de_Servicio asociados a ese empleado
2. THE Sistema SHALL ordenar los servicios por fecha de forma descendente (más recientes primero)
3. WHEN se solicitan servicios por período, THE Sistema SHALL filtrar los Registros_de_Servicio dentro del rango de fechas especificado
4. THE Sistema SHALL mostrar para cada servicio la fecha, tipo de servicio, precio y comisión calculada
5. WHEN un Empleado no tiene servicios registrados, THE Sistema SHALL retornar una lista vacía

### Requirement 7: Filtrar Servicios por Fecha

**User Story:** Como administrador del salón, quiero filtrar servicios por rangos de fechas, para analizar períodos específicos de operación.

#### Acceptance Criteria

1. WHEN se especifica una fecha de inicio, THE Sistema SHALL retornar servicios desde esa fecha en adelante
2. WHEN se especifica una fecha de fin, THE Sistema SHALL retornar servicios hasta esa fecha
3. WHEN se especifican ambas fechas, THE Sistema SHALL retornar servicios dentro del rango inclusivo
4. THE Sistema SHALL validar que la fecha de inicio no sea posterior a la fecha de fin
5. WHEN las fechas son inválidas, THE Sistema SHALL retornar un mensaje de error descriptivo

### Requirement 8: Persistencia de Datos

**User Story:** Como administrador del salón, quiero que todos los datos se guarden de forma permanente, para no perder información al cerrar la aplicación.

#### Acceptance Criteria

1. THE Sistema SHALL almacenar todos los Registros_de_Servicio de forma persistente
2. THE Sistema SHALL almacenar todos los datos de Empleados de forma persistente
3. THE Sistema SHALL almacenar todos los Tipos_de_Servicio de forma persistente
4. WHEN el Sistema se reinicia, THE Sistema SHALL cargar todos los datos previamente guardados
5. THE Sistema SHALL mantener la integridad de los datos ante cierres inesperados
6. THE Sistema SHALL validar la integridad de los datos al cargarlos

