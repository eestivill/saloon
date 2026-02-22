# Plan de Implementación: Sistema de Gestión de Salón de Peluquería

## Resumen

Este plan implementa un sistema de gestión para salón de peluquería con arquitectura web mobile-first. El backend utiliza FastAPI (Python) con SQLAlchemy y SQLite para exponer una API REST. El frontend utiliza Vue 3 con TypeScript y Tailwind CSS para proporcionar una interfaz responsive optimizada para dispositivos móviles. El sistema permite gestionar empleados, tipos de servicios, registrar servicios realizados y calcular comisiones e ingresos.

## Tareas

### BACKEND: Configuración y Modelos de Datos

- [x] 1. Configurar estructura del proyecto backend
  - Crear estructura de directorios (app/, tests/, alembic/)
  - Configurar entorno virtual Python
  - Crear requirements.txt con dependencias: fastapi, uvicorn, sqlalchemy, pydantic, python-dotenv, hypothesis (testing)
  - Crear archivo .env para configuración
  - Configurar .gitignore para Python
  - _Requisitos: 8.1, 8.2, 8.3_

- [x] 2. Implementar modelos de dominio y tipos auxiliares
  - Crear modelos de datos: Empleado, TipoServicio, ServicioRegistrado
  - Implementar tipos auxiliares: Result, Ok, Err
  - Implementar tipos de error: ValidationError, NotFoundError, DuplicateError, PersistenceError
  - Implementar DesglosePago y ServicioDetalle
  - Agregar métodos to_dict() y from_orm() para conversión
  - _Requisitos: 1.1, 2.1, 3.1, 8.1, 8.2, 8.3_


- [x] 3. Implementar modelos SQLAlchemy ORM
  - Crear Base declarativa de SQLAlchemy
  - Implementar EmpleadoORM con tabla 'empleados'
  - Implementar TipoServicioORM con tabla 'tipos_servicios' y constraint de porcentaje
  - Implementar ServicioORM con tabla 'servicios', foreign keys e índices
  - Agregar índices: idx_servicios_empleado_fecha, idx_servicios_fecha
  - _Requisitos: 8.1, 8.2, 8.3, 8.4_

- [x] 3.1 Escribir pruebas de propiedad para serialización de modelos
  - **Property 26: Persistencia Round-Trip para Todas las Entidades**
  - **Valida: Requisitos 3.6, 8.1, 8.2, 8.3, 8.4**

- [x] 4. Implementar módulo de validación
  - Crear clase Validator con métodos estáticos
  - Implementar validar_porcentaje_comision() que retorna Result
  - Implementar validar_precio() que retorna Result
  - Implementar validar_rango_fechas() que retorna Result
  - Implementar validar_identificador_unico() que retorna Result
  - _Requisitos: 2.2, 3.2, 7.4_

- [x] 4.1 Escribir pruebas unitarias para validaciones
  - Probar casos de borde para porcentajes (0, 100, -1, 101)
  - Probar precios válidos e inválidos (0, 0.01, -10)
  - Probar rangos de fechas válidos e inválidos
  - _Requisitos: 2.2, 3.2, 7.4_

- [x] 4.2 Escribir pruebas de propiedad para validaciones
  - **Property 6: Validación de Rango de Porcentaje de Comisión**
  - **Valida: Requisitos 2.2**
  - **Property 11: Validación de Precio Positivo**
  - **Valida: Requisitos 3.2**
  - **Property 25: Validación de Rango de Fechas**
  - **Valida: Requisitos 7.4**

