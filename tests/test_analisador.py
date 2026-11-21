"""Testes do AnalisadorCreditoDesmatamento. Tire o @skip quando implementar cada método."""

import pytest

from analise import AnalisadorCreditoDesmatamento


def test_ufs_e_anos_disponiveis(df_base, df_por_produto):
    analisador = AnalisadorCreditoDesmatamento(df_base, df_por_produto)
    assert analisador.ufs == ["MT", "RO"]
    assert analisador.anos == (2020, 2021)


@pytest.mark.skip(reason="TODO: implementar filtrar")
def test_filtrar_por_uf_e_ano(df_base, df_por_produto):
    analisador = AnalisadorCreditoDesmatamento(df_base, df_por_produto)
    df = analisador.filtrar(ufs=["RO"], ano_inicial=2021, ano_final=2021)
    assert len(df) == 2
    assert set(df["uf"]) == {"RO"}


@pytest.mark.skip(reason="TODO: implementar acumular_por_municipio e ranking")
def test_ranking_de_desmatamento(df_base, df_por_produto):
    analisador = AnalisadorCreditoDesmatamento(df_base, df_por_produto)
    m = analisador.acumular_por_municipio(df_base)
    assert analisador.ranking(m, "incremento_km2", n=1)["municipio"].iloc[0] == "Ariquemes"


@pytest.mark.skip(reason="TODO: implementar p4_serie_por_uf")
def test_serie_por_uf(df_base, df_por_produto):
    s = AnalisadorCreditoDesmatamento.p4_serie_por_uf(df_base)
    ro_2020 = s[(s["uf"] == "RO") & (s["ano_prodes"] == 2020)]
    assert ro_2020["credito_total"].iloc[0] == 1000.0
