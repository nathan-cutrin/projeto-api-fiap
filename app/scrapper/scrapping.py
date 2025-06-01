from bs4 import BeautifulSoup


def extract_producao_data(response):
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        return []

    rows = table.find_all("tr")
    result = []
    tipo_produto = None

    n_cols = 2
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) != n_cols:
            continue

        td_classes = cols[0].get("class", [])
        text_0 = cols[0].get_text(strip=True)
        text_1 = cols[1].get_text(strip=True)

        if "tb_item" in td_classes:
            tipo_produto = text_0
        elif "tb_subitem" in td_classes and tipo_produto:
            result.append({
                "tipo_produto": tipo_produto.title(),
                "produto": text_0.lower(),
                "quantidade_litros": (
                    int(
                        text_1.replace(".", "")
                        .replace(",", ".")
                        .replace("-", "0")
                    )
                ),
            })
    return result


def extract_processamento_data(response):
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="tb_base tb_dados")
    if not table:
        return []

    rows = table.find_all("tr")
    result = []
    current_group = None

    n_cols = 2
    for row in rows:
        cols = row.find_all("td")
        if not cols or len(cols) < n_cols:
            continue
        cultivar = cols[0].get_text(strip=True)
        quantidade = cols[1].get_text(strip=True)

        if "tb_item" in cols[0].get("class", []):
            current_group = cultivar
            continue
        if "tb_subitem" in cols[0].get("class", []):
            result.append({
                "tipo_uva": current_group,
                "cultivo": cultivar,
                "quantidade_kg": quantidade,
            })
    return result


def extract_comercializacao_data(response):
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="tb_base tb_dados")
    if not table or not table.tbody:
        return {"data": []}

    result = []
    tipo_produto = None
    n_cols = 2
    for row in table.tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) != n_cols:
            continue

        td_classes = cols[0].get("class", [])
        text_0 = cols[0].get_text(strip=True)
        text_1 = cols[1].get_text(strip=True)

        if "tb_item" in td_classes:
            tipo_produto = text_0.title()
        elif "tb_subitem" in td_classes and tipo_produto:
            result.append({
                "tipo_produto": tipo_produto,
                "produto": text_0.lower(),
                "quantidade_litros": (
                    int(text_1.replace(".", "").replace("-", "0"))
                ),
            })
    return result


def extract_import_export_data(response):
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="tb_base tb_dados")
    if not table or not table.tbody:
        return []

    result = []
    n_cols = 3
    for row in table.tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == n_cols:
            pais = cols[0].get_text(strip=True)
            quantidade = cols[1].get_text(strip=True).replace(".", "").replace("-", "0")
            valor = cols[2].get_text(strip=True).replace(".", "").replace("-", "0")
            result.append({
                "pais": pais,
                "quantidade_kg": int(quantidade) if quantidade.isdigit() else 0,
                "valor_dolar": int(valor) if valor.isdigit() else 0,
            })
    return result