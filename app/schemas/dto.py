""" Definimos que estructuras salen y entran al servicio mediante la API """

from datetime import date
from pydantic import BaseModel, Field
from app.domain.enums import TaskStatus

class ProjectCreate(BaseModel):
    name: str = Field(min_lenght = 5)
    
class ProjectOut(BaseModel):
    id: str
    name: str
    
class TaskCreate(BaseModel):
    title: str = Field(min_lenght = 5)
    task_type: str = Field(pattern = '^(bug|feature|chore)$')   # exp. regular (^) inicio, ($)final
    due_date: date | None
    
class TaskUpdate(BaseModel):
    title: str|None = Field(default = None, min_lenght = 5)
    due_date: date|None = None
    status: TaskStatus|None = None
    
class TaskOut(BaseModel):
    ide: str
    project_id: str
    title: str
    status: TaskStatus
    due_date: date|None
    priority_score: int
    
    
    