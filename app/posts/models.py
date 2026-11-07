from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app import db


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

    def __repr__(self):
        return f'<Post(title={self.title})>'