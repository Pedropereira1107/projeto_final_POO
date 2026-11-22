"""Testes do tratamento (TratadorCredito) e da integração (IntegradorMunicipal)."""

import pandas as pd

from preparar_dados import IntegradorMunicipal, TratadorCredito


def test_investimento_recebe_codigo_ibge(custeio, investimento, ipca_zero):
    credito = TratadorCredito(custeio, investimento, ipca_zero).processar()
    invest = credito[credito["finalidade"] == "investimento"]
    assert invest["cod_ibge"].tolist() == ["1100023"]   # a linha sem tradução (99999) foi descartada


def test_ano_prodes_vai_de_agosto_a_julho(custeio, investimento, ipca_zero):
    credito = TratadorCredito(custeio, investimento, ipca_zero).processar()
    custeio_tratado = credito[credito["finalidade"] == "custeio"].sort_values("mes")
    assert custeio_tratado["ano_prodes"].tolist() == [2020, 2021]   # julho -> 2020, agosto -> 2021


def test_tira_aspas_e_cria_uf(custeio, investimento, ipca_zero):
    credito = TratadorCredito(custeio, investimento, ipca_zero).processar()
    assert "BOVINOS" in credito["produto"].tolist()
    assert credito["uf"].unique().tolist() == ["RO"]


def test_corrige_pela_inflacao(custeio, investimento):
    # Inflação de 10% só no último mês: tudo o que é de antes vale 10% a mais
    ipca = pd.DataFrame({"data": ["01/07/2020", "01/08/2020", "01/01/2021"],
                         "valor": ["0", "0", "10"]})
    credito = TratadorCredito(custeio, investimento, ipca).processar()
    julho = credito[credito["mes"] == 7]
    assert round(julho["valor"].iloc[0], 2) == 1100.0   # 1000 x 1,10


def test_integrador_monta_grade_completa(custeio, investimento, ipca_zero):
    credito = TratadorCredito(custeio, investimento, ipca_zero).processar()
    prodes = pd.DataFrame({"codibge": ["1100023"], "ano_prodes": ["2021"], "incremento_km2": ["5.0"]})
    municipios = pd.DataFrame({"cod_ibge": ["1100023", "1100015"],
                               "municipio": ["Ariquemes", "Alta Floresta D'Oeste"],
                               "uf": ["RO", "RO"]})

    base = IntegradorMunicipal(credito, prodes, municipios).montar_base()

    assert len(base) == 2 * 12                          # 2 municípios x 12 anos (2014 a 2025)
    assert base["incremento_km2"].sum() == 5.0          # o desmatamento não se perdeu
    assert base["credito_total"].sum() == 3500.0        # 1000 + 500 + 2000
    sem_nada = base[base["cod_ibge"] == "1100015"]
    assert sem_nada["credito_total"].sum() == 0         # sem crédito = 0 (e não vazio)
