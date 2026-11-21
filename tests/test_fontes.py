"""Testes das classes de fontes de dados."""

import pytest

from fontes import FonteCSV, FonteDados


def test_fonte_dados_eh_abstrata():
    with pytest.raises(TypeError):
        FonteDados("qualquer")  # type: ignore[abstract]


def test_fonte_csv_eh_fonte_dados():
    assert isinstance(FonteCSV("teste", "arquivo.csv"), FonteDados)


@pytest.mark.skip(reason="TODO: implementar FonteCSV.carregar")
def test_fonte_csv_carrega_arquivo(tmp_path):
    ...


@pytest.mark.skip(reason="TODO: implementar FonteDados.obter")
def test_obter_usa_cache():
    ...


@pytest.mark.skip(reason="TODO: implementar FonteAPI (usar monkeypatch em requests.get para simular o IPCA)")
def test_fonte_api_converte_json_em_dataframe(monkeypatch):
    ...
