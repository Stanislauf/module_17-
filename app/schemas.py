from pydantic import BaseModel

# Схемы для пользователя

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

# Схемы для задачи
class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int


class User(UserBase):
    id: int

    class Config:
        orm_mode = True