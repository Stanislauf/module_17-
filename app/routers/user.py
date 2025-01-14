from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated, List
from app.models import User as UserModel  # Импортируйте модель SQLAlchemy
from app.schemas import CreateUser, UpdateUser, User  # Убедитесь, что User импортирован из схем
from sqlalchemy import insert, select, update, delete
from slugify import slugify
import logging
logger = logging.getLogger("myapp")

router = APIRouter()

@router.get("/", response_model=List[User])
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(UserModel)).scalars().all()
    return users

@router.get("/{user_id}", response_model=User)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(UserModel).where(UserModel.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    logger.info("Creating user: %s", user.username)

    new_user = UserModel(**user.dict())
    new_user.slug = slugify(new_user.username)

    db.execute(
        insert(UserModel).values(username=new_user.username, firstname=new_user.firstname, lastname=new_user.lastname,
                                 age=new_user.age, slug=new_user.slug))
    db.commit()

    logger.info("User created with username: %s", new_user.username)

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

"""@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    new_user = UserModel(**user.dict())
    new_user.slug = slugify(new_user.username)
    db.execute(insert(UserModel).values(username=new_user.username, firstname=new_user.firstname, lastname=new_user.lastname, age=new_user.age, slug=new_user.slug))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}"""

@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    db_user = db.execute(select(UserModel).where(UserModel.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(update(UserModel).where(UserModel.id == user_id).values(**user.dict()))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    db_user = db.execute(select(UserModel).where(UserModel.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(UserModel).where(UserModel.id == user_id))
    db.commit()

"""from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated, List
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter()

@router.get("/", response_model=List[User])
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users

@router.get("/{user_id}", response_model=User)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    new_user = User(**user.dict())
    new_user.slug = slugify(new_user.username)
    db.execute(insert(User).values(new_user))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(update(User).where(User.id == user_id).values(**user.dict()))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_204_NO_CONTENT}"""