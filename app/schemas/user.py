from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.post import PostResponse

class UserBase(BaseModel):
    """Schema base para datos del usuario.

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos.
    """
    email: EmailStr
    username: str = Field(...,min_length=3, max_length=50)
    
class UserCreate(UserBase):
    """Schema para la creación de un nuevo usuario.

    Args:
        UserBase (_type_): Hereda los campos base del usuario.
    """
    password: str = Field(..., min_length=8, max_length=72)
    
class UserUpdate(BaseModel):
    """Schema para la actualización de datos del usuario.

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos.
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=72)
    is_active: Optional[bool] = None
    
    
class UserInDB(UserBase):
    """Schema que representa un usuario almacenado en la base de datos.

    Args:
        UserBase (_type_): Hereda los campos base del usuario.
    """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True }
    
class UserResponse(UserInDB):
    """Schema para la respuesta de datos del usuario.

    Args:
        UserInDB (_type_): Hereda los campos del usuario en la base de datos.
    """
    pass

class UserWithPosts(UserResponse):
    """Schema de Usuarios con Post Incluidos

    Args:
        UserResponse (_type_): Hereda los campos del usuario en la base de datos.
    """
    posts: List['PostResponse'] = []