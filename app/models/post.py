from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.database.mixins import TimestampMixin, SoftDeleteMixin

class Post(Base,TimestampMixin,SoftDeleteMixin):
    """
    Clase que representa una publicación en el sistema.

    Args:
        Base (_type_): Clase base para todos los modelos de la base de datos.
        TimestampMixin (_type_): Annade campos de marca de tiempo.
        SoftDeleteMixin (_type_): Annade soporte para eliminación lógica.
    """
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    
    # Relaciones
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")