- [x] 5. Implementar capa de acceso a datos (SQLAlchemyRepository)
  - Crear interfaz abstracta DataRepository con todos los métodos
  - Implementar SQLAlchemyRepository con inicialización de engine y sesiones
  - Implementar métodos para guardar y obtener empleados
  - Implementar métodos para guardar y obtener tipos de servicios
  - Implementar métodos para guardar y listar servicios
  - Implementar get_session() para gestión de sesiones
  - Manejar errores de SQLAlchemy y convertirlos en PersistenceError
  - _Requisitos: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [x] 5.1 Escribir pruebas unitarias para SQLAlchemyRepository
  - Probar creación de tablas si no existen
  - Probar carga de datos existentes
  - Probar manejo de errores de base de datos
  - Probar persistencia después de guardar
  - Probar que índices están creados correctamente
  - _Requisitos: 8.4, 8.5, 8.6_


- [x] 5.2 Escribir pruebas de propiedad para persistencia
  - **Property 27: Validación de Integridad al Cargar Datos**
  - **Valida: Requisitos 8.6**

- [x] 6. Checkpoint - Verificar capa de datos
  - Asegurar que todos los tests pasen, preguntar al usuario si surgen dudas.

### BACKEND: Lógica de Negocio

- [x] 7. Implementar gestión de empleados en SalonManager
  - Crear clase SalonManager con constructor que recibe DataRepository
  - Implementar crear_empleado() con validación de ID único
  - Implementar obtener_empleado() que retorna Optional[Empleado]
  - Implementar listar_empleados() que retorna List[Empleado]
  - Implementar actualizar_empleado() que preserva ID
  - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 7.1 Escribir pruebas unitarias para gestión de empleados
  - Probar creación exitosa de empleado
  - Probar error al crear empleado con ID duplicado
  - Probar actualización de empleado existente
  - Probar lista vacía cuando no hay empleados
  - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 7.2 Escribir pruebas de propiedad para empleados
  - **Property 1: Creación de Empleados con Atributos Válidos**
  - **Valida: Requisitos 1.1**
  - **Property 2: Unicidad de Identificadores de Empleados**
  - **Valida: Requisitos 1.2**
  - **Property 3: Consulta Completa de Empleados**
  - **Valida: Requisitos 1.4**
  - **Property 4: Actualización de Empleados Preserva Identidad**
  - **Valida: Requisitos 1.5**

- [x] 8. Implementar gestión de tipos de servicios en SalonManager
  - Implementar crear_tipo_servicio() con validación de nombre único y porcentaje
  - Implementar obtener_tipo_servicio() que retorna Optional[TipoServicio]
  - Implementar listar_tipos_servicios() que retorna List[TipoServicio]
  - Implementar actualizar_tipo_servicio() con validación de porcentaje
  - _Requisitos: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 8.1 Escribir pruebas unitarias para tipos de servicios
  - Probar creación exitosa con porcentaje válido
  - Probar error con porcentaje fuera de rango
  - Probar error con nombre duplicado
  - Probar actualización de porcentaje
  - _Requisitos: 2.1, 2.2, 2.3, 2.6_

- [x] 8.2 Escribir pruebas de propiedad para tipos de servicios
  - **Property 5: Creación de Tipos de Servicio con Atributos Válidos**
  - **Valida: Requisitos 2.1**
  - **Property 7: Unicidad de Nombres de Tipos de Servicio**
  - **Valida: Requisitos 2.3**
  - **Property 8: Consulta Completa de Tipos de Servicios**
  - **Valida: Requisitos 2.5**
  - **Property 9: Actualización de Porcentaje de Comisión**
  - **Valida: Requisitos 2.6**


- [x] 9. Implementar registro de servicios en SalonManager
  - Implementar registrar_servicio() con generación automática de ID único
  - Validar que empleado_id exista (retornar NotFoundError si no)
  - Validar que tipo_servicio exista (retornar NotFoundError si no)
  - Validar precio usando Validator
  - Calcular comisión usando porcentaje del tipo de servicio
  - Crear ServicioRegistrado con comision_calculada
  - Persistir servicio usando DataRepository
  - _Requisitos: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 2.7_

- [x] 9.1 Escribir pruebas unitarias para registro de servicios
  - Probar registro exitoso con datos válidos
  - Probar error con precio inválido
  - Probar error con empleado inexistente
  - Probar error con tipo de servicio inexistente
  - Probar que comisión se calcula correctamente
  - _Requisitos: 3.1, 3.2, 3.3, 3.4, 2.7_

