from fastapi import APIRouter, Depends, HTTPException

""" Como es la capa de aplicación, aqui uso todas las capas externas! """

from app.domain.exceptions import DomainError, NotFoundError, InvalidStatusTransition, ValidationError
from app.repositories.memory import InMemoryProjectRepo, InMemoryTaskRepo
from app.services.proyect_service import ProjectService
from app.services.task_service import TaskService
from app.schemas.dto import ProjectCreate, ProjectOut, TaskCreate, TaskOut, TaskUpdate


router = APIRouter()    # dirige el trafico a los distintos urls (o End Points) / puntos de conexion

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
# TO-DO: GET /projects/{project_id}
# @router.get('/projects/{project_id}', response_model=ProjectOut)
# TO-DO POST /projects/{project_id}/tasks
# TO-DO GET /projects/{project_id}/tasks
# TO-DO DELETE /tasks/{task_id}