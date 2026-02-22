"""
Aplicación FastAPI para el sistema de gestión de salón de peluquería.
"""
import logging
from datetime import date
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.repository import SQLAlchemyRepository
from app.manager import SalonManager
from app.errors import ValidationError, NotFoundError, DuplicateError, PersistenceError

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Salón de Peluquería",
    description="API REST para gestión de empleados, servicios y comisiones",
    version="1.0.0"
)

# Configurar middleware CORS para permitir acceso desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Desarrollo
        "https://stephany-mondragon-frontend.onrender.com",  # Producción
        "*"  # Permitir todos los orígenes temporalmente
    ],  # URL del frontend en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear instancias de repositorio y manager
# Determinar ruta de base de datos según entorno
import os
db_path = os.getenv("DATABASE_PATH", "salon.db")
repository = SQLAlchemyRepository(f"sqlite:///{db_path}")
salon_manager = SalonManager(repository)


# Exception Handlers Globales

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Maneja errores de SQLAlchemy."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "database_error",
            "message": "Error al procesar la solicitud en la base de datos"
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones no capturadas."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "Error interno del servidor"
        }
    )


# Middleware para logging de peticiones
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Registra todas las peticiones HTTP."""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response


# Health check endpoint
@app.get("/")
async def root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {
        "message": "Sistema de Gestión de Salón de Peluquería API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Endpoint de health check."""
    return {"status": "healthy"}


# ============================================================================
# ENDPOINTS DE EMPLEADOS
# ============================================================================

from fastapi import HTTPException, status, Query
from typing import List, Optional
from app.schemas import (
    EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse,
    IngresosResponse, BeneficiosResponse, DesglosePagoResponse
)
from app.result import Ok, Err


@app.get("/api/empleados", response_model=List[EmpleadoResponse])
async def listar_empleados():
    """
    Lista todos los empleados registrados.
    
    Returns:
        Lista de empleados
    """
    empleados = salon_manager.listar_empleados()
    return [EmpleadoResponse(id=emp.id, nombre=emp.nombre) for emp in empleados]


@app.get("/api/empleados/{id}", response_model=EmpleadoResponse)
async def obtener_empleado(id: str):
    """
    Obtiene un empleado por su ID.
    
    Args:
        id: Identificador del empleado
        
    Returns:
        Empleado encontrado
        
    Raises:
        HTTPException 404: Si el empleado no existe
    """
    empleado = salon_manager.obtener_empleado(id)
    
    if empleado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Empleado con identificador '{id}' no encontrado"
            }
        )
    
    return EmpleadoResponse(id=empleado.id, nombre=empleado.nombre)


@app.post("/api/empleados", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
async def crear_empleado(empleado: EmpleadoCreate):
    """
    Crea un nuevo empleado.
    
    Args:
        empleado: Datos del empleado a crear
        
    Returns:
        Empleado creado
        
    Raises:
        HTTPException 409: Si el ID del empleado ya existe
    """
    resultado = salon_manager.crear_empleado(empleado.id, empleado.nombre)
    
    match resultado:
        case Ok(emp):
            return EmpleadoResponse(id=emp.id, nombre=emp.nombre)
        case Err(DuplicateError(entity, identifier)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "duplicate_error",
                    "message": f"{entity} con identificador '{identifier}' ya existe"
                }
            )
        case Err(error):
            # Caso genérico para otros errores
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": str(error)
                }
            )


@app.put("/api/empleados/{id}", response_model=EmpleadoResponse)
async def actualizar_empleado(id: str, empleado: EmpleadoUpdate):
    """
    Actualiza un empleado existente.
    
    Args:
        id: Identificador del empleado a actualizar
        empleado: Nuevos datos del empleado
        
    Returns:
        Empleado actualizado
        
    Raises:
        HTTPException 404: Si el empleado no existe
    """
    resultado = salon_manager.actualizar_empleado(id, empleado.nombre)
    
    match resultado:
        case Ok(emp):
            return EmpleadoResponse(id=emp.id, nombre=emp.nombre)
        case Err(NotFoundError(entity, identifier)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "not_found",
                    "message": f"{entity} con identificador '{identifier}' no encontrado"
                }
            )
        case Err(error):
            # Caso genérico para otros errores
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": str(error)
                }
            )


@app.delete("/api/empleados/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_empleado(id: str):
    """
    Elimina un empleado.
    
    Args:
        id: Identificador del empleado a eliminar
        
    Raises:
        HTTPException 404: Si el empleado no existe
    """
    # Verificar que el empleado existe
    empleado = salon_manager.obtener_empleado(id)
    
    if empleado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Empleado con identificador '{id}' no encontrado"
            }
        )
    
    # Eliminar el empleado
    salon_manager.repository.eliminar_empleado(id)
    
    return None


