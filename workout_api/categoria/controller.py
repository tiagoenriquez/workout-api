from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException
from sqlalchemy.future import select
from pydantic import UUID4

from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.categoria.schemas import Categoria as CategoriaIn, CategoriaOut
from workout_api.categoria.model import CategoriaModel

router = APIRouter()

@router.post(
    path="/",
    summary="Cria uma nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut
)
async def post(
    db_session: DatabaseDependency,
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out

@router.get(
    path="/",
    summary="Consulta todas as categorias",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut]
)
async def all(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias

@router.get(
    path="/{id}",
    summary="Consulta uma categoria por id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut
)
async def find(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    return categoria