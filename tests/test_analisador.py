"""Testes do AnalisadorDados."""

import pytest

from analise import AnalisadorDados


def test_dados_antes_de_integrar_gera_erro(df_desmatamento, df_credito):
    analisador = AnalisadorDados(df_desmatamento, df_credito)
    with pytest.raises(RuntimeError):
        _ = analisador.dados


@pytest.mark.skip(reason="TODO: implementar limpar_desmatamento")
def test_remove_linhas_acumuladas_de_2007(df_desmatamento, df_credito):
    ...


@pytest.mark.skip(reason="TODO: implementar limpar_desmatamento")
def test_remove_duplicados(df_desmatamento, df_credito):
    ...


@pytest.mark.skip(reason="TODO: implementar integrar")
def test_credito_ausente_vira_zero(df_desmatamento, df_credito):
    ...


@pytest.mark.skip(reason="TODO: implementar filtrar")
def test_filtrar_por_uf_e_ano(df_desmatamento, df_credito):
    ...