# ============================================================================
# ENDPOINTS DE TIPOS DE SERVICIOS
# ============================================================================

from app.schemas import TipoServicioCreate, TipoServicioUpdate, TipoServicioResponse


@app.get("/api/tipos-servicios", response_model=List[TipoServicioResponse])
async def listar_tipos_servicios():
    """
    Lista todos los tipos de servicios registrados.
    
    Returns:
        Lista de tipos de servicios
    """
    tipos = salon_manager.listar_tipos_servicios()
    return [
        TipoServicioResponse(
            nombre=tipo.nombre,
            descripcion=tipo.descripcion,
            porcentaje_comision=tipo.porcentaje_comision,
            precio_por_defecto=tipo.precio_por_defecto
        )
        for tipo in tipos
    ]


@app.get("/api/tipos-servicios/{nombre}", response_model=TipoServicioResponse)
async def obtener_tipo_servicio(nombre: str):
    """
    Obtiene un tipo de servicio por su nombre.
    
    Args:
        nombre: Nombre del tipo de servicio
        
    Returns:
        Tipo de servicio encontrado
        
    Raises:
        HTTPException 404: Si el tipo de servicio no existe
    """
    tipo = salon_manager.obtener_tipo_servicio(nombre)
    
    if tipo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"TipoServicio con identificador '{nombre}' no encontrado"
            }
        )
    
    return TipoServicioResponse(
        nombre=tipo.nombre,
        descripcion=tipo.descripcion,
        porcentaje_comision=tipo.porcentaje_comision,
        precio_por_defecto=tipo.precio_por_defecto
    )


@app.post("/api/tipos-servicios", response_model=TipoServicioResponse, status_code=status.HTTP_201_CREATED)
async def crear_tipo_servicio(tipo: TipoServicioCreate):
    """
    Crea un nuevo tipo de servicio.
    
    Args:
        tipo: Datos del tipo de servicio a crear
        
    Returns:
        Tipo de servicio creado
        
    Raises:
        HTTPException 400: Si el porcentaje de comisión es inválido
        HTTPException 409: Si el nombre del tipo de servicio ya existe
    """
    resultado = salon_manager.crear_tipo_servicio(
        tipo.nombre,
        tipo.descripcion,
        tipo.porcentaje_comision,
        tipo.precio_por_defecto
    )
    
    match resultado:
        case Ok(tipo_servicio):
            return TipoServicioResponse(
                nombre=tipo_servicio.nombre,
                descripcion=tipo_servicio.descripcion,
                porcentaje_comision=tipo_servicio.porcentaje_comision,
                precio_por_defecto=tipo_servicio.precio_por_defecto
            )
        case Err(DuplicateError(entity, identifier)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "duplicate_error",
                    "message": f"{entity} con identificador '{identifier}' ya existe"
                }
            )
        case Err(ValidationError(message, field)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": message,
                    "field": field
                }
            )
        case Err(error):
            # Caso genérico para otros errores
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": str(error)
                }
            )


@app.put("/api/tipos-servicios/{nombre}", response_model=TipoServicioResponse)
async def actualizar_tipo_servicio(nombre: str, tipo: TipoServicioUpdate):
    """
    Actualiza un tipo de servicio existente.
    
    Args:
        nombre: Nombre del tipo de servicio a actualizar
        tipo: Nuevos datos del tipo de servicio
        
    Returns:
        Tipo de servicio actualizado
        
    Raises:
        HTTPException 400: Si el porcentaje de comisión es inválido
        HTTPException 404: Si el tipo de servicio no existe
    """
    # Obtener el tipo de servicio existente
    tipo_existente = salon_manager.obtener_tipo_servicio(nombre)
    
    if tipo_existente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"TipoServicio con identificador '{nombre}' no encontrado"
            }
        )
    
    # Determinar qué actualizar
    nueva_descripcion = tipo.descripcion if tipo.descripcion is not None else tipo_existente.descripcion
    nuevo_porcentaje = tipo.porcentaje_comision if tipo.porcentaje_comision is not None else tipo_existente.porcentaje_comision
    nuevo_precio = tipo.precio_por_defecto if tipo.precio_por_defecto is not None else tipo_existente.precio_por_defecto
    
    # Actualizar el tipo de servicio
    resultado = salon_manager.actualizar_tipo_servicio(nombre, nuevo_porcentaje, nuevo_precio)
    
    match resultado:
        case Ok(tipo_actualizado):
            # Si se proporcionó una nueva descripción o precio, actualizarlos también
            if tipo.descripcion is not None or tipo.precio_por_defecto is not None:
                from app.models import TipoServicio
                tipo_completo = TipoServicio(
                    nombre=nombre,
                    descripcion=nueva_descripcion,
                    porcentaje_comision=nuevo_porcentaje,
                    precio_por_defecto=nuevo_precio
                )
                salon_manager.repository.guardar_tipo_servicio(tipo_completo)
                tipo_actualizado = tipo_completo
            
            return TipoServicioResponse(
                nombre=tipo_actualizado.nombre,
                descripcion=tipo_actualizado.descripcion,
                porcentaje_comision=tipo_actualizado.porcentaje_comision,
                precio_por_defecto=tipo_actualizado.precio_por_defecto
            )
        case Err(ValidationError(message, field)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": message,
                    "field": field
                }
            )
        case Err(NotFoundError(entity, identifier)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "not_found",
                    "message": f"{entity} con identificador '{identifier}' no encontrado"
                }
            )
        case Err(error):
            # Caso genérico para otros errores
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": str(error)
                }
            )


