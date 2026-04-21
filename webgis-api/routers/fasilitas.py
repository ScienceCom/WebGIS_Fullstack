from fastapi import APIRouter, HTTPException
from database import get_pool
from models import FasilitasCreate
from models import UserCreate
from models import UserLogin
import json

router = APIRouter(prefix="/api/fasilitas")

@router.get("/")
async def get_all():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
        SELECT id, nama, jenis,
        ST_AsGeoJSON(geom) as geom
        FROM sukamenanti
        """)
        return [dict(row) for row in rows]


@router.get("/geojson")
async def geojson():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
        SELECT id, nama, jenis,
        ST_AsGeoJSON(geom) as geom
        FROM sukamenanti
        """)

        features = []
        for row in rows:
            features.append({
                "type": "Feature",
                "geometry": json.loads(row["geom"]),
                "properties": {
                    "id": row["id"],
                    "nama": row["nama"],
                    "jenis": row["jenis"]
                }
            })

        return {"type": "FeatureCollection", "features": features}


@router.get("/nearby")
async def nearby(lat: float, lon: float, radius: int = 500):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
        SELECT id, nama, jenis,
        ROUND(ST_Distance(
            geom::geography,
            ST_Point($1,$2)::geography
        )) as jarak
        FROM sukamenanti
        WHERE ST_DWithin(
            geom::geography,
            ST_Point($1,$2)::geography,
            $3
        )
        ORDER BY jarak
        """, lon, lat, radius)

        return [dict(row) for row in rows]


@router.get("/{id}")
async def get_by_id(id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
        SELECT id, nama, jenis,
        ST_X(geom) as longitude,
        ST_Y(geom) as latitude
        FROM sukamenanti
        WHERE id = $1
        """, id)

        if not row:
            raise HTTPException(404, "Data tidak ditemukan")

        return dict(row)


@router.post("/")
async def create(data: FasilitasCreate):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
        INSERT INTO sukamenanti (nama, jenis, geom)
        VALUES ($1, $2,
        ST_SetSRID(ST_Point($3,$4), 4326))
        RETURNING id, nama, jenis
        """, data.nama, data.jenis,
           data.longitude, data.latitude)

        return dict(row)

@router.put("/{id}")
async def update(id: int, data: FasilitasCreate):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
        UPDATE sukamenanti
        SET nama = $1,
            jenis = $2,
            geom = ST_SetSRID(ST_Point($3,$4), 4326)
        WHERE id = $5
        RETURNING id, nama, jenis
        """, data.nama, data.jenis,
           data.longitude, data.latitude, id)

        if not row:
            raise HTTPException(404, "Data tidak ditemukan")

        return dict(row)


@router.delete("/{id}")
async def delete(id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute("""
        DELETE FROM sukamenanti
        WHERE id = $1
        """, id)

        return {"msg": "Data berhasil dihapus"}