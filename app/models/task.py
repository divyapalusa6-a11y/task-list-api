from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
        }

    @classmethod
    def from_dict(cls, task_data):
<<<<<<< HEAD
        return cls(
        title=task_data["title"],
        description=task_data["description"],
        completed_at=None
    )

        
=======
        if "title" not in task_data:
            raise KeyError("title")
        if "description" not in task_data:
            raise KeyError("description")

        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at"),
        )
>>>>>>> 5b65398d079d58ae4ed6876b4acd3297ea7a1450
