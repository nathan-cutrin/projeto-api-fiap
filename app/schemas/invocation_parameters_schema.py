from enum import Enum

from pydantic import BaseModel, Field

ano_field_until_2023 = Field(
    ...,
    ge=1970,
    le=2023,
    description="Dados disponíveis entre os anos 1970 e 2023",
)

ano_field_until_2024 = Field(
    ...,
    ge=1970,
    le=2024,
    description="Dados disponíveis entre os anos 1970 e 2024",
)


class ProducaoPathParams(BaseModel):
    ano: int = ano_field_until_2023


class ComercializacaoPathParams(BaseModel):
    ano: int = ano_field_until_2023


class SubAbaProcessamentoSchema(str, Enum):
    UVAS_VINIFERAS = "viniferas"
    VINHO = "americanas_hibridas"
    UVA_MESA = "uvas_de_mesa"
    PASSAS = "sem_classificacao"


class ProcessamentoPathParams(BaseModel):
    sub_aba: SubAbaProcessamentoSchema = Field(
        ..., description="Sub-abas de processamento"
    )
    ano: int = ano_field_until_2023


class SubAbaImportacaoSchema(str, Enum):
    VINHOS_DE_MESA = "vinhos_de_mesa"
    ESPUMANTES = "espumantes"
    UVAS_FRESCAS = "uvas_frescas"
    UVAS_PASSAS = "uvas_passas"
    SUCO_DE_UVA = "suco_de_uva"


class ImportacaoPathParams(BaseModel):
    sub_aba: SubAbaImportacaoSchema = Field(
        ..., description="Sub-abas de importação"
    )
    ano: int = ano_field_until_2024


class SubAbaExportacaoSchema(str, Enum):
    VINHOS_DE_MESA = "vinhos_de_mesa"
    ESPUMANTES = "espumantes"
    UVAS_FRESCAS = "uvas_frescas"
    SUCO_DE_UVA = "suco_de_uva"


class ExportacaoPathParams(BaseModel):
    sub_aba: SubAbaExportacaoSchema = Field(
        ..., description="Sub-abas de exportação"
    )
    ano: int = ano_field_until_2024
