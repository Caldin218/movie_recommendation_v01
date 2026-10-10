from pydantic import BaseModel, Field, ConfigDict
#=============================  SCHEMA MOVIE  =======================================

class MovieCreate(BaseModel):
    title: str

class MovieResponse(BaseModel):
    id: int
    title: str

    model_config= ConfigDict(from_attributes=True) #Cho phép TRUE: Pydantic nhận/tiếp xúc attributes từ Objects của SqlAlchemy 
#=============================  SCHEMA RATING  =======================================
class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int = Field(ge= 1, le= 5)

class RatingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int

    model_config = ConfigDict(from_attributes=True) #Cho phép TRUE: Pydantic lấy các attributes của Objects đầu vào 

class RatingUpdate(BaseModel):
    rating: int = Field(ge= 1, le= 5)
#=============================  SCHEMA USER  =======================================

class UserCreate(BaseModel):
    email : str
    password_hash : str

class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)
#===================================================================================