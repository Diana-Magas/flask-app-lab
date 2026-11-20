from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(150))
    content: Mapped[str] = mapped_column(sa.Text)
    posted: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    category: Mapped[Optional[str]] = mapped_column(
        sa.Enum('news', 'publication', 'tech', 'other', name='post_category')
    )
    is_active: Mapped[bool] = mapped_column(default=True, server_default=sa.true())
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")

    def __repr__(self):
        return f'<Post(title={self.title})>'


class Tag(db.Model):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")