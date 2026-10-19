import pandas as pd
from sqlalchemy import text
from app.database import engine
from app.models import Base

DATA = "data/ml-1m"

users = pd.read_csv(f"{DATA}/users.dat", sep="::", engine="python",
                    names=["id", "gender", "age", "occupation", "zip"])
movies = pd.read_csv(f"{DATA}/movies.dat", sep="::", engine="python",
                     names=["id", "title", "genres"], encoding="latin-1")
ratings = pd.read_csv(f"{DATA}/ratings.dat", sep="::", engine="python",
                      names=["user_id", "movie_id", "rating", "ts"],
                      usecols=["user_id", "movie_id", "rating"])

# MovieLens không có email/password nên tạo giá trị giả cho các user mẫu này
users_df = pd.DataFrame({
    "id": users["id"],
    "email": "user" + users["id"].astype(str) + "@movielens.local",
    "password_hash": "!",
})

# Tạo lại 3 bảng theo model mới
Base.metadata.create_all(engine)

users_df.to_sql("users", engine, if_exists="append", index=False, chunksize=5000, method="multi")
movies[["id", "title", "genres"]].to_sql("movies", engine, if_exists="append", index=False, chunksize=5000, method="multi")
ratings.to_sql("ratings", engine, if_exists="append", index=False, chunksize=10000, method="multi")

# Đặt lại bộ đếm id để POST /users, POST /movies sau này không bị trùng id
with engine.begin() as conn:
    for t in ("users", "movies"):
        conn.execute(text(
            f"SELECT setval(pg_get_serial_sequence('{t}', 'id'), (SELECT MAX(id) FROM {t}))"
        ))

print("Xong:", len(users_df), "users,", len(movies), "movies,", len(ratings), "ratings")