from unittest.mock import MagicMock, patch

from app.fallback import fallback_creation
from app.fallback.fallback_creation import fetch_and_store


def test_fetch_and_store_success():
    mock_func = MagicMock(return_value={"resultado": 123})
    url = "http://fake-url"
    key_path = ["producao", "2022"]

    with (
        patch("app.fallback.fallback_creation.requests.get") as mock_get,
        patch(
            "app.fallback.fallback_creation.time.sleep",
            return_value=None,
        ),
    ):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_and_store(mock_func, url, key_path)

    assert result == (key_path, {"resultado": 123})
    mock_func.assert_called_once_with(mock_response)


def test_run_fallback_creation_fast():
    # Mock tasks para não rodar tudo
    fallback_creation.tasks = [
        (
            MagicMock(return_value={"ok": True}),
            "http://fake-url",
            ["producao", "2022"],
        )
    ]

    with (
        patch(
            "app.fallback.fallback_creation.fetch_and_store",
            return_value=(["producao", "2022"], {"ok": True}),
        ),
        patch("app.fallback.fallback_creation.os.makedirs"),
        patch("app.fallback.fallback_creation.open"),
        patch("app.fallback.fallback_creation.json.dump"),
        patch("app.fallback.fallback_creation.logger.info"),
    ):
        fallback_creation.run_fallback_creation(max_workers=1)


def test_fetch_and_store_error():
    # Mock da função de extração que lança exceção
    def raise_error(response):
        raise ValueError("Erro de extração")

    url = "http://fake-url"
    key_path = ["producao", "2022"]

    with patch("app.fallback.fallback_creation.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_and_store(raise_error, url, key_path)

    # Deve retornar (key_path, None) em caso de erro
    assert result == (key_path, None)
