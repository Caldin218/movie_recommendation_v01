from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Movie
from app.schemas import MovieCreate, MovieResponse

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("", response_model=list[MovieResponse])
def get_movies(
    skip: int = 0,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return db.query(Movie).order_by(Movie.id).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=MovieResponse)
def get_movie_by_id(id: int, db: Session = Depends(get_db)):

    existing_movie = db.get(Movie, id)

    if existing_movie:
        return existing_movie

    raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )

@router.post("", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):

    db_movie = Movie(title=movie.title)

    db.add(db_movie)
    db.commit()

    return db_movie

@router.put("/{id}", response_model=MovieResponse)
def update_movie_by_id(
    id: int,
    movie: MovieCreate,
    db: Session = Depends(get_db)
):

    existing_movie = db.get(Movie, id)

    if existing_movie:

        existing_movie.title = movie.title

        db.commit()

        return existing_movie

    raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )

@router.delete("/{id}", status_code=204)
def delete_movie_by_id(
    id: int,
    db: Session = Depends(get_db)
):

    existing_movie = db.get(Movie, id)

    if existing_movie:

        db.delete(existing_movie)
        db.commit()

        return

    raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )
