from fastapi import FastAPI
from app.routers import movies, users, ratings

app = FastAPI()

app.include_router(movies.router)

app.include_router(users.router)

app.include_router(ratings.router)