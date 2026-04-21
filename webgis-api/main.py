from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import get_pool, close_pool
from routers import fasilitas
from fastapi.middleware.cors import CORSMiddleware
from routers import user

@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    print("DB Connected")
    yield
    await close_pool()
    print("DB Disconnected")

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # boleh semua (untuk praktikum)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fasilitas.router)
app.include_router(user.router)