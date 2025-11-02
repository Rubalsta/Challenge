from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.session import get_db
from app.models.tag import Tag
from app.models.user import User
from app.schemas.tag import TagCreate, TagUpdate, TagResponse
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Crear un nuevo tag
    
    - **name**: Nombre del tag (1-50 caracteres, único)
    
    Requiere autenticación
    """
    # Verificar si el tag ya existe
    result = await db.execute(
        select(Tag).where(Tag.name == tag_data.name, Tag.is_deleted == False)
    )
    existing_tag = result.scalar_one_or_none()
    
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un tag con ese nombre"
        )
    
    # Crear el tag
    new_tag = Tag(name=tag_data.name)
    
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    
    return new_tag


@router.get("/", response_model=List[TagResponse])
async def get_tags(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Número de registros a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar todos los tags con paginación
    """
    result = await db.execute(
        select(Tag)
        .where(Tag.is_deleted == False)
        .offset(skip)
        .limit(limit)
    )
    tags = result.scalars().all()
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag_by_id(
    tag_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener un tag específico por ID
    """
    result = await db.execute(
        select(Tag).where(Tag.id == tag_id, Tag.is_deleted == False)
    )
    tag = result.scalar_one_or_none()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag no encontrado"
        )
    
    return tag


@router.get("/name/{tag_name}", response_model=TagResponse)
async def get_tag_by_name(
    tag_name: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener un tag específico por nombre
    """
    result = await db.execute(
        select(Tag).where(Tag.name == tag_name, Tag.is_deleted == False)
    )
    tag = result.scalar_one_or_none()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag no encontrado"
        )
    
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar un tag existente
    
    Requiere autenticación
    """
    # Buscar el tag
    result = await db.execute(
        select(Tag).where(Tag.id == tag_id, Tag.is_deleted == False)
    )
    tag = result.scalar_one_or_none()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag no encontrado"
        )
    
    # Verificar si el nuevo nombre ya existe
    if tag_data.name and tag_data.name != tag.name:
        result = await db.execute(
            select(Tag).where(Tag.name == tag_data.name, Tag.is_deleted == False)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un tag con ese nombre"
            )
        tag.name = tag_data.name
    
    await db.commit()
    await db.refresh(tag)
    
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar un tag (soft delete)
    
    Requiere autenticación 
    """
    # Buscar el tag
    result = await db.execute(
        select(Tag).where(Tag.id == tag_id, Tag.is_deleted == False)
    )
    tag = result.scalar_one_or_none()
    
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag no encontrado"
        )
    
    # Soft delete
    tag.is_deleted = True
    await db.commit()
    
    return None