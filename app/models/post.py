from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.database.mixins import TimestampMixin, SoftDeleteMixin
from app.models.associations import post_tags

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
    title = Column(String(200), index=True, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relaciones
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")