- [x] 9.2 Escribir pruebas de propiedad para registro de servicios
  - **Property 10: Registro de Servicio con Todos los Atributos**
  - **Valida: Requisitos 3.1**
  - **Property 12: Validación de Integridad Referencial**
  - **Valida: Requisitos 3.3, 3.4**
  - **Property 18: Cálculo de Comisión Individual**
  - **Valida: Requisitos 2.7, 5.1**

- [x] 10. Implementar consultas de servicios en SalonManager
  - Implementar obtener_servicios() con parámetros opcionales
  - Filtrar por empleado_id si se proporciona
  - Filtrar por fecha_inicio si se proporciona
  - Filtrar por fecha_fin si se proporciona
  - Ordenar resultados por fecha descendente
  - Retornar lista vacía si no hay coincidencias
  - _Requisitos: 6.1, 6.2, 6.3, 6.5, 7.1, 7.2, 7.3_

- [x] 10.1 Escribir pruebas unitarias para consultas de servicios
  - Probar filtrado por empleado
  - Probar filtrado por rango de fechas
  - Probar ordenamiento descendente
  - Probar lista vacía cuando no hay servicios
  - _Requisitos: 6.1, 6.2, 6.3, 6.5_

- [x] 10.2 Escribir pruebas de propiedad para consultas
  - **Property 14: Filtrado de Ingresos por Rango de Fechas**
  - **Valida: Requisitos 4.2, 7.1, 7.2, 7.3**
  - **Property 22: Filtrado de Servicios por Empleado**
  - **Valida: Requisitos 6.1**
  - **Property 23: Ordenamiento Descendente por Fecha**
  - **Valida: Requisitos 6.2**
  - **Property 24: Servicios Contienen Información Completa**
  - **Valida: Requisitos 6.4**

- [x] 11. Implementar cálculos financieros en SalonManager
  - Implementar calcular_ingresos_totales() con filtrado opcional por fechas
  - Sumar precios de todos los servicios filtrados
  - Retornar Decimal("0") si no hay servicios
  - Implementar calcular_beneficios() como ingresos menos suma de comisiones
  - Aplicar filtrado por fechas si se proporciona
  - _Requisitos: 4.1, 4.2, 4.4, 4.5_


- [x] 11.1 Escribir pruebas unitarias para cálculos financieros
  - Probar ingresos con múltiples servicios
  - Probar ingresos con lista vacía retorna cero
  - Probar filtrado por período
  - Probar cálculo de beneficios
  - _Requisitos: 4.1, 4.2, 4.4, 4.5_

- [x] 11.2 Escribir pruebas de propiedad para cálculos financieros
  - **Property 13: Cálculo Correcto de Ingresos Totales**
  - **Valida: Requisitos 4.1**
  - **Property 15: Cálculo de Beneficios como Ingresos Menos Comisiones**
  - **Valida: Requisitos 4.2**
  - **Property 17: Ingresos se Actualizan Inmediatamente**
  - **Valida: Requisitos 4.5**

- [x] 12. Implementar cálculo de pagos a empleados en SalonManager
  - Implementar calcular_pago_empleado() con filtrado opcional por fechas
  - Obtener todos los servicios del empleado usando obtener_servicios()
  - Sumar comisiones de todos los servicios
  - Crear DesglosePago con lista de ServicioDetalle
  - Retornar pago de cero si empleado no tiene servicios
  - _Requisitos: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 12.1 Escribir pruebas unitarias para pagos a empleados
  - Probar cálculo con múltiples servicios
  - Probar empleado sin servicios retorna cero
  - Probar filtrado por período
  - Probar desglose contiene todos los servicios
  - _Requisitos: 5.2, 5.3, 5.4, 5.5_

