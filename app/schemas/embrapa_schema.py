from enum import Enum

from fastapi import Query

ANO_MIN = 1970
ANO_MAX = 2023
ANO_MAX_IMP_EXP = 2024

ano_query = Query(
    default=2023,
    ge=ANO_MIN,
    le=ANO_MAX,
    description=f"Ano entre {ANO_MIN} e {ANO_MAX}",
)

ano_query_imp_exp = Query(
    default=2024,
    ge=ANO_MIN,
    le=ANO_MAX_IMP_EXP,
    description=f"Ano entre {ANO_MIN} e {ANO_MAX_IMP_EXP}",
)


class SubAbaProcessamentoSchema(str, Enum):
    SUCO = "viniferas"
    VINHO = "americanas_hibridas"
    UVA_MESA = "uvas_de_mesa"
    PASSAS = "sem_classificacao"


class SubAbaImportacaoSchema(str, Enum):
    VINHOS_DE_MESA = "vinhos_de_mesa"
    ESPUMANTES = "espumantes"
    UVAS_FRESCAS = "uvas_frescas"
    UVAS_PASSAS = "uvas_passas"
    SUCO_DE_UVA = "suco_de_uva"


class SubAbaExportacaoSchema(str, Enum):
    VINHOS_DE_MESA = "vinhos_de_mesa"
    ESPUMANTES = "espumantes"
    UVAS_FRESCAS = "uvas_frescas"
    SUCO_DE_UVA = "suco_de_uva"
