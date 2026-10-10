from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.database import get_db  
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("", response_model= list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{id}", response_model= UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):

    existing_user = db.get(User,id)

    if existing_user:

        for r in existing_user.ratings:

            print("các rating của user này:", r.rating)

        return existing_user

    raise HTTPException(status_code=404,  detail="User not found")

@router.post("", response_model= UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_email:

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    db_user = User(email = user.email, password_hash = user.password_hash)

    try: 

        db.add(db_user)

        db.commit()

        db.refresh(db_user)

    except IntegrityError as e:

        db.rollback()

        print("Orgin Error: ", e.orig)

        raise HTTPException(
            status_code=409,
            detail="Database Integrity Constraint violated"
        )

    return db_user

@router.put("/{id}", response_model= UserResponse)
def update_user_by_id(id:int, user: UserCreate, db: Session= Depends(get_db)):

    existing_user = db.get(User, id)

    if existing_user:

        check_email_dup = db.query(User).filter((User.email == user.email) & (User.id != id)).first()

        if check_email_dup:
            raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

        existing_user.email = user.email

        existing_user.password_hash = user.password_hash

        try:

            db.commit()

        except IntegrityError as e:

            db.rollback()
            print("Origin Error:", e.orig)

            raise HTTPException(
                status_code=409,
                detail="Database integrity constraint violated"
            )

        return existing_user

    raise HTTPException(
        status_code= 404,
        detail="User not found"
    )

@router.delete("/{id}", status_code= 204)
def delete_user_by_id(id: int, db: Session = Depends(get_db)):

    existing_user = db.get(User, id)

    if existing_user:
        db.delete(existing_user)

        db.commit()

        return

    raise HTTPException(status_code=404, detail="User not found")