- [x] 12.2 Escribir pruebas de propiedad para pagos
  - **Property 19: Suma de Comisiones por Empleado**
  - **Valida: Requisitos 5.2**
  - **Property 20: Filtrado de Pagos por Período**
  - **Valida: Requisitos 5.3**
  - **Property 21: Desglose de Pago Contiene Todos los Servicios**
  - **Valida: Requisitos 5.4**

- [x] 13. Checkpoint - Verificar lógica de negocio completa
  - Asegurar que todos los tests pasen, preguntar al usuario si surgen dudas.

### BACKEND: API REST con FastAPI

- [x] 14. Configurar aplicación FastAPI
  - Crear app FastAPI con título, descripción y versión
  - Configurar middleware CORS para permitir acceso desde frontend
  - Configurar manejo de errores global con exception handlers
  - Configurar logging con niveles apropiados
  - Crear instancia de SQLAlchemyRepository y SalonManager
  - _Requisitos: Todos (infraestructura)_

- [x] 15. Implementar modelos Pydantic para request/response
  - Crear EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse
  - Crear TipoServicioCreate, TipoServicioUpdate, TipoServicioResponse
  - Crear ServicioCreate, ServicioResponse
  - Crear IngresosResponse, BeneficiosResponse
  - Crear ServicioDetalle, DesglosePagoResponse
  - Agregar validadores personalizados con @validator
  - Configurar orm_mode = True en Config
  - _Requisitos: 1.1, 2.1, 3.1, 4.1, 5.1_


- [x] 16. Implementar endpoints de empleados
  - Implementar GET /api/empleados - Listar todos los empleados
  - Implementar GET /api/empleados/{id} - Obtener empleado por ID
  - Implementar POST /api/empleados - Crear nuevo empleado
  - Implementar PUT /api/empleados/{id} - Actualizar empleado
  - Implementar DELETE /api/empleados/{id} - Eliminar empleado
  - Manejar errores Result y convertir a HTTPException apropiadas
  - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 16.1 Escribir pruebas de API para endpoints de empleados
  - Probar POST exitoso retorna 201
  - Probar POST con ID duplicado retorna 409
  - Probar GET con ID inexistente retorna 404
  - Probar PUT actualiza correctamente
  - Probar DELETE elimina correctamente
  - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 17. Implementar endpoints de tipos de servicios
  - Implementar GET /api/tipos-servicios - Listar todos los tipos
  - Implementar GET /api/tipos-servicios/{nombre} - Obtener tipo por nombre
  - Implementar POST /api/tipos-servicios - Crear nuevo tipo
  - Implementar PUT /api/tipos-servicios/{nombre} - Actualizar tipo
  - Implementar DELETE /api/tipos-servicios/{nombre} - Eliminar tipo
  - Validar porcentaje de comisión en rango [0, 100]
  - _Requisitos: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 17.1 Escribir pruebas de API para endpoints de tipos de servicios
  - Probar POST exitoso con porcentaje válido
  - Probar POST con porcentaje inválido retorna 400
  - Probar POST con nombre duplicado retorna 409
  - Probar PUT actualiza porcentaje correctamente
  - _Requisitos: 2.1, 2.2, 2.3, 2.6_

- [x] 18. Implementar endpoints de servicios
  - Implementar GET /api/servicios - Listar servicios con filtros opcionales (empleado_id, fecha_inicio, fecha_fin)
  - Implementar GET /api/servicios/{id} - Obtener servicio por ID
  - Implementar POST /api/servicios - Registrar nuevo servicio
  - Implementar DELETE /api/servicios/{id} - Eliminar servicio
  - Validar integridad referencial (empleado y tipo de servicio existen)
  - Calcular comisión automáticamente al registrar
  - _Requisitos: 3.1, 3.2, 3.3, 3.4, 3.5, 6.1, 6.2, 6.3, 7.1, 7.2, 7.3_

