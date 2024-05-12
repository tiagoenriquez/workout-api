from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchemas, OutMixing
from workout_api.categoria.schemas import Categoria
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta


class Atleta(BaseSchemas):
    nome: Annotated[str, Field(description="nome do atleta", example="João", max_length=500)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="01234567890", max_length=11)]
    idade: Annotated[int, Field(description="idade do atleta", example=34)]
    peso: Annotated[PositiveFloat, Field(description="peso do atleta", example=80.5)]
    altura: Annotated[PositiveFloat, Field(description="altura do atleta", example=1.8)]
    sexo: Annotated[str, Field(description="sexo do atleta", example="m", max_length=1)]
    categoria: Annotated[Categoria, Field(description="categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="centro de treinamento do atleta")]


class AtletaOut(Atleta, OutMixing):
    pass


class AtletaAllOut(AtletaOut):
    resumo: Annotated[str, Field(description="texto informando nome do atleta, categoria e centro de treinamento")]


class AtletaUpdate(BaseSchemas):
    nome: Annotated[Optional[str], Field(description="nome do atleta", example="João", max_length=500)]
    idade: Annotated[Optional[int], Field(description="idade do atleta", example=34)]