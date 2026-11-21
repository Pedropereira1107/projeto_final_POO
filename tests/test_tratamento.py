"""Testes do TratadorCredito e do IntegradorMunicipal (preparar_dados.py).

As classes leem arquivos de uma pasta, então os testes gravam CSVs pequenos
em uma pasta temporária (``tmp_path``) e apontam as classes para ela.
"""

import json

import pytest

from preparar_dados import IntegradorMunicipal, TratadorCredito


@pytest.fixture
def pasta_dados(tmp_path, df_custeio_bruto, df_invest_bruto):
    """Pasta temporária com 1 CSV de custeio, 1 de investimento, o PRODES e a lista de municípios."""
    df_custeio_bruto.to_csv(tmp_path / "mdcr_custeio_2020_amazonia_legal.csv", index=False)
    df_invest_bruto.to_csv(tmp_path / "mdcr_investimento_2021_amazonia_legal.csv", index=False)
    (tmp_path / "prodes_incremento_municipios_amazonia_legal.csv").write_text(
        "codibge,municipio,uf,ano_prodes,inicio_periodo,fim_periodo,incremento_km2\n"
        "1100023,Ariquemes,RO,2021,2020-08-01,2021-07-31,5.0\n",
        encoding="utf-8",
    )
    nomes = {"lois": [{"name": "mun", "loinames": [{"codibge": 1100023}, {"codibge": 1100015}]}]}
    (tmp_path / "prodes_legal_amazon_nomes_bruto.json").write_text(json.dumps(nomes), encoding="utf-8")
    return tmp_path


def test_investimento_recebe_codigo_ibge_pelo_cadmu(pasta_dados):
    credito = TratadorCredito(pasta_dados).processar()
    invest = credito[credito["finalidade"] == "investimento"]
    assert invest["cod_ibge"].tolist() == ["1100023"]  # a linha com cadmu 99999 foi descartada


def test_ano_prodes_vai_de_agosto_a_julho(pasta_dados):
    credito = TratadorCredito(pasta_dados).processar()
    custeio = credito[credito["finalidade"] == "custeio"].sort_values("mes")
    assert custeio["ano_prodes"].tolist() == [2020, 2021]


def test_limpa_aspas_do_produto_e_cria_uf(pasta_dados):
    credito = TratadorCredito(pasta_dados).processar()
    assert "BOVINOS" in set(credito["produto"])
    assert set(credito["uf"]) == {"RO"}


def test_integrador_monta_grade_completa_com_zeros(pasta_dados):
    credito = TratadorCredito(pasta_dados).processar()
    base = IntegradorMunicipal(pasta_dados).integrar(credito)

    assert len(base) == 2 * len(IntegradorMunicipal.ANOS)  # 2 municípios × 12 anos
    assert base["incremento_km2"].sum() == 5.0             # desmatamento preservado
    assert base["credito_total"].sum() == 3500             # 1000 + 500 + 2000
    sem_nada = base[base["cod_ibge"] == "1100015"]
    assert (sem_nada["credito_total"] == 0).all()          # ausente vira 0
