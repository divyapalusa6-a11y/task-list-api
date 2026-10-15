from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    description: Mapped[str] = mapped_column(db.String(200), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=None)
