
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.base import Base

# Tabla intermedia para la relación muchos a muchos entre Post y Tag
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)
