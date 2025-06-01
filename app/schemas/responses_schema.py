from pydantic import BaseModel, Field


class ProdutoSchema(BaseModel):
    tipo_produto: str = Field(..., description="Tipo da uva")
    produto: str = Field(..., description="Uva cultivada")
    quantidade_litros: int = Field(..., description="Quantidade em kg")


class ProducaoResponseSchema(BaseModel):
    data: list[ProdutoSchema] = Field(
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


class ComercializacaoResponseSchema(BaseModel):
    data: list[ProdutoSchema] = Field(
        ..., description="Lista de dados de processamento"
    )


class ImportacaoExportacaoSchema(BaseModel):
    pais: str = Field(..., description="País")
    quantidade_kg: int = Field(..., description="Quantidade em kg")
    valor_dolar: int = Field(..., description="Valor em US$")


class ImportacaoResponseSchema(BaseModel):
    data: list[ImportacaoExportacaoSchema] = Field(
        ..., description="Lista de dados de importação"
    )


class ExportacaoResponseSchema(BaseModel):
    data: list[ImportacaoExportacaoSchema] = Field(
        ..., description="Lista de dados de exportacao"
    )
