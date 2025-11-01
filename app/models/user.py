from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.database.mixins import TimestampMixin, SoftDeleteMixin

class User(Base, TimestampMixin, SoftDeleteMixin):
    """
    Clase que representa a un usuario en el sistema.

    Args:
        Base (_type_): Clase base para todos los modelos de la base de datos.
        TimestampMixin (_type_): Annade campos de marca de tiempo.
        SoftDeleteMixin (_type_): Annade soporte para eliminación lógica.
    """
    __table__ = "users"
    
    id = Column(Integer, primary_key=True, index = True)
    email = Column(String, unique =  True, index=True,nullable=False)
    username = Column(String, unique=True,index=True,nullable = False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relación con otros modelos (Posts)
    posts = relationship("Post", back_populates="author",cascade="all, delete-orphan")