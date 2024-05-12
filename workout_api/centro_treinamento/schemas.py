from typing_extensions import Annotated
from pydantic import Field, UUID4

from workout_api.contrib.schemas import BaseSchemas


class CentroTreinamento(BaseSchemas):
    nome: Annotated[str, Field(description="nome do centro de treinamento", example="CT King", max_length=20)]
    endereco: Annotated[str, Field(description="endereço do centro de treinamento", example="Rua das Botas", max_length=60)]
    proprietario: Annotated[str, Field(description="nome do proprietário do centro de treinamento", example="José", max_length=30)]


class CentroTreinamentoAtleta(CentroTreinamento):
    nome: Annotated[str, Field(description="nome do centro de treinamento", example="CT King", max_length=20)]


class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description="identificador do centro de de treinamento")]