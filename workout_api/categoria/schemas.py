from typing_extensions import Annotated
from pydantic import Field, UUID4

from workout_api.contrib.schemas import BaseSchemas


class Categoria(BaseSchemas):
    nome: Annotated[str, Field(description="nome da categoria", example="Scale", max_length=10)]


class CategoriaOut(Categoria):
    id: Annotated[UUID4, Field(description="identificador da categoria")]