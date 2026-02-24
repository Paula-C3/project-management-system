from fastapi import FastAPI
from app.api.routes import router
from app.infra.init_db import init_db

app = FastAPI(title='ProjectManagement API', version='1.0.0')

@app.on_event('startup')
def on_stratup():
    init_db()

app.include_router(router)