- [x] 18.1 Escribir pruebas de API para endpoints de servicios
  - Probar POST exitoso calcula comisión correctamente
  - Probar POST con empleado inexistente retorna 404
  - Probar POST con tipo de servicio inexistente retorna 404
  - Probar POST con precio inválido retorna 400
  - Probar GET con filtros retorna servicios correctos
  - Probar ordenamiento descendente por fecha
  - _Requisitos: 3.1, 3.2, 3.3, 3.4, 6.1, 6.2_

- [x] 19. Implementar endpoints de reportes
  - Implementar GET /api/reportes/ingresos - Calcular ingresos totales con filtros opcionales
  - Implementar GET /api/reportes/beneficios - Calcular beneficios con filtros opcionales
  - Implementar GET /api/empleados/{id}/pago - Calcular pago de empleado con filtros opcionales
  - Aplicar formato monetario apropiado en respuestas
  - _Requisitos: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4_


- [x] 19.1 Escribir pruebas de API para endpoints de reportes
  - Probar cálculo de ingresos con múltiples servicios
  - Probar filtrado por rango de fechas
  - Probar cálculo de beneficios correcto
  - Probar desglose de pago contiene todos los servicios
  - _Requisitos: 4.1, 4.2, 5.2, 5.3, 5.4_

- [x] 19.2 Escribir pruebas de propiedad para formato monetario
  - **Property 16: Formato Monetario Contiene Símbolos Apropiados**
  - **Valida: Requisitos 4.3**

- [x] 20. Checkpoint - Verificar API REST completa
  - Asegurar que todos los tests de API pasen
  - Verificar documentación automática en /docs
  - Probar todos los endpoints manualmente con Swagger UI
  - Asegurar que todos los tests pasen, preguntar al usuario si surgen dudas.

### FRONTEND: Configuración y Estructura

- [x] 21. Configurar proyecto frontend Vue 3
  - Crear proyecto con Vite + Vue 3 + TypeScript
  - Instalar dependencias: vue-router, pinia, axios, tailwindcss
  - Configurar Tailwind CSS con diseño mobile-first
  - Configurar ESLint y Prettier
  - Crear estructura de directorios (components/, views/, stores/, services/, types/)
  - Configurar .gitignore para Node.js
  - _Requisitos: Todos (infraestructura frontend)_

- [x] 22. Implementar tipos TypeScript
  - Crear interfaces: Empleado, TipoServicio, Servicio
  - Crear interfaces: ServicioDetalle, DesglosePago
  - Crear interfaces: IngresosResponse, BeneficiosResponse
  - Crear tipos para formularios: EmpleadoFormData, TipoServicioFormData, ServicioFormData
  - Crear tipo para filtros: ServiciosFiltros
  - _Requisitos: 1.1, 2.1, 3.1, 4.1, 5.1_

- [x] 23. Implementar servicio API con Axios
  - Crear instancia de Axios con baseURL configurada
  - Implementar interceptor de respuesta para manejo de errores
  - Crear empleadosAPI con métodos: listar, obtener, crear, actualizar, eliminar, obtenerPago
  - Crear tiposServiciosAPI con métodos: listar, obtener, crear, actualizar, eliminar
  - Crear serviciosAPI con métodos: listar, obtener, crear, eliminar
  - Crear reportesAPI con métodos: ingresos, beneficios
  - _Requisitos: Todos (comunicación con backend)_

- [x] 24. Configurar Vue Router
  - Crear rutas: /, /empleados, /servicios, /tipos-servicios, /reportes
  - Implementar navegación entre vistas
  - Configurar modo history
  - _Requisitos: Todos (navegación)_

### FRONTEND: Stores con Pinia

- [x] 25. Implementar store de empleados
  - Crear useEmpleadosStore con estado: empleados, loading, error
  - Implementar computed: empleadosOrdenados
  - Implementar acciones: cargarEmpleados, crearEmpleado, actualizarEmpleado, eliminarEmpleado
  - Manejar errores y actualizar estado error apropiadamente
  - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5_


