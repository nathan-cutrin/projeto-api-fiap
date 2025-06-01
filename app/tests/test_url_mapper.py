import pytest

from app.mapper.url_mapper import URLMapper


def test_build_url_with_valid_option():
    url = URLMapper.build_url("producao")
    assert url == ("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")


def test_build_url_with_valid_option_and_year():
    url = URLMapper.build_url("producao", year=2020)
    assert url == (
        "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano=2020"
    )


def test_build_url_with_valid_option_and_suboption():
    url = URLMapper.build_url("processamento", suboption="viniferas")
    assert url == (
        "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03&subopcao=subopt_01"
    )


def test_build_url_with_valid_option_suboption_and_year():
    url = URLMapper.build_url("importacao", suboption="espumantes", year=2022)
    assert url == (
        "http://vitibrasil.cnpuv.embrapa.br/index.php?"
        "opcao=opt_05&subopcao=subopt_02&ano=2022"
    )


def test_build_url_invalid_option():
    with pytest.raises(ValueError, match="Invalid option: invalid"):
        URLMapper.build_url("invalid")


def test_build_url_invalid_suboption():
    with pytest.raises(
        ValueError,
        match="Invalid suboption: invalid_sub for option: processamento",
    ):
        URLMapper.build_url("processamento", suboption="invalid_sub")


def test_build_url_suboption_not_allowed_for_option():
    with pytest.raises(
        ValueError, match="Invalid suboption: viniferas for option: producao"
    ):
        URLMapper.build_url("producao", suboption="viniferas")
