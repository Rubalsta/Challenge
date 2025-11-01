from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.database.mixins import TimestampMixin, SoftDeleteMixin

class Comment(Base, TimestampMixin, SoftDeleteMixin):
    """
    Clase que representa un comentario en una publicación.

    Args:
        Base (_type_): Clase base para todos los modelos de la base de datos.
        TimestampMixin (_type_): Annade campos de marca de tiempo.
        SoftDeleteMixin (_type_): Annade soporte para eliminación lógica.
    """
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relaciones
    post = relationship("Post", back_populates="comments")
    author = relationship("User")