- [x] 26. Implementar store de tipos de servicios
  - Crear useTiposServiciosStore con estado: tiposServicios, loading, error
  - Implementar acciones: cargarTiposServicios, crearTipoServicio, actualizarTipoServicio, eliminarTipoServicio
  - Manejar errores apropiadamente
  - _Requisitos: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 27. Implementar store de servicios
  - Crear useServiciosStore con estado: servicios, loading, error
  - Implementar acciones: cargarServicios, registrarServicio, eliminarServicio
  - Implementar acción: filtrarServicios con parámetros opcionales
  - Manejar errores apropiadamente
  - _Requisitos: 3.1, 3.2, 3.3, 3.4, 6.1, 6.2, 6.3, 7.1, 7.2, 7.3_

- [x] 28. Implementar store de reportes
  - Crear useReportesStore con estado: ingresos, beneficios, pagoEmpleado, loading, error
  - Implementar acciones: calcularIngresos, calcularBeneficios, calcularPagoEmpleado
  - Soportar filtrado por rango de fechas
  - _Requisitos: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4_

### FRONTEND: Componentes Comunes

- [x] 29. Implementar componentes comunes
  - Crear AppHeader.vue con título y navegación mobile-first
  - Crear AppNavigation.vue con menú responsive (hamburger en móvil)
  - Crear LoadingSpinner.vue con animación
  - Crear ErrorMessage.vue con estilos Tailwind (rojo, icono)
  - Crear SuccessMessage.vue con estilos Tailwind (verde, icono)
  - _Requisitos: Todos (UI común)_

### FRONTEND: Componentes de Empleados

- [x] 30. Implementar componentes de empleados
  - Crear EmpleadosList.vue con grid responsive (1 col móvil, 2-3 cols desktop)
  - Crear EmpleadoCard.vue con diseño mobile-first
  - Crear EmpleadoForm.vue con validación de formulario
  - Implementar botones de acción: editar, eliminar
  - Mostrar LoadingSpinner mientras carga
  - Mostrar ErrorMessage si hay error
  - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 30.1 Escribir pruebas unitarias para componentes de empleados
  - Probar que EmpleadosList muestra lista correctamente
  - Probar que muestra spinner mientras carga
  - Probar que muestra error cuando falla
  - Probar validación de formulario
  - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5_

### FRONTEND: Componentes de Tipos de Servicios

- [x] 31. Implementar componentes de tipos de servicios
  - Crear TiposServiciosList.vue con grid responsive
  - Crear TipoServicioCard.vue mostrando nombre, descripción y porcentaje
  - Crear TipoServicioForm.vue con validación de porcentaje [0-100]
  - Implementar botones de acción: editar, eliminar
  - Mostrar LoadingSpinner y ErrorMessage apropiadamente
  - _Requisitos: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 31.1 Escribir pruebas unitarias para componentes de tipos de servicios
  - Probar que TiposServiciosList muestra lista correctamente
  - Probar validación de porcentaje en formulario
  - Probar manejo de errores
  - _Requisitos: 2.1, 2.2, 2.3, 2.6_


### FRONTEND: Componentes de Servicios

- [x] 32. Implementar componentes de servicios
  - Crear ServiciosList.vue con tabla/lista responsive
  - Crear ServicioCard.vue mostrando fecha, empleado, tipo, precio y comisión
  - Crear ServicioForm.vue con selects para empleado y tipo de servicio
  - Crear ServicioFilters.vue con filtros por empleado y rango de fechas
  - Implementar date pickers para fechas
  - Cargar empleados y tipos de servicios en selects
  - Validar que precio sea positivo
  - Mostrar servicios ordenados por fecha descendente
  - _Requisitos: 3.1, 3.2, 3.3, 3.4, 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.3_

- [x] 32.1 Escribir pruebas unitarias para componentes de servicios
  - Probar que ServiciosList muestra servicios correctamente
  - Probar que ServicioFilters aplica filtros
  - Probar validación de precio en formulario
  - Probar ordenamiento por fecha
  - _Requisitos: 3.1, 3.2, 6.1, 6.2_

