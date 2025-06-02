from http import HTTPStatus
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.app import app

API_PREFIX = "/api/v1"
client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get(f"{API_PREFIX}/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "Bem-vindo à API de Vitivinicultura da Embrapa"
    }


@patch("app.routes.routes.Embrapa_URL_Builder")
@patch("app.routes.routes.requests.get")
def test_get_producao_success(mock_requests_get, mock_url_builder):
    mock_url_builder.build_url.return_value = "http://fake-url"
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.text = "<html></html>"
    mock_requests_get.return_value = mock_response

    producao_mock = [
        {
            "tipo_produto": "Vinho De Mesa",
            "produto": "branco",
            "quantidade_litros": 400,
        }
    ]
    with patch(
        "app.routes.routes.extract_producao_data",
        return_value=producao_mock,
    ):
        response = client.get(f"{API_PREFIX}/producao/2023")
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.json()
        assert response.json()["data"] == producao_mock


@patch("app.routes.routes.Embrapa_URL_Builder")
@patch("app.routes.routes.requests.get")
def test_get_processamento_success(mock_requests_get, mock_url_builder):
    mock_url_builder.build_url.return_value = "http://fake-url"
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.text = "<html></html>"
    mock_requests_get.return_value = mock_response

    processamento_mock = [
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
    with patch(
        "app.routes.routes.extract_processamento_data",
        return_value=processamento_mock,
    ):
        response = client.get(f"{API_PREFIX}/processamento/viniferas/2023")
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.json()
        assert response.json()["data"] == processamento_mock


@patch("app.routes.routes.Embrapa_URL_Builder")
@patch("app.routes.routes.requests.get")
def test_get_comercializacao_success(mock_requests_get, mock_url_builder):
    mock_url_builder.build_url.return_value = "http://fake-url"
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.text = "<html></html>"
    mock_requests_get.return_value = mock_response

    comercializacao_mock = [
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
    with patch(
        "app.routes.routes.extract_comercializacao_data",
        return_value=comercializacao_mock,
    ):
        response = client.get(f"{API_PREFIX}/comercializacao/2023")
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.json()
        assert response.json()["data"] == comercializacao_mock


@patch("app.routes.routes.Embrapa_URL_Builder")
@patch("app.routes.routes.requests.get")
def test_get_importacao_success(mock_requests_get, mock_url_builder):
    mock_url_builder.build_url.return_value = "http://fake-url"
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.text = "<html></html>"
    mock_requests_get.return_value = mock_response

    importacao_mock = [
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
    with patch(
        "app.routes.routes.extract_import_export_data",
        return_value=importacao_mock,
    ):
        response = client.get(f"{API_PREFIX}/importacao/espumantes/2023")
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.json()
        assert response.json()["data"] == importacao_mock


@patch("app.routes.routes.Embrapa_URL_Builder")
@patch("app.routes.routes.requests.get")
def test_get_exportacao_success(mock_requests_get, mock_url_builder):
    mock_url_builder.build_url.return_value = "http://fake-url"
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.text = "<html></html>"
    mock_requests_get.return_value = mock_response

    exportacao_mock = [
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
    with patch(
        "app.routes.routes.extract_import_export_data",
        return_value=exportacao_mock,
    ):
        response = client.get(f"{API_PREFIX}/exportacao/espumantes/2023")
        assert response.status_code == HTTPStatus.OK
        assert "data" in response.json()
        assert response.json()["data"] == exportacao_mock


@patch("app.routes.routes.Embrapa_URL_Builder")
@patch(
    "app.routes.routes.requests.get",
    side_effect=Exception("Erro de conexão"),
)
def test_fetch_and_extract_error(mock_requests_get, mock_url_builder):
    response = client.get(f"{API_PREFIX}/producao/2023")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "detail" in response.json()
