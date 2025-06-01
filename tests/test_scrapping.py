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
