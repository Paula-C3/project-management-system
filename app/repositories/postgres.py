from __future__ import annotations
from sqlalchemy import select
from sqlalchemy import Session 
from app.domain.entities import Project, Task
from app.domain.enums import TaskStatus
from app.domain.exceptions import NotFoundError
from app.domain.priority import BugPriority, FeaturePriority, ChorePriority
from app.infra.models import ProjectModel, TaskModel

class PostgresProjectRepo:
    def __init__(self, session: Session) -> None:
        self.session = session
        
    def add(self, project: Project) -> None:
        modelo = ProjectModel(
            id = project.id,
            name = project.name
        )
        self.session.add(modelo)
        self.session.commit()
    
    def get(self, project_id: str) -> Project:
        modelo = self.session.get(ProjectModel, project_id)
        
        if modelo is None:
            raise NotFoundError('Proyecto no encontrado')
        
        return Project(id=modelo.id, name=modelo.name)
    
    def list(self) -> list[Project]:
        modelos = self.session.execute(select(ProjectModel)).scalars().all # asi obtengo una lista escalar
        
        return [Project(id=modelo.id, name=modelo.name) for modelo in modelos] # aqui hago la lista de proyectos
        
        """ Es lo mismo que hacer un for normal como sigue: """
        # for modelo in modelos:
        #     resulado.append(Project(id=modelo.id, name=modelo.name))
        
    def _strategy_from_type(task_type: str):
        if task_type == 'bug':
            return BugPriority
        if task_type == 'feature':
            return FeaturePriority
        if task_type == 'chore':
            return ChorePriority
        
        return ValueError('task_type invalido al construir objeto del dominio desde repositorio')
        
        
# =========== TASK =============       
class PostgresTaskRepo:
    def __init__(self, session: Session) -> None:
        self.session = session
        
    def add(self, task: Task) -> None:
        # El tipo de tarea necesita persistencia: inferir de la clase estartegia (nombre)
        
        strategy_name = type(task.strategy).__name__.lower()
        
        if 'bug' in strategy_name:
            task_type = 'bug'
        elif 'feature' in strategy_name:
            task_type = 'feature'
        elif 'chore' in strategy_name:
            task_type = 'chore'
        else:
            raise ValueError('task_type invalido al persistir')
            
        self.session.add(
            TaskModel(
                id = task.id,
                project_id = task.project_id,
                title = task.title,
                status = task.status,
                due_date = task.due_date,
                task_type = task_type
                
            )
        )
        self.session.commit
    
    def get(self, project_id: str) -> Project:
        modelo = self.session.get(TaskModel, task_id)
        
        if modelo is None:
            raise NotFoundError('Tarea no encontrada')
        
        strategy = _strategy_from_type(modelo.task_type)
        
        dominio = Task(
            id= modelo.id,
            project_id= modelo.project_id,
            title= modelo.title,
            due_date= modelo.due_date,
            strategy= strategy
        )
        
        if modelo.status == TaskStatus.DOING.value:
            dominio.transition_to(TaskStatus.DOING)
        elif modelo.status == TaskStatus.DONE.value:
            dominio.transition_to(TaskStatus.DONE)
    
    def delete(self, task_id: str) -> None:
        modelo = self.session.get(TaskModel, task_id)
        
        if modelo is None:
            raise NotFoundError('Tarea no encontrada')
        
        self.session.delete(modelo)
        self.session.commit
    
    def list_by_projects(self, project_id: str) -> list[Task]:
        modelo = self.session.execute(
            select(TaskModel).where(TaskModel.project_id == project_id)
        ).scallars.all()
        
        tasks: list[Task]
        
        for task in tasks:
            dominio = Task(
                id= modelo.id,
                project_id= modelo.project_id,
                title= modelo.title,
                due_date= modelo.due_date,
                strategy= strategy
            )
            
            if modelo.status == TaskStatus.DOING.value:
                dominio.transition_to(TaskStatus.DOING)
            elif modelo.status == TaskStatus.DONE.value:
                dominio.transition_to(TaskStatus.DONE)

        tasks.append(dominio)
        
    return tasks