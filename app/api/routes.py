from fastapi import APIRouter, Depends, HTTPException

""" Como es la capa de aplicación, aqui uso todas las capas externas! """

from app.infra.repo_factory import build_repo_factory
from app.domain.exceptions import DomainError, NotFoundError, InvalidStatusTransition, ValidationError
from app.repositories.memory import InMemoryProjectRepo, InMemoryTaskRepo
from app.services.proyect_service import ProjectService
from app.services.task_service import TaskService
from app.schemas.dto import ProjectCreate, ProjectOut, TaskCreate, TaskOut, TaskUpdate


router = APIRouter()    # dirige el trafico a los distintos urls (o End Points) / puntos de conexion

factory = build_repo_factory()
project_repo = InMemoryProjectRepo()    # aqui instancio los repo
task_repo = InMemoryTaskRepo()

def get_project_service() -> ProjectService:
    return ProjectService(project_repo)

def get_task_service() -> TaskService:
    return TaskService(task_repo)

def to_http(e:Exception) -> HTTPException:
    if isinstance(e, NotFoundError):
        return HTTPException(status_code = 404, details=str(e))
    
    if isinstance(e, InvalidStatusTransition, ValidationError, ValueError):
        return HTTPException(status_code = 400, details=str(e))
    
    if isinstance(e, DomainError):
        return HTTPException(status_code = 500, details='Internal server error')
    
    
@router.post('/projects', response_model = ProjectOut, status_code = 201)
def create_project(body: ProjectCreate, service:ProjectService = Depends(get_project_service)):
    try:
        project = service.create(body.name)
        return ProjectOut(id=project.id, name=project.name)
    except Exception as e:
        raise to_http(e)


# TO-DO: GET /projects
@router.get('/projects', response_model= list[ProjectOut], status_code =200)
def get_projects(service: ProjectService = Depends(get_project_service)):
    try:
        projects = service.list()
        return [ProjectOut(id = p.id, name = p.name) for p in projects]
    except Exception as e:
        raise to_http(e)
    
    
# TO-DO: GET /projects/{project_id}
# @router.get('/projects/{project_id}', response_model=ProjectOut)
@router.get('/projects/{project_id}', response_model= ProjectOut)
def get_project(project_id: str, service: ProjectService = Depends(get_project_service)):
    try:
        project = service.get(project_id)
        return ProjectOut(id = project.id, name = project.name)
    except Exception as e:
        raise to_http(e)


# TO-DO POST /projects/{project_id}/tasks
@router.post('/projects/{project_id}/tasks',response_model = TaskOut ,status_code = 201)
def create_task(project_id:str, body: TaskCreate, service: TaskService = Depends(get_task_service)):
    try:
        task = service.create_task(
            project_id= project_id,
            title= body.title,
            task_type= body.task_type,
            due_date=body.due_date,
        )
        return TaskOut(
            id= task.id,
            project_id= task.project_id,
            title= task.title,
            status= task.status,
            priority_score= task.priority_score,
            due_date = task.due_date
        )
    except Exception as e:
        raise to_http(e)

# TO-DO GET /projects/{project_id}/tasks
@router.get('/projects/{project_id}/tasks',response_model = list[TaskOut] ,status_code = 201)
def get_task(project_id:str, service: TaskService = Depends(get_task_service)):
    try:
        tasks = service.list_tasks(project_id)
        return [
            TaskOut(
                id= t.id,
                project_id= t.project_id,
                title= t.title,
                status= t.status,
                priority_score= t.priority_score,
                due_date = t.due_date
            ) for t in tasks
        ]
    except Exception as e:
        raise to_http(e)


# TO-DO DELETE /tasks/{task_id}
@router.delete('/projects/{task_id}',response_model = TaskService ,status_code = 201)
def get_task(task_id:str, service: TaskService = Depends(get_task_service)):
    try:
        service.delete_task(task_id)
        return None
    except Exception as e:
        raise to_http(e)