from http import HTTPStatus

import requests
from fastapi import FastAPI, HTTPException

from app.mapper.url_mapper import URLMapper
from app.schemas.embrapa_schema import (
    SubAbaExportacaoSchema,
    SubAbaImportacaoSchema,
    SubAbaProcessamentoSchema,
    ano_query,
    ano_query_imp_exp,
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


@app.get("/", status_code=HTTPStatus.OK)
def read_root():
    return {"message": "Bem-vindo à API de Vitivinicultura da Embrapa"}


@app.get("/producao/", status_code=HTTPStatus.OK)
async def get_producao(ano: int = ano_query):
    return fetch_and_extract(
        option="producao",
        suboption=None,
        year=ano,
        extract_func=extract_producao_data,
    )


@app.get("/processamento/", status_code=HTTPStatus.OK)
async def get_processamento(
    sub_aba: SubAbaProcessamentoSchema, ano: int = ano_query
):
    return fetch_and_extract(
        option="processamento",
        suboption=sub_aba,
        year=ano,
        extract_func=extract_processamento_data,
    )


@app.get("/comercializacao")
def get_comercializacao(ano: int = ano_query):
    return fetch_and_extract(
        option="comercializacao",
        suboption=None,
        year=ano,
        extract_func=extract_comercializacao_data,
    )


@app.get("/importacao")
async def get_importacao(
    sub_aba: SubAbaImportacaoSchema, ano: int = ano_query_imp_exp
):
    return fetch_and_extract(
        option="importacao",
        suboption=sub_aba,
        year=ano,
        extract_func=extract_importacao_data,
    )


@app.get("/exportacao")
async def get_exportacao(
    sub_aba: SubAbaExportacaoSchema, ano: int = ano_query_imp_exp
):
    return fetch_and_extract(
        option="exportacao",
        suboption=sub_aba,
        year=ano,
        extract_func=extract_exportacao_data,
    )
