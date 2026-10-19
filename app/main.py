from fastapi import FastAPI
from app.routers import movies, users, ratings, recommendations

app = FastAPI(title="Movie Recommendation API")

app.include_router(movies.router)

app.include_router(users.router)

app.include_router(ratings.router)

app.include_router(recommendations.router)

@app.get("/")
def root():
    return {"message":"Chào mừng đến với hệ thống gợi ý phim!"}