import logging
from http import HTTPStatus

import requests
from fastapi import APIRouter, HTTPException, Path, Response

from app.fallback.fallback_handler import get_fallback_data
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
    extract_import_export_data,
    extract_processamento_data,
    extract_producao_data,
)

logger = logging.getLogger(__name__)

router = APIRouter()
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
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


@router.get(
    "/producao/{ano}",
    status_code=HTTPStatus.OK,
    response_model=ProducaoResponseSchema,
    description=(
        "Obtém dados de produção da vitivinicultura. "
        "Retorna informações sobre a produção vitivinícola, "
        "como tipos de produto (vinho, suco, etc), produto e ano de produção."
    ),
)
async def get_producao(
    params: ProducaoPathParams = Path(...),
    response: Response = None,
):
    """
    Obtém dados de produção da vitivinicultura.

    Args:
        params (ProducaoPathParams): Parâmetros contém 'ano' (ano de produção).

    Returns:
        dict: Dados extraídos de produção conforme os parâmetros fornecidos.
    """
    aba = "producao"
    try:
        result = fetch_and_extract(
            option=aba,
            suboption=None,
            year=params.ano,
            extract_func=extract_producao_data,
        )
        return result

    except Exception as e:
        logger.warning(f"Usando fallback para {aba} {params.ano}: {e}")
        if response:
            response.headers["X-Fallback"] = "true"
        return get_fallback_data(aba, params)


@router.get(
    "/processamento/{sub_aba}/{ano}",
    status_code=HTTPStatus.OK,
    response_model=ProcessamentoResponseSchema,
    description=(
        "Obtém dados de processamento da vitivinicultura "
        "Retorna informações sobre o processamento de vinhos, "
        "uvas e derivados."
    ),
)
async def get_processamento(
    params: ProcessamentoPathParams = Path(...),
    response: Response = None,
):
    """
    Obtém dados de processamento da vitivinicultura.

    Args:
        params (ProcessamentoPathParams): Parâmetros contendo 'sub_aba'
            (subopção) e 'ano' (ano de referência).

    Returns:
        dict: Dados extraídos de processamento conforme os parâmetros
            fornecidos.
    """
    aba = "processamento"
    try:
        return fetch_and_extract(
            option=aba,
            suboption=params.sub_aba,
            year=params.ano,
            extract_func=extract_processamento_data,
        )
    except Exception as e:
        logger.warning(
            f"Usando fallback para {aba} {params.sub_aba} {params.ano}: {e}"
        )
        if response:
            response.headers["X-Fallback"] = "true"
        return get_fallback_data(aba, params)


@router.get(
    "/comercializacao/{ano}",
    status_code=HTTPStatus.OK,
    response_model=ComercializacaoResponseSchema,
    description=(
        "Obtém dados de comercialização da vitivinicultura. "
        "Retorna informações sobre comercialização de uvas, "
        "vinho e derivados."
    ),
)
async def get_comercializacao(
    params: ComercializacaoPathParams = Path(...),
    response: Response = None,
):
    """
    Obtém dados de comercialização da vitivinicultura.

    Args:
        params (ComercializacaoPathParams): Parâmetros contém
        'ano' (ano de referência).

    Returns:
        dict: Dados extraídos de comercialização conforme os parâmetros
            fornecidos.
    """
    aba = "comercializacao"
    try:
        return fetch_and_extract(
            option=aba,
            suboption=None,
            year=params.ano,
            extract_func=extract_comercializacao_data,
        )
    except Exception as e:
        logger.warning(f"Usando fallback para {aba} {params.ano}: {e}")
        if response:
            response.headers["X-Fallback"] = "true"
        return get_fallback_data(aba, params)


@router.get(
    "/importacao/{sub_aba}/{ano}",
    status_code=HTTPStatus.OK,
    response_model=ImportacaoResponseSchema,
    description=(
        "Obtém dados de importação da vitivinicultura."
        "Retorna informações sobre importacao de  derivados de uva."
    ),
)
async def get_importacao_(
    params: ImportacaoPathParams = Path(...),
    response: Response = None,
):
    """
    Obtém dados de importação da vitivinicultura.

    Args:
        params (ImportacaoPathParams): Parâmetros contendo 'sub_aba'
            (subopção) e 'ano' (ano de referência).

    Returns:
        dict: Dados extraídos de importação conforme os parâmetros
            fornecidos.
    """
    aba = "importacao"
    try:
        return fetch_and_extract(
            option=aba,
            suboption=params.sub_aba,
            year=params.ano,
            extract_func=extract_import_export_data,
        )
    except Exception as e:
        logger.warning(
            f"Usando fallback para {aba} {params.sub_aba} {params.ano}: {e}"
        )
        if response:
            response.headers["X-Fallback"] = "true"
        return get_fallback_data(aba, params)


@router.get(
    "/exportacao/{sub_aba}/{ano}",
    status_code=HTTPStatus.OK,
    response_model=ExportacaoResponseSchema,
    description=(
        "Obtém dados de exportação da vitivinicultura."
        "Retorna informações sobre exportação de  derivados de uva."
    ),
)
async def get_exportacao(
    params: ExportacaoPathParams = Path(...),
    response: Response = None,
):
    """
    Obtém dados de exportação da vitivinicultura.

    Args:
        params (ExportacaoPathParams): Parâmetros contendo 'sub_aba'
            (subopção) e 'ano' (ano de referência).

    Returns:
        dict: Dados extraídos de exportação conforme os parâmetros
            fornecidos.
    """
    aba = "exportacao"
    try:
        return fetch_and_extract(
            option=aba,
            suboption=params.sub_aba,
            year=params.ano,
            extract_func=extract_import_export_data,
        )
    except Exception as e:
        logger.warning(
            f"Usando fallback para {aba} {params.sub_aba} {params.ano}: {e}"
        )
        if response:
            response.headers["X-Fallback"] = "true"
        return get_fallback_data(aba, params)
