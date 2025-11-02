from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    """Campos comunes del Comment

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos.
    """
    
    content: str = Field(..., min_length=1, max_length=500)
    
class CommentCreate(CommentBase):
    """Esquema para crear un nuevo Comment

    Args:
        CommentBase (_type_): Campos comunes del Comment.
    """
    post_id: int
    
class CommentUpdate(BaseModel):
    """Esquema para actualizar un Comment existente

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos
    """
    content: Optional[str] = Field(None, min_length=1, max_length=500)
    
class CommentInDB(CommentBase):
    """Esquema que representa un Comment almacenado en la base de datos

    Args:
        CommentBase (_type_): Campos comunes del Comment.
    """
    id: int
    post_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config ={"from_attributes": True}
    
class CommentResponse(CommentInDB):
    """Esquema para la respuesta del Comment

    Args:
        CommentInDB (_type_): Campos del Comment en la base de datos.
    """
    pass