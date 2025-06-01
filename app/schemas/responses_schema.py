from pydantic import BaseModel, Field


class ProducaoSchema(BaseModel):
    tipo_produto: str = Field(..., description="Tipo da uva")
    produto: str = Field(..., description="Uva cultivada")
    quantidade_litros: int = Field(..., description="Quantidade em kg")


class ProducaoResponseSchema(BaseModel):
    data: list[ProducaoSchema] = Field(
        ..., description="Lista de dados de processamento"
    )


class ProcessamentoSchema(BaseModel):
    tipo_uva: str = Field(..., description="Tipo da uva")
    cultivo: str = Field(..., description="Uva cultivada")
    quantidade_kg: str = Field(..., description="Quantidade em kg")


class ProcessamentoResponseSchema(BaseModel):
    data: list[ProcessamentoSchema] = Field(
        ..., description="Lista de dados de processamento"
    )