### FRONTEND: Componentes de Reportes

- [x] 33. Implementar componentes de reportes
  - Crear IngresosReport.vue con filtros de fecha y visualización de total
  - Crear BeneficiosReport.vue mostrando ingresos, comisiones y beneficios
  - Crear PagoEmpleadoReport.vue con selector de empleado y desglose de servicios
  - Implementar filtros de rango de fechas en todos los reportes
  - Mostrar valores monetarios con formato apropiado (símbolo $, decimales)
  - Crear tabla responsive para desglose de servicios
  - _Requisitos: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4_

- [x] 33.1 Escribir pruebas unitarias para componentes de reportes
  - Probar que IngresosReport muestra total correctamente
  - Probar que BeneficiosReport calcula correctamente
  - Probar que PagoEmpleadoReport muestra desglose
  - Probar formato monetario
  - _Requisitos: 4.1, 4.2, 4.3, 5.2, 5.4_

### FRONTEND: Vistas Principales

- [x] 34. Implementar vistas principales
  - Crear HomeView.vue con dashboard y resumen de estadísticas
  - Crear EmpleadosView.vue integrando EmpleadosList
  - Crear ServiciosView.vue integrando ServiciosList y ServicioFilters
  - Crear TiposServiciosView.vue integrando TiposServiciosList
  - Crear ReportesView.vue con tabs para diferentes reportes
  - Aplicar diseño mobile-first con Tailwind CSS
  - _Requisitos: Todos (vistas principales)_

- [x] 35. Implementar App.vue y navegación
  - Crear layout principal con AppHeader y AppNavigation
  - Implementar router-view para contenido dinámico
  - Configurar navegación responsive (menú hamburger en móvil)
  - Aplicar estilos globales con Tailwind
  - _Requisitos: Todos (layout)_

- [x] 36. Checkpoint - Verificar frontend completo
  - Probar todas las vistas en diferentes tamaños de pantalla
  - Verificar diseño mobile-first (320px, 768px, 1024px)
  - Probar flujo completo: crear empleado, tipo de servicio, registrar servicio, ver reportes
  - Verificar manejo de errores en UI
  - Asegurar que todos los tests pasen, preguntar al usuario si surgen dudas.


### INTEGRACIÓN Y PRUEBAS E2E

- [x] 37. Configurar pruebas E2E
  - Instalar Playwright o Cypress
  - Configurar scripts de prueba en package.json
  - Crear fixtures para datos de prueba
  - _Requisitos: Todos (testing E2E)_

- [x] 37.1 Escribir pruebas E2E para flujo completo
  - Probar crear empleado desde UI
  - Probar crear tipo de servicio desde UI
  - Probar registrar servicio desde UI
  - Probar consultar reportes desde UI
  - Probar filtrado de servicios
  - Probar validación de formularios
  - Probar diseño responsive en diferentes viewports
  - _Requisitos: Todos (flujo completo)_

- [x] 38. Integración backend-frontend
  - Verificar que CORS está configurado correctamente
  - Probar todas las llamadas API desde frontend
  - Verificar manejo de errores end-to-end
  - Probar persistencia: registrar datos, recargar página, verificar que persisten
  - _Requisitos: Todos (integración)_

### DOCUMENTACIÓN Y CONFIGURACIÓN FINAL

- [x] 39. Crear documentación del proyecto
  - Crear README.md del backend con instrucciones de instalación y ejecución
  - Crear README.md del frontend con instrucciones de instalación y ejecución
  - Documentar estructura del proyecto
  - Documentar endpoints de API
  - Incluir ejemplos de uso
  - Documentar variables de entorno necesarias
  - _Requisitos: Todos (documentación)_

- [x] 40. Configurar archivos de entorno
  - Crear .env.example para backend con DATABASE_URL, CORS_ORIGINS
  - Crear .env.example para frontend con VITE_API_URL
  - Documentar variables de entorno en README
  - _Requisitos: Todos (configuración)_

