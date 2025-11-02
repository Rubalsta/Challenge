from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.session import get_db
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Crear un nuevo post (requiere autenticación)
    
    - **title**: Título del post (5-100 caracteres)
    - **content**: Contenido del post (mínimo 10 caracteres)
    """
    # Crear el post asociado al usuario actual
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        user_id=current_user.id  # Asignamos el post al usuario autenticado
    )
    
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    
    # Cargar las relaciones para la respuesta
    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.comments),
            selectinload(Post.tags)
        )
        .where(Post.id == new_post.id)
    )
    post = result.scalar_one()
    
    return post


@router.get("/", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar todos los posts con paginación
    
    - **skip**: Cuántos posts saltar (para paginación)
    - **limit**: Cuántos posts traer (máximo 100)
    """
    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.comments),
            selectinload(Post.tags)
        )
        .where(Post.is_deleted == False)
        .offset(skip)
        .limit(limit)
    )
    posts = result.scalars().all()
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post_by_id(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener un post específico por ID
    
    Incluye: autor, comentarios y tags
    """
    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.comments),
            selectinload(Post.tags)
        )
        .where(Post.id == post_id, Post.is_deleted == False)
    )
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post no encontrado"
        )
    
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar un post existente
    
    **Solo el autor del post puede actualizarlo**
    """
    # Buscar el post
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.is_deleted == False)
    )
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post no encontrado"
        )
    
    # Verificar que el usuario actual sea el autor
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este post"
        )
    
    # Actualizar solo los campos proporcionados
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    
    await db.commit()
    await db.refresh(post)
    
    # Cargar relaciones para la respuesta
    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.author),
            selectinload(Post.comments),
            selectinload(Post.tags)
        )
        .where(Post.id == post.id)
    )
    updated_post = result.scalar_one()
    
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar un post (soft delete)
    
    **Solo el autor del post puede eliminarlo**
    """
    # Buscar el post
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.is_deleted == False)
    )
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post no encontrado"
        )
    
    # Verificar que el usuario actual sea el autor
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este post"
        )
    
    # Soft delete
    post.is_deleted = True
    await db.commit()
    
    return None
