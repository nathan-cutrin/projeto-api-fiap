import pytest

from app.scrapper import scrapping


class FakeResponse:
    def __init__(self, html):
        self.text = html


@pytest.fixture
def producao_html():
    return """
    <table class="tb_base tb_dados">
        <tr><td class="tb_item">Vinho de mesa</td>
            <td class="tb_item">1000</td></tr>
        <tr><td class="tb_subitem">Branco</td>
            <td class="tb_subitem">400</td></tr>
    </table>
    """


@pytest.fixture
def comercializacao_html():
    return """
    <table class="tb_base tb_dados">
        <tr><td class="tb_item">Vinho de mesa</td>
            <td class="tb_item">1000</td></tr>
        <tr><td class="tb_subitem">Tinto</td>
            <td class="tb_subitem">600</td></tr>
        <tr><td class="tb_subitem">Branco</td>
            <td class="tb_subitem">400</td></tr>
    </table>
    """


@pytest.fixture
def processamento_html():
    # Exemplo baseado no downloaded_processamento.html (apenas um recorte)
    return """
    <table class="tb_base tb_dados">
        <tr>
            <td class="tb_item">TINTAS</td>
            <td class="tb_item">35.881.118</td>
        </tr>
        <tr>
            <td class="tb_subitem">Alicante Bouschet</td>
            <td class="tb_subitem">4.108.858</td>
        </tr>
        <tr>
            <td class="tb_subitem">Ancelota</td>
            <td class="tb_subitem">783.688</td>
        </tr>
    </table>
    """


@pytest.fixture
def import_export_html():
    return """
    <table class="tb_base tb_dados">
        <tr>
            <td>Argentina</td>
            <td>1.000</td>
            <td>2.000</td>
        </tr>
        <tr>
            <td>Chile</td>
            <td>3.000</td>
            <td>4.000</td>
        </tr>
    </table>
    """


def test_extract_producao_data(producao_html):
    response = FakeResponse(producao_html)
    result = scrapping.extract_producao_data(response)
    assert result == [
        {
            "tipo_produto": "Vinho De Mesa",
            "produto": "Branco",
            "quantidade_litros": 400,
        },
    ]


def test_extract_processamento_data(processamento_html):
    response = FakeResponse(processamento_html)
    result = scrapping.extract_processamento_data(response)
    assert result == [
        {
            "tipo_uva": "Tintas",
            "cultivo": "Alicante Bouschet",
            "quantidade_kg": 4108858,
        },
        {
            "tipo_uva": "Tintas",
            "cultivo": "Ancelota",
            "quantidade_kg": 783688,
        },
    ]


def test_extract_comercializacao_data(comercializacao_html):
    response = FakeResponse(comercializacao_html)
    result = scrapping.extract_comercializacao_data(response)
    assert result == [
        {
            "tipo_produto": "Vinho De Mesa",
            "produto": "tinto",
            "quantidade_litros": 600,
        },
        {
            "tipo_produto": "Vinho De Mesa",
            "produto": "branco",
            "quantidade_litros": 400,
        },
    ]


def test_extract_import_export_data(import_export_html):
    response = FakeResponse(import_export_html)
    result = scrapping.extract_import_export_data(response)
    assert result == [
        {
            "pais": "Argentina",
            "quantidade_kg": 1000,
            "valor_dolar": 2000,
        },
        {
            "pais": "Chile",
            "quantidade_kg": 3000,
            "valor_dolar": 4000,
        },
    ]


def test_parse_table_no_table():
    html = "<html><body><p>Sem tabela aqui!</p></body></html>"
    response = FakeResponse(html)
    result = scrapping._parse_table(
        response, "tb_base tb_dados", 2, lambda cols: {"ok": True}
    )
    assert result == []


def test_parse_table_skip_header():
    html = """
    <table class="tb_base tb_dados">
        <tr><td>header1</td><td>header2</td></tr>
        <tr><td>valor1</td><td>valor2</td></tr>
    </table>
    """
    response = FakeResponse(html)

    def row_parser(cols):
        return {"col1": cols[0].get_text(), "col2": cols[1].get_text()}

    result = scrapping._parse_table(
        response, "tb_base tb_dados", 2, row_parser, skip_header=True
    )
    assert result == [{"col1": "valor1", "col2": "valor2"}]


def test_parse_table_wrong_n_cols():
    html = """
    <table class="tb_base tb_dados">
        <tr><td>apenas um</td></tr>
        <tr><td>dois</td><td>colunas</td></tr>
    </table>
    """
    response = FakeResponse(html)

    def row_parser(cols):
        return {
            "col1": cols[0].get_text(),
            "col2": cols[1].get_text(),
        }

    result = scrapping._parse_table(
        response, "tb_base tb_dados", 2, row_parser
    )
    assert result == [{"col1": "dois", "col2": "colunas"}]


def test_extract_producao_data_subitem_sem_contexto():
    html = """
    <table class="tb_base tb_dados">
        <tr>
            <td class="tb_subitem">Branco</td>
            <td class="tb_subitem">400</td>
        </tr>
    </table>
    """
    response = FakeResponse(html)
    result = scrapping.extract_producao_data(response)
    assert result == []  # Não há tb_item antes, então não retorna nada


def test_extract_processamento_data_subitem_sem_contexto():
    html = """
    <table class="tb_base tb_dados">
        <tr>
            <td class="tb_subitem">Alicante Bouschet</td>
            <td class="tb_subitem">4.108.858</td>
        </tr>
    </table>
    """
    response = FakeResponse(html)
    result = scrapping.extract_processamento_data(response)
    assert result == []  # Não há tb_item antes, então não retorna nada


def test_extract_comercializacao_data_linha_invalida():
    html = """
    <table class="tb_base tb_dados">
        <tr>
            <td>Sem classe</td>
            <td>123</td>
        </tr>
    </table>
    """
    response = FakeResponse(html)
    result = scrapping.extract_comercializacao_data(response)
    assert result == []  # Linha sem classe tb_item/tb_subitem é ignorada
