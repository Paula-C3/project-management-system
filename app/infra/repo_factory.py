from __future__ import annotations

import os
from abc import ABC, abstractmethod

from app.repositories.memory import InMemoryProjectRepo, InMemoryTaskRepo
from app.repositories.postgres import PostgresProjectRepo, PostgresTaskRepo

from app.infra.db import SessionLocal

class RepoFactory(ABC):
    @abstractmethod
    def create_project_repo(self):
        raise NotImplementedError()
    
    @abstractmethod
    def create_task_repo(self):
        raise NotImplementedError()
    
    
class MemoryRepoFactory(RepoFactory):
    def __init__(self):
        super().__init__()
        self._project_repo = InMemoryProjectRepo()
        self._task_repo = InMemoryTaskRepo()
        
    def create_project_repo(self):
        return self._project_repo
    
    def create_task_repo(self):
        return self._task_repo
    
    
class PostgresRepoFactory(RepoFactory):
    def __init__(self):
        super().__init__()
        self._session = SessionLocal()
        
        
    def create_project_repo(self):
        return PostgresProjectRepo(self._session)
    
    def create_task_repo(self):
        return PostgresTaskRepo(self._session)
    
def build_Repo_factory() -> RepoFactory:
    backend = os.getenv('REPO_BACKEND', 'memory').lower()
    
    if backend == 'postgres':
        return PostgresRepoFactory

    return MemoryRepoFactory    