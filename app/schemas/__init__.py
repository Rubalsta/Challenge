
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserInDB, UserWithPosts
from app.schemas.post import PostCreate, PostResponse, PostUpdate, PostInDB
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate,CommentInDB
from app.schemas.tag import TagCreate,  TagUpdate , TagResponse, TagInDB 
from app.schemas.token import Token, TokenData

from pydantic import ConfigDict
# Resuelve el problema de referencias circulares entre esquemas
PostResponse.model_rebuild()
CommentResponse.model_rebuild()
UserWithPosts.model_rebuild()

__all__ = [
    "UserCreate",
    "UserResponse",
    "UserUpdate",     
    "UserInDB",
    "PostCreate",
    "PostResponse",
    "PostUpdate",
    "PostInDB",
    "CommentCreate",
    "CommentResponse",
    "CommentUpdate",
    "CommentInDB",
    "TagCreate",
    "TagResponse",
    "TagUpdate",
    "TagInDB",
    "Token",
    "TokenData"
]