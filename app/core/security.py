from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña proporcionada coincide con la contraseña hasheada almacenada.

    Args:
        plain_password (str): Contraseña en texto plano proporcionada por el usuario.
        hashed_password (str): Contraseña hasheada almacenada en la base de datos.

    Returns:
        bool: True si las contraseñas coinciden, False en caso contrario.
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    """Genera un hash seguro para la contraseña proporcionada.

    Args:
        password (str): Contraseña en texto plano.

    Returns:
        str: Contraseña hasheada.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token de acceso JWT con la información proporcionada y una fecha de expiración opcional.

    Args:
        data (dict): Datos que se incluirán en el payload del token.
        expires_delta (Optional[timedelta], optional): Tiempo hasta la expiración del token. Si no se proporciona, se usará el valor por defecto. Defaults to None.

    Returns:
        str: Token JWT generado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str) -> Optional[dict]:
    """Verifica la validez del token de acceso JWT y decodifica su contenido.

    Args:
        token (str): Token JWT a verificar.
    
    Returns:
        Optional[dict]: Payload decodificado si el token es válido, None en caso contrario.
    """
    try:
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    
    except JWTError:
        return None