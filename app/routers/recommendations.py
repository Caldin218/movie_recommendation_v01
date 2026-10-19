from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PopularMovieResponse
from app.services.recommender import get_popular_movies

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)

@router.get("/popular", response_model=list[PopularMovieResponse])
def popular_movies(
    top_n: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    rows = get_popular_movies(db, top_n=top_n)
    return [
        PopularMovieResponse(
            id=r.id,
            title=r.title,
            avg_rating=round(float(r.avg_rating), 2),
            num_ratings=r.num_ratings,
        )
        for r in rows
    ]