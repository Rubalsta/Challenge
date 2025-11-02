from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    """Campos comunes del Post

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos.
    """
    
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=10)
    
class PostCreate(PostBase):
    """Esquema para crear un nuevo Post

    Args:
        PostBase (_type_): Campos comunes del Post.
    """
    pass

class PostUpdate(BaseModel):
    """Esquema para actualizar un Post existente

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos
    """
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    content: Optional[str] = Field(None, min_length=10)
    
class PostInDB(PostBase):
    """Esquema que representa un Post almacenado en la base de datos

    Args:
        PostBase (_type_): Campos comunes del Post.
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        
class PostResponse(PostInDB):
    """Esquema para la respuesta del Post

    Args:
        PostInDB (_type_): Campos del Post en la base de datos.
    """
    pass