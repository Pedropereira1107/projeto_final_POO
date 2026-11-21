"""Testes do TratadorCredito e do IntegradorMunicipal (código já implementado)."""

import pandas as pd

from tratamento import IntegradorMunicipal, TratadorCredito


def test_investimento_recebe_codigo_ibge_pelo_cadmu(df_custeio_bruto, df_invest_bruto):
    tratador = TratadorCredito(df_custeio_bruto, df_invest_bruto)
    credito = tratador.processar()
    invest = credito[credito["finalidade"] == "investimento"]
    assert invest["cod_ibge"].tolist() == ["1100023"]
    assert tratador.linhas_descartadas == 1


def test_ano_prodes_vai_de_agosto_a_julho(df_custeio_bruto, df_invest_bruto):
    credito = TratadorCredito(df_custeio_bruto, df_invest_bruto).processar()
    custeio = credito[credito["finalidade"] == "custeio"].sort_values("mes")
    assert custeio["ano_prodes"].tolist() == [2020, 2021]


def test_limpa_aspas_do_produto_e_cria_uf(df_custeio_bruto, df_invest_bruto):
    credito = TratadorCredito(df_custeio_bruto, df_invest_bruto).processar()
    assert "BOVINOS" in set(credito["produto"])
    assert set(credito["uf"]) == {"RO"}


def test_integrador_monta_grade_completa_com_zeros(df_custeio_bruto, df_invest_bruto):
    credito = TratadorCredito(df_custeio_bruto, df_invest_bruto).processar()
    municipios = pd.DataFrame({"cod_ibge": ["1100023", "1100015"]})
    prodes = pd.DataFrame({"codibge": ["1100023"], "municipio": ["Ariquemes"],
                           "ano_prodes": [2021], "incremento_km2": [5.0]})
    base = IntegradorMunicipal(municipios, prodes, anos=range(2020, 2022)).integrar(credito)

    assert len(base) == 4                       # 2 municípios × 2 anos
    assert base["incremento_km2"].sum() == 5.0  # desmatamento preservado
    assert base["credito_total"].sum() == 3500  # 1000 + 500 + 2000
    sem_nada = base[base["cod_ibge"] == "1100015"]
    assert (sem_nada["credito_total"] == 0).all()  # ausente vira 0
