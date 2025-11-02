from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserWithPosts
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener información del usuario actual autenticado
    """
    return current_user


@router.get("/{user_id}", response_model=UserWithPosts)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener un usuario específico por ID con sus posts
    """
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id, User.is_deleted == False)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar todos los usuarios con paginación
    """
    result = await db.execute(
        select(User)
        .where(User.is_deleted == False)
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()
    return users


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar información del usuario actual
    """
    # Verificar si el email ya existe (si se está cambiando)
    if user_data.email and user_data.email != current_user.email:
        result = await db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso"
            )
    
    # Verificar si el username ya existe (si se está cambiando)
    if user_data.username and user_data.username != current_user.username:
        result = await db.execute(select(User).where(User.username == user_data.username))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya está en uso"
            )
    
    # Actualizar solo los campos proporcionados
    if user_data.email:
        current_user.email = user_data.email
    if user_data.username:
        current_user.username = user_data.username
    if user_data.password:
        from app.core.security import get_password_hash
        current_user.hashed_password = get_password_hash(user_data.password)
    if user_data.is_active is not None:
        current_user.is_active = user_data.is_active
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar (soft delete) el usuario actual
    """
    current_user.is_deleted = True
    current_user.is_active = False
    
    await db.commit()
    
    return None
