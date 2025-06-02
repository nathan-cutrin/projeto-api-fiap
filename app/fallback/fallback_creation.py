import json
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from app.mapper.url_mapper import URLMapper
from app.schemas.invocation_parameters_schema import (
    SubAbaExportacaoSchema,
    SubAbaImportacaoSchema,
    SubAbaProcessamentoSchema,
)
from app.scrapper.scrapping import (
    extract_comercializacao_data,
    extract_import_export_data,
    extract_processamento_data,
    extract_producao_data,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

anos_producao = range(1970, 2024)
anos_processamento = range(1970, 2024)
anos_comercializacao = range(1970, 2024)
anos_import_export = range(1970, 2025)
fallback_data = {}

# Monta a lista de tarefas (função, url, key_path)
tasks = []

for ano in anos_producao:
    url = URLMapper.build_url(option="producao", year=ano)
    tasks.append((extract_producao_data, url, ["producao", str(ano)]))

for sub in SubAbaProcessamentoSchema:
    for ano in anos_processamento:
        url = URLMapper.build_url(
            option="processamento", suboption=sub.value, year=ano
        )
        tasks.append((
            extract_processamento_data,
            url,
            ["processamento", sub.value, str(ano)],
        ))

for ano in anos_comercializacao:
    url = URLMapper.build_url(option="comercializacao", year=ano)
    tasks.append((
        extract_comercializacao_data,
        url,
        ["comercializacao", str(ano)],
    ))

for sub in SubAbaImportacaoSchema:
    for ano in anos_import_export:
        url = URLMapper.build_url(
            option="importacao", suboption=sub.value, year=ano
        )
        tasks.append((
            extract_import_export_data,
            url,
            ["importacao", sub.value, str(ano)],
        ))

for sub in SubAbaExportacaoSchema:
    for ano in anos_import_export:
        url = URLMapper.build_url(
            option="exportacao", suboption=sub.value, year=ano
        )
        tasks.append((
            extract_import_export_data,
            url,
            ["exportacao", sub.value, str(ano)],
        ))


def fetch_and_store(func, url, key_path):
    logger.info(f"Processando {url} ...")
    try:
        time.sleep(0.5)  # Aguarda 0.5 segundos antes de cada requisição
        # (ajuste conforme necessário)
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = func(response)
        logger.info(f"Dados salvos para {url}")
        return (key_path, data)
    except Exception as e:
        logger.error(f"Erro ao processar {url}: {e}")
        return (key_path, None)


def run_fallback_creation(max_workers=12):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(fetch_and_store, func, url, key_path)
            for func, url, key_path in tasks
        ]
        for future in as_completed(futures):
            key_path, data = future.result()
            if data is not None:
                d = fallback_data
                for key in key_path[:-1]:
                    d = d.setdefault(key, {})
                d[key_path[-1]] = data

    os.makedirs("app/fallback", exist_ok=True)
    with open("app/fallback/fallback_data.json", "w", encoding="utf-8") as f:
        json.dump(fallback_data, f, ensure_ascii=False, indent=2)

    logger.info("Arquivo fallback_data.json criado com sucesso!")


if __name__ == "__main__":
    run_fallback_creation()
