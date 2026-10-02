from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.models import supervision
from app.routes import project, quantity, cost
from app.routes import project, quantity, cost, prediction
from app.routes import project, quantity, cost, prediction, risk
from app.routes import project, quantity, cost, prediction, risk, supervision
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Construction Planning System")
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project.router)
app.include_router(quantity.router)
app.include_router(cost.router)
app.include_router(prediction.router)
app.include_router(risk.router)
app.include_router(supervision.router)

@app.get("/")
def root():
    return {"message": "Smart Construction API is running"}