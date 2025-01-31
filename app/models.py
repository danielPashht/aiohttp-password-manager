from pydantic import BaseModel, PositiveInt, Field


class RegisterModel(BaseModel):
    username: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=6)


class LoginModel(BaseModel):
    username: str
    password: str


class PasswordModel(BaseModel):
    length: PositiveInt
    label: str

