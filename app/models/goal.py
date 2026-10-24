from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
if TYPE_CHECKING:
    from ..models.task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
    
    @classmethod
    def from_dict(cls, goal_data):
        goal = cls()
        goal.title = goal_data["title"]
        return goal
        