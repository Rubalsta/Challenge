from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TagBase(BaseModel):
    """Esquema base para el Tag

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos.
    """
    name: str = Field(..., min_length=1, max_length=50)
    
class TagCreate(TagBase):
    """Esquema para crear un nuevo Tag

    Args:
        TagBase (_type_): Campos comunes del Tag.
    """
    pass


class TagUpdate(BaseModel):
    """Esquema para actualizar un Tag existente

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    
    
    
class TagInDB(TagBase):
    """Esquema que representa un Tag almacenado en la base de datos

    Args:
        TagBase (_type_): Campos comunes del Tag.
    """
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config ={"from_attributes": True}
    
    
class TagResponse(TagInDB):
    """Esquema para la respuesta de un Tag

    Args:
        TagInDB (_type_): Campos del Tag en la base de datos.
    """
    pass
