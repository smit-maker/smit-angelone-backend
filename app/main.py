from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Database
from .database import engine, Base

# Routers
from app.router.users import router as usersRouter

# Models
from .model import users

def create_app():
    Base.metadata.create_all(bind=engine)
    # Base.metadata.drop_all(bind=engine)

    app = FastAPI(debug=True)
    # app.mount('/static', StaticFiles(directory='static', html=True), name='static')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    
    # # Set up CORS middleware
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["http://localhost:5173"],  # Add the origin of your React app
    #     allow_credentials=True,
    #     allow_methods=["GET"],
    #     allow_headers=["*"],
    # )

    app.include_router(usersRouter)

    return app

app = create_app()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/{name}")
def get_name(name: str):
    return {"Name": name}

    