"""Testes do Analisador."""

from analisador import Analisador


def test_filtrar_por_estado_e_ano(base, produtos):
    tabela = Analisador(base, produtos).filtrar(["RO"], 2021, 2021)
    assert len(tabela) == 2                         # 2 municípios de RO em 2021
    assert tabela["uf"].unique().tolist() == ["RO"]


def test_somar_por_municipio(base, produtos):
    municipios = Analisador(base, produtos).somar_por_municipio(base)
    ariquemes = municipios[municipios["municipio"] == "Ariquemes"]
    assert ariquemes["incremento_km2"].iloc[0] == 90.0     # 50 + 40


def test_classificar_marca_o_critico(base, produtos):
    municipios = Analisador(base, produtos).classificar(base)
    criticos = municipios[municipios["grupo"] == "Crítico"]
    assert criticos["municipio"].tolist() == ["Ariquemes"]  # o que mais desmata


def test_resumo_nao_divide_por_zero(base, produtos):
    sem_desmatamento = base[base["uf"] == "MT"]             # Acorizal tem 0 km²
    resumo = Analisador(base, produtos).resumo(sem_desmatamento)
    assert resumo["credito_por_km2"] == 0


def test_pergunta2_produtos_dos_criticos(base, produtos):
    resultado = Analisador(base, produtos).pergunta2(base, "Crítico")
    assert resultado["valor"].sum() == 900.0                # 500 + 400 de Ariquemes


def test_pergunta4_soma_por_estado_e_ano(base, produtos):
    serie = Analisador(base, produtos).pergunta4(base)
    ro_2020 = serie[(serie["uf"] == "RO") & (serie["ano_prodes"] == 2020)]
    assert ro_2020["credito_total"].iloc[0] == 1000.0       # 100 + 900
