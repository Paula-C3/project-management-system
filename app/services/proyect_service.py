from app.domain.entities import Project
from app.repositories.base import ProjectRepository

# ============== PROYECT ===================
class ProjectService:
    def __init__(self, repo: ProjectRepository) -> None:
        self.repo  = repo
        
    def create(self, name:str) -> Project:       # FUNCION: crear proyecto
        project = Project(name=name)
        self.repo.add(project)
        return project
    
    def get(self, project_id:str) -> Project:     # FUNCION: obtener un proyecto. Ya no valido (valide en repo)
        return self.repo.get(project_id)
    
    def list(self) -> list[Project]:    # FUNCION : listar proyectos
        return self.repo.list()
    
  