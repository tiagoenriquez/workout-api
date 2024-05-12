from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, status, Body, HTTPException
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from fastapi_pagination import LimitOffsetPage, paginate


from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.schemas import Atleta as AtletaIn, AtletaAllOut, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categoria.schemas import CategoriaOut
from workout_api.categoria.model import CategoriaModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoOut
from workout_api.centro_treinamento.model import CentroTreinamentoModel

router = APIRouter()

@router.post(
    path="/",
    summary="Cria um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)) -> AtletaOut:
    categoria: CategoriaOut = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))
    ).scalars().first()
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))
    ).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A categoria do atleta não encontrada")
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O centro de treinamento do atleta não encontrado")
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude=["categoria", "centro_treinamento"]))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f"Já existe atleta cadastrado com CPF {atleta_in.cpf}")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao cadastrar dados do atleta")
    return atleta_out

@router.get(
    path="/",
    summary="Consulta todos atletas",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaAllOut]
)
async def all(db_session: DatabaseDependency) -> LimitOffsetPage[AtletaOut]:
    atletas: list[AtletaAllOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    for atleta in atletas:
        atleta.resumo = f"{atleta.nome} pratica {atleta.categoria.nome} no centro de treinamento {atleta.centro_treinamento.nome}."
        AtletaAllOut.model_validate(atleta)
    return paginate(atletas)

@router.get(
    path="/{id}",
    summary="Consulta um atleta por id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def find(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(
        select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    return atleta

@router.get(
    path="/busca-por-nome/{nome}",
    summary="Consulta um atleta por nome",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def findByNome(nome: str, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(
        select(AtletaModel).filter_by(nome=nome))
    ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado com o nome pesquisado")
    return atleta

@router.get(
    path="/busca-por-cpf/{cpf}",
    summary="Consulta um atleta por CPF",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def findByCpf(cpf: str, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(
        select(AtletaModel).filter_by(cpf=cpf))
    ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado com o CPF pesquisado")
    return atleta

@router.patch(
    path="/{id}",
    summary="Atualiza um atleta",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def update(id: UUID4, db_session: DatabaseDependency, atleta_upd: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(
        select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    atleta_update = atleta_upd.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta

@router.delete(
    path="/{id}",
    summary="Exclui um atleta",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(
        select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")
    await db_session.delete(atleta)
    await db_session.commit()
