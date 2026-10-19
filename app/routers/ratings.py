from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas import RatingCreate, RatingResponse, RatingUpdate
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Rating, User, Movie

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)

@router.get("", response_model=list[RatingResponse])
def get_ratings(
    skip: int = 0,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return db.query(Rating).order_by(Rating.id).offset(skip).limit(limit).all()

@router.post("", response_model= RatingResponse)
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):

    existing_user = db.get(User, rating.user_id)

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_movie = db.get(Movie, rating.movie_id)

    if not existing_movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    existing_rating = db.query(Rating).filter(
        Rating.user_id == rating.user_id,
        Rating.movie_id == rating.movie_id
    ).first()

    if existing_rating:

        existing_rating.rating = rating.rating

        db.commit()     

        return existing_rating

    else:
        
        db_rating = Rating(user_id = rating.user_id, movie_id = rating.movie_id, rating = rating.rating)

        db.add(db_rating)

        db.commit()

        return db_rating

@router.put("/{id}", response_model= RatingResponse)
def update_rating_by_id(id: int, rating: RatingUpdate, db: Session = Depends(get_db)):

    existing_rating = db.get(Rating, id)

    if existing_rating:

        existing_rating.rating = rating.rating

        db.commit()

        return existing_rating

    raise HTTPException(
        status_code=404,
        detail="Not found rating"
    )

@router.delete("/{id}", status_code=204)
def delete_rating_by_id(id: int, db: Session = Depends(get_db)):

    existing_rating = db.get(Rating, id)

    if existing_rating:

        db.delete(existing_rating)

        db.commit()

        return 

    raise HTTPException(
        status_code= 404,
        detail="Rating not found"
    )