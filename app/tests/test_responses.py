import pytest
from pydantic import ValidationError

from app.schemas.responses_schema import (
    ComercializacaoResponseSchema,
    ExportacaoResponseSchema,
    ImportacaoExportacaoSchema,
    ImportacaoResponseSchema,
    ProcessamentoResponseSchema,
    ProcessamentoSchema,
    ProducaoResponseSchema,
    ProdutoSchema,
)

VALOR_DOLAR_ARGENTINA = 5000
VALOR_DOLAR_CHILE = 8000
VALOR_DOLAR_URUGUAI = 6000
QUANTIDADE_KG_ARGENTINA = 10000
QUANTIDADE_KG_CHILE = 20000
QUANTIDADE_KG_URUGUAI = 15000
QUANTIDADE_TINTA_ALICANTE = 500
QUANTIDADE_LITROS_VINHO = 1000


def test_produto_schema_valid():
    produto = ProdutoSchema(
        tipo_produto="Vinho de mesa",
        produto="tinto",
        quantidade_litros=1000,
    )
    assert produto.tipo_produto == "Vinho de mesa"
    assert produto.produto == "tinto"
    assert produto.quantidade_litros == QUANTIDADE_LITROS_VINHO


def test_produto_schema_invalid():
    with pytest.raises(ValidationError):
        ProdutoSchema(
            tipo_produto="Vinho de mesa",
            produto="tinto",
            quantidade_litros="mil",
        )


def test_producao_response_schema_valid():
    data = [
        ProdutoSchema(
            tipo_produto="Vinho de mesa",
            produto="tinto",
            quantidade_litros=1000,
        )
    ]
    resp = ProducaoResponseSchema(data=data)
    assert resp.data[0].produto == "tinto"


def test_processamento_schema_valid():
    proc = ProcessamentoSchema(
        tipo_uva="Tinta",
        cultivo="Alicante",
        quantidade_kg=500,
    )
    assert proc.tipo_uva == "Tinta"
    assert proc.cultivo == "Alicante"
    assert proc.quantidade_kg == QUANTIDADE_TINTA_ALICANTE


def test_processamento_response_schema_valid():
    data = [
        ProcessamentoSchema(
            tipo_uva="Tinta",
            cultivo="Alicante",
            quantidade_kg=500,
        )
    ]
    resp = ProcessamentoResponseSchema(data=data)
    assert resp.data[0].cultivo == "Alicante"


def test_comercializacao_response_schema_valid():
    data = [
        ProdutoSchema(
            tipo_produto="Vinho de mesa",
            produto="branco",
            quantidade_litros=2000,
        )
    ]
    resp = ComercializacaoResponseSchema(data=data)
    assert resp.data[0].produto == "branco"


def test_importacao_exportacao_schema_valid():
    imp = ImportacaoExportacaoSchema(
        pais="Argentina",
        quantidade_kg=QUANTIDADE_KG_ARGENTINA,
        valor_dolar=VALOR_DOLAR_ARGENTINA,
    )
    assert imp.pais == "Argentina"
    assert imp.quantidade_kg == QUANTIDADE_KG_ARGENTINA
    assert imp.valor_dolar == VALOR_DOLAR_ARGENTINA


def test_importacao_response_schema_valid():
    data = [
        ImportacaoExportacaoSchema(
            pais="Chile",
            quantidade_kg=QUANTIDADE_KG_CHILE,
            valor_dolar=VALOR_DOLAR_CHILE,
        )
    ]
    resp = ImportacaoResponseSchema(data=data)
    assert resp.data[0].pais == "Chile"


def test_exportacao_response_schema_valid():
    data = [
        ImportacaoExportacaoSchema(
            pais="Uruguai",
            quantidade_kg=QUANTIDADE_KG_URUGUAI,
            valor_dolar=VALOR_DOLAR_URUGUAI,
        )
    ]
    resp = ExportacaoResponseSchema(data=data)
    assert resp.data[0].pais == "Uruguai"


def test_producao_response_schema_empty():
    resp = ProducaoResponseSchema(data=[])
    assert resp.data == []
