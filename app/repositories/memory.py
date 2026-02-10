from __future__ import annotations      # en el futuro delega el typado, permite que se levanten mas rapido los servicios
from app.domain.entities import Project, Task
from app.domain.exceptions import NotFoundError

# ============= PROYECTOS ==================    
class InMemoryProjectRepo:
    def __init__(self) -> None:         # constructor
        self._data: dict[str, Project] = {}

    def add(self, project: Project) -> None:        # FUNCION:  agregar proyecto
        self._data[project.id] = project
        
    def get(self, project_id: str) -> Project:      # FUNCION: obtener un proyecto
        if project_id not in self._data:
            raise NotFoundError('Proyecto no encontrado')
        
        return self._data[project_id]
    
    def list(self) -> list[Project]:        # FUNCION: get todos los proyectos
        return list(self._data.values)  # para obtener valores y no claves
  
  
# ============= TAREAS ==================    
class InMemoryTaskRepo:
    def __init__(self) -> None:         # constructor
        self._data: dict[str, Task] = {}
        
    def add(self, task: Task) -> None:        # FUNCION:  agregar tarea
        self._data[task.id] = task
        
    def get(self, task_id: str) -> Task:      # FUNCION: obtener una tarea
        if task_id not in self._data:
            raise NotFoundError('Tarea no encontrada')
        
        return self._data[task_id]
    
    def delete(self, task_id: str) -> None:
        if task_id not in self._data:
            raise NotFoundError('Tarea no encontrada')
        
        del self._data[task_id]     # borro el espacio en memoria de la llave y valor
        
    def list_by_project(self, project_id: str) -> list[Task]:
        return [ task for task in self._data.values() if task.project_id == project_id]  
            # Para cada tarea (for) hacer append a la lista ( [] ) si se cumple la condicion del if
        
       