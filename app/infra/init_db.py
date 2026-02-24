from app.infra.db import engine, Base
from app.infra import models

def init_db() -> None:
    Base.metadata.create_all(bind=engine)