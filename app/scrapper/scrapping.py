from bs4 import BeautifulSoup


def _parse_table(response, table_class, n_cols, row_parser, skip_header=False):
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_=table_class)
    if not table:
        return []
    rows = table.find_all("tr")
    if skip_header:
        rows = rows[1:]
    result = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != n_cols:
            continue
        parsed = row_parser(cols)
        if parsed:
            result.append(parsed)
    return result


def extract_producao_data(response):
    tipo_produto = {"value": None}

    def row_parser(cols):
        td_classes = cols[0].get("class", [])
        text_0 = cols[0].get_text(strip=True)
        text_1 = cols[1].get_text(strip=True)
        if "tb_item" in td_classes:
            tipo_produto["value"] = text_0
            return None
        elif "tb_subitem" in td_classes and tipo_produto["value"]:
            return {
                "tipo_produto": tipo_produto["value"].title(),
                "produto": text_0.lower(),
                "quantidade_litros": int(text_1.replace(".", "").replace(",", ".").replace("-", "0"))
            }
        return None
    return _parse_table(response, "tb_base tb_dados", 2, row_parser, skip_header=True)


def extract_processamento_data(response):
    current_group = {"value": None}

    def row_parser(cols):
        cultivar = cols[0].get_text(strip=True)
        quantidade = cols[1].get_text(strip=True)
        td_classes = cols[0].get("class", [])
        if "tb_item" in td_classes:
            current_group["value"] = cultivar
            return None
        if "tb_subitem" in td_classes and current_group["value"]:
            return {
                "tipo_uva": current_group["value"],
                "cultivo": cultivar,
                "quantidade_kg": int(quantidade.replace(".", "").replace("-", "0"))
            }
        return None
    return _parse_table(response, "tb_base tb_dados", 2, row_parser)


def extract_comercializacao_data(response):
    tipo_produto = {"value": None}

    def row_parser(cols):
        td_classes = cols[0].get("class", [])
        text_0 = cols[0].get_text(strip=True)
        text_1 = cols[1].get_text(strip=True)
        if "tb_item" in td_classes:
            tipo_produto["value"] = text_0.title()
            return None
        elif "tb_subitem" in td_classes and tipo_produto["value"]:
            return {
                "tipo_produto": tipo_produto["value"],
                "produto": text_0.lower(),
                "quantidade_litros": int(text_1.replace(".", "").replace("-", "0"))
            }
        return None
    return _parse_table(response, "tb_base tb_dados", 2, row_parser)


def extract_import_export_data(response):
    def row_parser(cols):
        pais = cols[0].get_text(strip=True)
        quantidade = cols[1].get_text(strip=True).replace(".", "").replace("-", "0")
        valor = cols[2].get_text(strip=True).replace(".", "").replace("-", "0")
        return {
            "pais": pais,
            "quantidade_kg": int(quantidade) if quantidade.isdigit() else 0,
            "valor_dolar": int(valor) if valor.isdigit() else 0,
        }
    return _parse_table(response, "tb_base tb_dados", 3, row_parser)
