from sqlalchemy import Column, Integer,String
from app.database.base import Base
from app.database.mixins import TimestampMixin, SoftDeleteMixin

class Tag(Base, TimestampMixin, SoftDeleteMixin):
    """
    Clase que representa una etiqueta (tag) en el sistema.

    Args:
        Base (_type_): Clase base para todos los modelos de la base de datos.
        TimestampMixin (_type_): Annade campos de marca de tiempo.
        SoftDeleteMixin (_type_): Annade soporte para eliminación lógica.
    """
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)