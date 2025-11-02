from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Esquema para el token de autenticación

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos.
    """
    access_token: str
    token_type: str = " bearer"
    
class TokenData(BaseModel):
    """Esquema para los datos del token

    Args:
        BaseModel (_type_): Clase base de Pydantic para modelos de datos.
    """
    user_id: Optional[int] = None