- [x] 41. Configurar scripts de desarrollo
  - Crear script para iniciar backend: uvicorn app.main:app --reload
  - Crear script para iniciar frontend: npm run dev
  - Crear script para ejecutar tests backend: pytest
  - Crear script para ejecutar tests frontend: npm run test:unit
  - Documentar comandos en README
  - _Requisitos: Todos (scripts)_

- [x] 42. Checkpoint final - Verificación completa del sistema
  - Ejecutar todos los tests unitarios del backend
  - Ejecutar todos los tests de propiedades con 100+ iteraciones
  - Ejecutar todos los tests de API
  - Ejecutar todos los tests unitarios del frontend
  - Ejecutar tests E2E
  - Verificar cobertura de código (objetivo: 80%+)
  - Probar flujo completo manualmente en diferentes dispositivos
  - Verificar persistencia: cerrar y reabrir aplicación, verificar que datos se mantienen
  - Verificar documentación automática de API en /docs
  - Asegurar que todos los tests pasen, preguntar al usuario si surgen dudas.


## Notas

- Las tareas marcadas con `*` son opcionales y pueden omitirse para un MVP más rápido
- Cada tarea referencia requisitos específicos para trazabilidad
- Los checkpoints aseguran validación incremental
- Las pruebas de propiedad validan propiedades universales de corrección
- Las pruebas unitarias validan ejemplos específicos y casos de borde
- Se recomienda usar Hypothesis para property-based testing con mínimo 100 iteraciones por propiedad

### Arquitectura

- **Backend**: FastAPI (Python) + SQLAlchemy + SQLite
- **Frontend**: Vue 3 + TypeScript + Tailwind CSS + Vite
- **Comunicación**: API REST con JSON
- **Persistencia**: SQLite con índices optimizados
- **Testing Backend**: pytest + Hypothesis + FastAPI TestClient
- **Testing Frontend**: Vitest + Vue Test Utils + Playwright/Cypress

### Estructura del Proyecto

```
salon-peluqueria/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── models.py            # Domain models
│   │   ├── orm_models.py        # SQLAlchemy ORM
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── repository.py        # Data access layer
│   │   ├── manager.py           # Business logic
│   │   ├── validators.py        # Validation logic
│   │   └── errors.py            # Error types
│   ├── tests/
│   │   ├── unit/                # Unit tests
│   │   ├── property/            # Property-based tests
│   │   └── api/                 # API integration tests
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/          # Vue components
│   │   ├── views/               # Vue views
│   │   ├── stores/              # Pinia stores
│   │   ├── services/            # API service
│   │   ├── types/               # TypeScript types
│   │   ├── router/              # Vue Router
│   │   ├── App.vue
│   │   └── main.ts
│   ├── tests/
│   │   ├── unit/                # Unit tests
│   │   └── e2e/                 # E2E tests
│   ├── package.json
│   ├── .env.example
│   └── README.md
└── README.md                     # Documentación general
```

### Comandos Útiles

**Backend**:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload

# Ejecutar tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app --cov-report=html

# Ejecutar property tests con más iteraciones
pytest tests/property/ --hypothesis-iterations=1000
```

**Frontend**:
```bash
# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# Ejecutar tests unitarios
npm run test:unit

# Ejecutar tests con cobertura
npm run test:unit -- --coverage

# Ejecutar tests E2E
npm run test:e2e

# Build para producción
npm run build
```

### Orden de Implementación Recomendado

1. **Backend primero**: Implementar modelos, lógica de negocio y API REST (tareas 1-20)
2. **Frontend después**: Implementar UI consumiendo la API (tareas 21-36)
3. **Integración**: Conectar ambas capas y probar E2E (tareas 37-38)
4. **Documentación**: Finalizar documentación y configuración (tareas 39-42)

Este enfoque permite probar el backend de forma independiente antes de construir el frontend, facilitando la detección temprana de errores.