@app.delete("/api/tipos-servicios/{nombre}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_tipo_servicio(nombre: str):
    """
    Elimina un tipo de servicio.
    
    Args:
        nombre: Nombre del tipo de servicio a eliminar
        
    Raises:
        HTTPException 404: Si el tipo de servicio no existe
    """
    # Verificar que el tipo de servicio existe
    tipo = salon_manager.obtener_tipo_servicio(nombre)
    
    if tipo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"TipoServicio con identificador '{nombre}' no encontrado"
            }
        )
    
    # Eliminar el tipo de servicio
    salon_manager.repository.eliminar_tipo_servicio(nombre)
    
    return None


# ============================================================================
# ENDPOINTS DE SERVICIOS
# ============================================================================

from typing import Optional
from app.schemas import ServicioCreate, ServicioResponse


@app.get("/api/servicios", response_model=List[ServicioResponse])
async def listar_servicios(
    empleado_id: Optional[str] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None
):
    """
    Lista servicios con filtros opcionales.
    
    Args:
        empleado_id: Filtrar por ID de empleado (opcional)
        fecha_inicio: Filtrar desde esta fecha (opcional)
        fecha_fin: Filtrar hasta esta fecha (opcional)
        
    Returns:
        Lista de servicios filtrados, ordenados por fecha descendente
        
    Raises:
        HTTPException 400: Si el rango de fechas es inválido
    """
    # Validar rango de fechas si ambas están presentes
    if fecha_inicio is not None and fecha_fin is not None:
        from app.validators import Validator
        validacion_fechas = Validator.validar_rango_fechas(fecha_inicio, fecha_fin)
        if isinstance(validacion_fechas, Err):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": "La fecha de inicio no puede ser posterior a la fecha de fin"
                }
            )
    
    # Obtener servicios filtrados
    servicios = salon_manager.obtener_servicios(
        empleado_id=empleado_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    
    return [
        ServicioResponse(
            id=servicio.id,
            fecha=servicio.fecha,
            empleado_id=servicio.empleado_id,
            tipo_servicio=servicio.tipo_servicio,
            precio=servicio.precio,
            comision_calculada=servicio.comision_calculada
        )
        for servicio in servicios
    ]


@app.get("/api/servicios/{id}", response_model=ServicioResponse)
async def obtener_servicio(id: str):
    """
    Obtiene un servicio por su ID.
    
    Args:
        id: Identificador del servicio
        
    Returns:
        Servicio encontrado
        
    Raises:
        HTTPException 404: Si el servicio no existe
    """
    # Buscar el servicio en la lista de todos los servicios
    servicios = salon_manager.obtener_servicios()
    servicio = next((s for s in servicios if s.id == id), None)
    
    if servicio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Servicio con identificador '{id}' no encontrado"
            }
        )
    
    return ServicioResponse(
        id=servicio.id,
        fecha=servicio.fecha,
        empleado_id=servicio.empleado_id,
        tipo_servicio=servicio.tipo_servicio,
        precio=servicio.precio,
        comision_calculada=servicio.comision_calculada
    )


@app.post("/api/servicios", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
async def registrar_servicio(servicio: ServicioCreate):
    """
    Registra un nuevo servicio.
    
    La comisión se calcula automáticamente basándose en el porcentaje
    del tipo de servicio asociado.
    
    Args:
        servicio: Datos del servicio a registrar
        
    Returns:
        Servicio registrado con comisión calculada
        
    Raises:
        HTTPException 400: Si los datos son inválidos
        HTTPException 404: Si el empleado o tipo de servicio no existen
    """
    resultado = salon_manager.registrar_servicio(
        fecha=servicio.fecha,
        empleado_id=servicio.empleado_id,
        tipo_servicio=servicio.tipo_servicio,
        precio=servicio.precio
    )
    
    match resultado:
        case Ok(servicio_registrado):
            return ServicioResponse(
                id=servicio_registrado.id,
                fecha=servicio_registrado.fecha,
                empleado_id=servicio_registrado.empleado_id,
                tipo_servicio=servicio_registrado.tipo_servicio,
                precio=servicio_registrado.precio,
                comision_calculada=servicio_registrado.comision_calculada
            )
        case Err(NotFoundError(entity, identifier)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "not_found",
                    "message": f"{entity} con identificador '{identifier}' no encontrado"
                }
            )
        case Err(ValidationError(message, field)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": message,
                    "field": field
                }
            )
        case Err(error):
            # Caso genérico para otros errores
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "validation_error",
                    "message": str(error)
                }
            )


