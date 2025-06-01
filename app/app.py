from http import HTTPStatus

import requests
from fastapi import FastAPI, HTTPException, Path

from app.mapper.url_mapper import URLMapper
from app.schemas.invocation_parameters_schema import (
    ComercializacaoPathParams,
    ExportacaoPathParams,
    ImportacaoPathParams,
    ProcessamentoPathParams,
    ProducaoPathParams,
)
from app.schemas.responses_schema import (
    ComercializacaoResponseSchema,
    ExportacaoResponseSchema,
    ImportacaoResponseSchema,
    ProcessamentoResponseSchema,
    ProducaoResponseSchema,
)
from app.scrapper.scrapping import (
    extract_comercializacao_data,
    extract_exportacao_data,
    extract_importacao_data,
    extract_processamento_data,
    extract_producao_data,
)

app = FastAPI(
    title="Embrapa Vitivinicultura API",
    description="API para consulta de dados de vitivinicultura da Embrapa.",
    version="1.0",
)

Embrapa_URL_Builder = URLMapper()


def fetch_and_extract(option, suboption, year, extract_func):
    """
    Realiza a requisição à URL construída e extrai os dados
    utilizando a função de extração fornecida.

    Args:
        option (str): Opção principal da consulta
            (ex: 'producao', 'processamento').
        suboption (str): Subopção ou categoria específica.
        year (int): Ano de referência.
        extract_func (callable): Função responsável por extrair
            os dados da resposta.

    Returns:
        dict: Dados extraídos da resposta.
    """
    try:
        request_url = Embrapa_URL_Builder.build_url(
            option=option, suboption=suboption, year=year
        )
        request_response = requests.get(request_url)
        request_response.raise_for_status()
        extracted_data = extract_func(request_response)
        return {"data": extracted_data}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/",
    status_code=HTTPStatus.OK,
    description="Endpoint raiz da API. Retorna uma mensagem de boas-vindas.",
)
def read_root():
    """
    Endpoint raiz da API.

    Returns:
        dict: Mensagem de boas-vindas para a API de Vitivinicultura da Embrapa.
    """
    return {"message": "Bem-vindo à API de Vitivinicultura da Embrapa"}


@app.get(
    "/producao/",
    status_code=HTTPStatus.OK,
    response_model=ProducaoResponseSchema,
    description=(
        "Obtém dados de produção da vitivinicultura, permitindo filtragem "
        "por subopção e ano."
        "Retorna informações detalhadas sobre a produção vitivinícola, "
        "como volume produzido, tipo de produto e outras métricas relevantes."
    ),
)
async def get_producao(params: ProducaoPathParams = Path(...)):
    """
    Obtém dados de produção da vitivinicultura.

    Args:
        params (ProducaoPathParams): Parâmetros contendo 'sub_aba'
            (subopção) e 'ano' (ano de referência).

    Returns:
        dict: Dados extraídos de produção conforme os parâmetros fornecidos.
    """
    result = fetch_and_extract(
        option="producao",
        suboption=None,
        year=None,
        extract_func=extract_producao_data,
    )
    return result


@app.get(
    "/processamento/{sub_aba}/{ano}",
    status_code=HTTPStatus.OK,
    response_model=ProcessamentoResponseSchema,
    description=(
        "Obtém dados de processamento da vitivinicultura para a subopção e "
        "ano informados. Retorna informações sobre o processamento de uvas e "
        "derivados."
    ),
)
async def get_processamento(params: ProcessamentoPathParams = Path(...)):
    """
    Obtém dados de processamento da vitivinicultura.

    Args:
        params (ProcessamentoPathParams): Parâmetros contendo 'sub_aba'
            (subopção) e 'ano' (ano de referência).

    Returns:
        dict: Dados extraídos de processamento conforme os parâmetros
            fornecidos.
    """
    return fetch_and_extract(
        option="processamento",
        suboption=params.sub_aba,
        year=params.ano,
        extract_func=extract_processamento_data,
    )


@app.get(
    "/comercializacao",
    status_code=HTTPStatus.OK,
    response_model=ComercializacaoResponseSchema,
    description=(
        "Obtém dados de comercialização da vitivinicultura, permitindo "
        "filtragem por subopção e ano. Retorna informações sobre vendas, "
        "distribuição e comercialização de produtos vitivinícolas."
    ),
)
async def get_comercializacao(params: ComercializacaoPathParams = Path(...)):
    """
    Obtém dados de comercialização da vitivinicultura.

    Args:
        params (ComercializacaoPathParams): Parâmetros contendo 'sub_aba'
            (subopção) e 'ano' (ano de referência).

    Returns:
        dict: Dados extraídos de comercialização conforme os parâmetros
            fornecidos.
    """
    return fetch_and_extract(
        option="comercializacao",
        suboption=None,
        year=params.ano,
        extract_func=extract_comercializacao_data,
    )


@app.get(
    "/importacao/{sub_aba}/{ano}",
    status_code=HTTPStatus.OK,
    response_model=ImportacaoReponseSchema,
    description=(
        "Obtém dados de importação da vitivinicultura para a subopção e ano "
        "informados. Retorna informações sobre importação de uvas, vinhos e "
        "derivados."
    ),
)
async def get_importacao_(params: ImportacaoPathParams = Path(...)):
    """
    Obtém dados de importação da vitivinicultura.

    Args:
        params (ImportacaoPathParams): Parâmetros contendo 'sub_aba'
            (subopção) e 'ano' (ano de referência).

    Returns:
        dict: Dados extraídos de importação conforme os parâmetros
            fornecidos.
    """
    return fetch_and_extract(
        option="importacao",
        suboption=params.sub_aba,
        year=params.ano,
        extract_func=extract_importacao_data,
    )


@app.get(
    "/exportacao/{sub_aba}/{ano}",
    status_code=HTTPStatus.OK,
    response_model=ExportacaoResponseSchema,
    description=(
        "Obtém dados de exportação da vitivinicultura para a subopção e ano "
        "informados. Retorna informações sobre exportação de uvas, vinhos e "
        "derivados."
    ),
)
async def get_exportacao(params: ExportacaoPathParams = Path(...)):
    """
    Obtém dados de exportação da vitivinicultura.

    Args:
        params (ExportacaoPathParams): Parâmetros contendo 'sub_aba'
            (subopção) e 'ano' (ano de referência).

    Returns:
        dict: Dados extraídos de exportação conforme os parâmetros
            fornecidos.
    """
    return fetch_and_extract(
        option="exportacao",
        suboption=params.sub_aba,
        year=params.ano,
        extract_func=extract_exportacao_data,
    )
