from pydantic import BaseModel

class FasilitasCreate(BaseModel):
    nama: str
    jenis: str
    longitude: float
    latitude: float

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str