@app.delete("/api/servicios/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_servicio(id: str):
    """
    Elimina un servicio.
    
    Args:
        id: Identificador del servicio a eliminar
        
    Raises:
        HTTPException 404: Si el servicio no existe
    """
    # Verificar que el servicio existe
    servicios = salon_manager.obtener_servicios()
    servicio = next((s for s in servicios if s.id == id), None)
    
    if servicio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Servicio con identificador '{id}' no encontrado"
            }
        )
    
    # Eliminar el servicio
    salon_manager.repository.eliminar_servicio(id)
    
    return None



# ============================================================================
# ENDPOINTS DE REPORTES
# ============================================================================

@app.get("/api/reportes/ingresos", response_model=IngresosResponse)
async def calcular_ingresos(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio del período (opcional)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin del período (opcional)")
):
    """
    Calcula los ingresos totales con filtros opcionales por fecha.
    
    Args:
        fecha_inicio: Filtrar desde esta fecha (opcional)
        fecha_fin: Filtrar hasta esta fecha (opcional)
        
    Returns:
        Total de ingresos con formato monetario apropiado
        
    Raises:
        HTTPException 400: Si el rango de fechas es inválido
    """
    # Validar rango de fechas
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "validation_error",
                "message": "La fecha de inicio no puede ser posterior a la fecha de fin"
            }
        )
    
    # Calcular ingresos
    total = salon_manager.calcular_ingresos_totales(fecha_inicio, fecha_fin)
    
    return IngresosResponse(
        total=total,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


@app.get("/api/reportes/beneficios", response_model=BeneficiosResponse)
async def calcular_beneficios(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio del período (opcional)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin del período (opcional)")
):
    """
    Calcula los beneficios (ingresos - comisiones) con filtros opcionales por fecha.
    
    Args:
        fecha_inicio: Filtrar desde esta fecha (opcional)
        fecha_fin: Filtrar hasta esta fecha (opcional)
        
    Returns:
        Ingresos, comisiones y beneficios con formato monetario apropiado
        
    Raises:
        HTTPException 400: Si el rango de fechas es inválido
    """
    # Validar rango de fechas
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "validation_error",
                "message": "La fecha de inicio no puede ser posterior a la fecha de fin"
            }
        )
    
    # Obtener servicios filtrados para calcular ingresos y comisiones
    from decimal import Decimal
    servicios = salon_manager.obtener_servicios(
        empleado_id=None,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    
    # Calcular ingresos y comisiones
    ingresos = sum((s.precio for s in servicios), Decimal("0"))
    comisiones = sum((s.comision_calculada for s in servicios), Decimal("0"))
    beneficios = ingresos - comisiones
    
    return BeneficiosResponse(
        ingresos=ingresos,
        comisiones=comisiones,
        beneficios=beneficios,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


@app.get("/api/empleados/{id}/pago", response_model=DesglosePagoResponse)
async def calcular_pago_empleado(
    id: str,
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio del período (opcional)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin del período (opcional)")
):
    """
    Calcula el pago de un empleado con filtros opcionales por fecha.
    
    Args:
        id: Identificador del empleado
        fecha_inicio: Filtrar desde esta fecha (opcional)
        fecha_fin: Filtrar hasta esta fecha (opcional)
        
    Returns:
        Desglose de pago con lista de servicios y total con formato monetario apropiado
        
    Raises:
        HTTPException 404: Si el empleado no existe
        HTTPException 400: Si el rango de fechas es inválido
    """
    # Verificar que el empleado existe
    empleado = salon_manager.obtener_empleado(id)
    if empleado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"Empleado con identificador '{id}' no encontrado"
            }
        )
    
    # Validar rango de fechas
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "validation_error",
                "message": "La fecha de inicio no puede ser posterior a la fecha de fin"
            }
        )
    
    # Calcular pago del empleado
    desglose = salon_manager.calcular_pago_empleado(id, fecha_inicio, fecha_fin)
    
    return DesglosePagoResponse(
        empleado_id=desglose.empleado_id,
        empleado_nombre=desglose.empleado_nombre,
        servicios=desglose.servicios,
        total=desglose.total
    )
