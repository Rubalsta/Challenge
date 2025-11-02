from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.models.user import User
from app.core.security import verify_access_token

# Define el endpoint de login para OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Obtiene el usuario actual desde el token JWT.
    Esta dependencia se usa para proteger endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verificar el token
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extraer el user_id del token
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Buscar el usuario en la BD
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica que el usuario esté activo.
    Puedes agregar más validaciones aquí si necesitas.
    """
    return current_user