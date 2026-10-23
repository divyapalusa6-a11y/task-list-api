from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore[import-not-found]
from ..db import db
#from ..models.goal import Goal
from sqlalchemy import ForeignKey  # type: ignore[import-not-found]
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")
    
    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.completed_at is not None
        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id
        return task_as_dict
    
    @classmethod
    def from_dict(cls, task_data):
        task = cls()
        task.title = task_data["title"]
        task.description = task_data["description"]
        task.completed_at = task_data.get("completed_at")

        if "goal_id" in task_data:
            task.goal_id = task_data["goal_id"]
        return task
    

        
        