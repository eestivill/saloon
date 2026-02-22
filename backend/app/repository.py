"""
Capa de acceso a datos para el sistema de gestión de salón de peluquería.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models import Empleado, TipoServicio, ServicioRegistrado
from app.orm_models import Base, EmpleadoORM, TipoServicioORM, ServicioORM
from app.errors import PersistenceError


class DataRepository(ABC):
    """Interfaz abstracta para el repositorio de datos."""
    
    @abstractmethod
    def guardar_empleado(self, empleado: Empleado) -> None:
        """Guarda un empleado en el repositorio."""
        pass
    
    @abstractmethod
    def obtener_empleado(self, id: str) -> Optional[Empleado]:
        """Obtiene un empleado por su ID."""
        pass
    
    @abstractmethod
    def listar_empleados(self) -> List[Empleado]:
        """Lista todos los empleados."""
        pass
    
    @abstractmethod
    def eliminar_empleado(self, id: str) -> None:
        """Elimina un empleado del repositorio."""
        pass
    
    @abstractmethod
    def guardar_tipo_servicio(self, tipo: TipoServicio) -> None:
        """Guarda un tipo de servicio en el repositorio."""
        pass
    
    @abstractmethod
    def obtener_tipo_servicio(self, nombre: str) -> Optional[TipoServicio]:
        """Obtiene un tipo de servicio por su nombre."""
        pass
    
    @abstractmethod
    def listar_tipos_servicios(self) -> List[TipoServicio]:
        """Lista todos los tipos de servicios."""
        pass
    
    @abstractmethod
    def eliminar_tipo_servicio(self, nombre: str) -> None:
        """Elimina un tipo de servicio del repositorio."""
        pass
    
    @abstractmethod
    def guardar_servicio(self, servicio: ServicioRegistrado) -> None:
        """Guarda un servicio registrado en el repositorio."""
        pass
    
    @abstractmethod
    def listar_servicios(self) -> List[ServicioRegistrado]:
        """Lista todos los servicios registrados."""
        pass
    
    @abstractmethod
    def eliminar_servicio(self, id: str) -> None:
        """Elimina un servicio del repositorio."""
        pass


class SQLAlchemyRepository(DataRepository):
    """Implementación del repositorio usando SQLAlchemy."""
    
    def __init__(self, database_url: str = "sqlite:///salon.db"):
        """
        Inicializa el repositorio con la URL de la base de datos.
        
        Args:
            database_url: URL de conexión a la base de datos
        """
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        """
        Obtiene una sesión de base de datos.
        
        Returns:
            Session: Sesión de SQLAlchemy
        """
        return self.SessionLocal()
    
    def guardar_empleado(self, empleado: Empleado) -> None:
        """
        Guarda un empleado en la base de datos.
        
        Args:
            empleado: Empleado a guardar
            
        Raises:
            PersistenceError: Si ocurre un error al guardar
        """
        session = self.get_session()
        try:
            # Verificar si ya existe
            existing = session.query(EmpleadoORM).filter_by(id=empleado.id).first()
            
            if existing:
                # Actualizar
                existing.nombre = empleado.nombre
            else:
                # Crear nuevo
                orm_empleado = EmpleadoORM(
                    id=empleado.id,
                    nombre=empleado.nombre
                )
                session.add(orm_empleado)
            
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise PersistenceError(
                message=f"Error al guardar empleado: {str(e)}",
                context="guardar_empleado"
            )
        finally:
            session.close()
    
    def obtener_empleado(self, id: str) -> Optional[Empleado]:
        """
        Obtiene un empleado por su ID.
        
        Args:
            id: ID del empleado
            
        Returns:
            Empleado si existe, None en caso contrario
            
        Raises:
            PersistenceError: Si ocurre un error al consultar
        """
        session = self.get_session()
        try:
            orm_empleado = session.query(EmpleadoORM).filter_by(id=id).first()
            
            if orm_empleado:
                return Empleado.from_orm(orm_empleado)
            return None
        except SQLAlchemyError as e:
            raise PersistenceError(
                message=f"Error al obtener empleado: {str(e)}",
                context="obtener_empleado"
            )
        finally:
            session.close()
    
    def listar_empleados(self) -> List[Empleado]:
        """
        Lista todos los empleados.
        
        Returns:
            Lista de empleados
            
        Raises:
            PersistenceError: Si ocurre un error al consultar
        """
        session = self.get_session()
        try:
            orm_empleados = session.query(EmpleadoORM).all()
            return [Empleado.from_orm(orm_emp) for orm_emp in orm_empleados]
        except SQLAlchemyError as e:
            raise PersistenceError(
                message=f"Error al listar empleados: {str(e)}",
                context="listar_empleados"
            )
        finally:
            session.close()
    
    def eliminar_empleado(self, id: str) -> None:
        """
        Elimina un empleado de la base de datos.
        
        Args:
            id: ID del empleado a eliminar
            
        Raises:
            PersistenceError: Si ocurre un error al eliminar
        """
        session = self.get_session()
        try:
            orm_empleado = session.query(EmpleadoORM).filter_by(id=id).first()
            
            if orm_empleado:
                session.delete(orm_empleado)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise PersistenceError(
                message=f"Error al eliminar empleado: {str(e)}",
                context="eliminar_empleado"
            )
        finally:
            session.close()
    
    def guardar_tipo_servicio(self, tipo: TipoServicio) -> None:
        """
        Guarda un tipo de servicio en la base de datos.
        
        Args:
            tipo: Tipo de servicio a guardar
            
        Raises:
            PersistenceError: Si ocurre un error al guardar
        """
        session = self.get_session()
        try:
            # Verificar si ya existe
            existing = session.query(TipoServicioORM).filter_by(nombre=tipo.nombre).first()
            
            if existing:
                # Actualizar
                existing.descripcion = tipo.descripcion
                existing.porcentaje_comision = tipo.porcentaje_comision
            else:
                # Crear nuevo
                orm_tipo = TipoServicioORM(
                    nombre=tipo.nombre,
                    descripcion=tipo.descripcion,
                    porcentaje_comision=tipo.porcentaje_comision
                )
                session.add(orm_tipo)
            
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise PersistenceError(
                message=f"Error al guardar tipo de servicio: {str(e)}",
                context="guardar_tipo_servicio"
            )
        finally:
            session.close()
    
    def obtener_tipo_servicio(self, nombre: str) -> Optional[TipoServicio]:
        """
        Obtiene un tipo de servicio por su nombre.
        
        Args:
            nombre: Nombre del tipo de servicio
            
        Returns:
            TipoServicio si existe, None en caso contrario
            
        Raises:
            PersistenceError: Si ocurre un error al consultar
        """
        session = self.get_session()
        try:
            orm_tipo = session.query(TipoServicioORM).filter_by(nombre=nombre).first()
            
            if orm_tipo:
                return TipoServicio.from_orm(orm_tipo)
            return None
        except SQLAlchemyError as e:
            raise PersistenceError(
                message=f"Error al obtener tipo de servicio: {str(e)}",
                context="obtener_tipo_servicio"
            )
        finally:
            session.close()
    
    def listar_tipos_servicios(self) -> List[TipoServicio]:
        """
        Lista todos los tipos de servicios.
        
        Returns:
            Lista de tipos de servicios
            
        Raises:
            PersistenceError: Si ocurre un error al consultar
        """
        session = self.get_session()
        try:
            orm_tipos = session.query(TipoServicioORM).all()
            return [TipoServicio.from_orm(orm_tipo) for orm_tipo in orm_tipos]
        except SQLAlchemyError as e:
            raise PersistenceError(
                message=f"Error al listar tipos de servicios: {str(e)}",
                context="listar_tipos_servicios"
            )
        finally:
            session.close()
    
    def eliminar_tipo_servicio(self, nombre: str) -> None:
        """
        Elimina un tipo de servicio de la base de datos.
        
        Args:
            nombre: Nombre del tipo de servicio a eliminar
            
        Raises:
            PersistenceError: Si ocurre un error al eliminar
        """
        session = self.get_session()
        try:
            orm_tipo = session.query(TipoServicioORM).filter_by(nombre=nombre).first()
            
            if orm_tipo:
                session.delete(orm_tipo)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise PersistenceError(
                message=f"Error al eliminar tipo de servicio: {str(e)}",
                context="eliminar_tipo_servicio"
            )
        finally:
            session.close()
    
    def guardar_servicio(self, servicio: ServicioRegistrado) -> None:
        """
        Guarda un servicio registrado en la base de datos.
        
        Args:
            servicio: Servicio a guardar
            
        Raises:
            PersistenceError: Si ocurre un error al guardar
        """
        session = self.get_session()
        try:
            # Verificar si ya existe
            existing = session.query(ServicioORM).filter_by(id=servicio.id).first()
            
            if existing:
                # Actualizar
                existing.fecha = servicio.fecha
                existing.empleado_id = servicio.empleado_id
                existing.tipo_servicio = servicio.tipo_servicio
                existing.precio = servicio.precio
                existing.comision_calculada = servicio.comision_calculada
            else:
                # Crear nuevo
                orm_servicio = ServicioORM(
                    id=servicio.id,
                    fecha=servicio.fecha,
                    empleado_id=servicio.empleado_id,
                    tipo_servicio=servicio.tipo_servicio,
                    precio=servicio.precio,
                    comision_calculada=servicio.comision_calculada
                )
                session.add(orm_servicio)
            
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise PersistenceError(
                message=f"Error al guardar servicio: {str(e)}",
                context="guardar_servicio"
            )
        finally:
            session.close()
    
    def listar_servicios(self) -> List[ServicioRegistrado]:
        """
        Lista todos los servicios registrados.
        
        Returns:
            Lista de servicios registrados
            
        Raises:
            PersistenceError: Si ocurre un error al consultar
        """
        session = self.get_session()
        try:
            orm_servicios = session.query(ServicioORM).all()
            return [ServicioRegistrado.from_orm(orm_serv) for orm_serv in orm_servicios]
        except SQLAlchemyError as e:
            raise PersistenceError(
                message=f"Error al listar servicios: {str(e)}",
                context="listar_servicios"
            )
        finally:
            session.close()
    
    def eliminar_servicio(self, id: str) -> None:
        """
        Elimina un servicio de la base de datos.
        
        Args:
            id: ID del servicio a eliminar
            
        Raises:
            PersistenceError: Si ocurre un error al eliminar
        """
        session = self.get_session()
        try:
            orm_servicio = session.query(ServicioORM).filter_by(id=id).first()
            
            if orm_servicio:
                session.delete(orm_servicio)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise PersistenceError(
                message=f"Error al eliminar servicio: {str(e)}",
                context="eliminar_servicio"
            )
        finally:
            session.close()
