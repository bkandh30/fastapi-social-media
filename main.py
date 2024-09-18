from fastapi import FastAPI
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Social Media App",
    description= "Social Media App Backend",
    version="0.1"
)
