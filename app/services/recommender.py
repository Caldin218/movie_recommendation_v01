from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Movie, Rating


def get_popular_movies(db: Session, top_n: int = 10, min_ratings: int = 50):
    """Phim phổ biến: điểm trung bình cao, và có đủ số lượt chấm để đáng tin."""
    rows = (
        db.query(
            Movie.id,
            Movie.title,
            func.avg(Rating.rating).label("avg_rating"),
            func.count(Rating.id).label("num_ratings"),
        )
        .join(Rating, Rating.movie_id == Movie.id)
        .group_by(Movie.id, Movie.title)
        .having(func.count(Rating.id) >= min_ratings)
        .order_by(func.avg(Rating.rating).desc())
        .limit(top_n)
        .all()
    )
    return rows