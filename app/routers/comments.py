from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.session import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Crear un nuevo comentario en un post
    
    - **content**: Contenido del comentario (1-500 caracteres)
    - **post_id**: ID del post al que pertenece el comentario
    """
    # Verificar que el post existe
    result = await db.execute(
        select(Post).where(Post.id == comment_data.post_id, Post.is_deleted == False)
    )
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post no encontrado"
        )
    
    # Crear el comentario
    new_comment = Comment(
        content=comment_data.content,
        post_id=comment_data.post_id,
        user_id=current_user.id
    )
    
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    
    # Cargar la relación con el autor
    result = await db.execute(
        select(Comment)
        .options(selectinload(Comment.author))
        .where(Comment.id == new_comment.id)
    )
    comment = result.scalar_one()
    
    return comment


@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def get_comments_by_post(
    post_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar todos los comentarios de un post específico
    """
    # Verificar que el post existe
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.is_deleted == False)
    )
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post no encontrado"
        )
    
    # Obtener comentarios del post
    result = await db.execute(
        select(Comment)
        .options(selectinload(Comment.author))
        .where(Comment.post_id == post_id, Comment.is_deleted == False)
        .offset(skip)
        .limit(limit)
    )
    comments = result.scalars().all()
    
    return comments


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment_by_id(
    comment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener un comentario específico por ID
    """
    result = await db.execute(
        select(Comment)
        .options(selectinload(Comment.author))
        .where(Comment.id == comment_id, Comment.is_deleted == False)
    )
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentario no encontrado"
        )
    
    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar un comentario existente
    
    **Solo el autor del comentario puede actualizarlo**
    """
    # Buscar el comentario
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.is_deleted == False)
    )
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentario no encontrado"
        )
    
    # Verificar que el usuario actual sea el autor
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este comentario"
        )
    
    # Actualizar el contenido
    if comment_data.content is not None:
        comment.content = comment_data.content
    
    await db.commit()
    await db.refresh(comment)
    
    # Cargar relación con el autor
    result = await db.execute(
        select(Comment)
        .options(selectinload(Comment.author))
        .where(Comment.id == comment.id)
    )
    updated_comment = result.scalar_one()
    
    return updated_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar un comentario (soft delete)
    
    **Solo el autor del comentario puede eliminarlo**
    """
    # Buscar el comentario
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.is_deleted == False)
    )
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentario no encontrado"
        )
    
    # Verificar que el usuario actual sea el autor
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este comentario"
        )
    
    # Soft delete
    comment.is_deleted = True
    await db.commit()
    
    return None