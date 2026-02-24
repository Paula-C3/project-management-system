from datetime import date
from sqalchemy import String, Date, ForaignKey
from sqalchemy import Mapped, mapped_column, relationship

from app.infra.db import Base

class ProjectModel(Base):

    __tablename__="projects"

    id: Mapped[str] = mapped_column(String, primary_key = True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[list["TaskModel"]] = relationship(

    )

class TaskModel(Base):

    __tablename__="tasks"

    id: Mapped[str] = mapped_column(String, primary_key = True)
    project_id: Mapped[str] = mapped_column(String, ForaignKey('project.id'), nullable=False)

    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    due_date: Mapped[date | None] = mapped_column