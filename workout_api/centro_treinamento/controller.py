from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException
from sqlalchemy.future import select
from pydantic import UUID4

from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.centro_treinamento.schemas import CentroTreinamento as CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.model import CentroTreinamentoModel

router = APIRouter()

@router.post(
    path="/",
    summary="Cria um novo centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    return centro_treinamento_out

@router.get(
    path="/",
    summary="Consulta todos centros de treinamento",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut]
)
async def all(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return centros_treinamento

@router.get(
    path="/{id}",
    summary="Consulta um centro de treinamento por id",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut
)
async def find(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro de treinamento não encontrado")
    return centro_treinamento