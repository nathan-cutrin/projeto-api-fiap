import pytest
from pydantic import ValidationError

from app.schemas.invocation_parameters_schema import (
    ComercializacaoPathParams,
    ExportacaoPathParams,
    ImportacaoPathParams,
    ProcessamentoPathParams,
    ProducaoPathParams,
    SubAbaExportacaoSchema,
    SubAbaImportacaoSchema,
    SubAbaProcessamentoSchema,
)

ANO_MIN = 1970
ANO_MAX_2023 = 2023
ANO_MAX_2024 = 2024


def test_producao_path_params_valid():
    params = ProducaoPathParams(ano=ANO_MAX_2023)
    assert params.ano == ANO_MAX_2023


def test_producao_path_params_invalid():
    with pytest.raises(ValidationError):
        ProducaoPathParams(ano=ANO_MIN - 1)
    with pytest.raises(ValidationError):
        ProducaoPathParams(ano=ANO_MAX_2024)


def test_comercializacao_path_params_valid():
    params = ComercializacaoPathParams(ano=ANO_MIN)
    assert params.ano == ANO_MIN


def test_comercializacao_path_params_invalid():
    with pytest.raises(ValidationError):
        ComercializacaoPathParams(ano=ANO_MIN - 10)
    with pytest.raises(ValidationError):
        ComercializacaoPathParams(ano=ANO_MAX_2024)


def test_processamento_path_params_valid():
    params = ProcessamentoPathParams(
        sub_aba=SubAbaProcessamentoSchema.SUCO, ano=ANO_MAX_2023
    )
    assert params.sub_aba == SubAbaProcessamentoSchema.SUCO
    assert params.ano == ANO_MAX_2023


def test_processamento_path_params_invalid_ano():
    with pytest.raises(ValidationError):
        ProcessamentoPathParams(
            sub_aba=SubAbaProcessamentoSchema.SUCO, ano=ANO_MIN - 10
        )


def test_processamento_path_params_invalid_subaba():
    with pytest.raises(ValidationError):
        ProcessamentoPathParams(sub_aba="invalido", ano=2020)


def test_importacao_path_params_valid():
    params = ImportacaoPathParams(
        sub_aba=SubAbaImportacaoSchema.ESPUMANTES, ano=ANO_MAX_2024
    )
    assert params.sub_aba == SubAbaImportacaoSchema.ESPUMANTES
    assert params.ano == ANO_MAX_2024


def test_importacao_path_params_invalid_ano():
    with pytest.raises(ValidationError):
        ImportacaoPathParams(
            sub_aba=SubAbaImportacaoSchema.ESPUMANTES, ano=ANO_MIN - 1
        )
    with pytest.raises(ValidationError):
        ImportacaoPathParams(
            sub_aba=SubAbaImportacaoSchema.ESPUMANTES, ano=ANO_MAX_2024 + 1
        )


def test_importacao_path_params_invalid_subaba():
    with pytest.raises(ValidationError):
        ImportacaoPathParams(sub_aba="invalido", ano=2020)


def test_exportacao_path_params_valid():
    params = ExportacaoPathParams(
        sub_aba=SubAbaExportacaoSchema.ESPUMANTES, ano=ANO_MAX_2024
    )
    assert params.sub_aba == SubAbaExportacaoSchema.ESPUMANTES
    assert params.ano == ANO_MAX_2024


def test_exportacao_path_params_invalid_ano():
    with pytest.raises(ValidationError):
        ExportacaoPathParams(
            sub_aba=SubAbaExportacaoSchema.ESPUMANTES, ano=ANO_MIN - 1
        )
    with pytest.raises(ValidationError):
        ExportacaoPathParams(
            sub_aba=SubAbaExportacaoSchema.ESPUMANTES, ano=ANO_MAX_2024 + 1
        )


def test_exportacao_path_params_invalid_subaba():
    with pytest.raises(ValidationError):
        ExportacaoPathParams(sub_aba="invalido", ano=2020)
