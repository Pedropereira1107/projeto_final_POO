"""Fixtures compartilhadas: pequenos DataFrames sintéticos no formato dos dados reais."""

import pandas as pd
import pytest


@pytest.fixture
def df_custeio_bruto() -> pd.DataFrame:
    """Formato da consulta CusteioMunicipioProduto (tudo texto, como lido com dtype=str)."""
    return pd.DataFrame({
        "Municipio": ["ARIQUEMES", "ARIQUEMES"],
        "nomeProduto": ['"BOVINOS"', '"CAFÉ"'],
        "MesEmissao": ["07", "08"],          # julho -> PRODES 2020; agosto -> PRODES 2021
        "AnoEmissao": ["2020", "2020"],
        "cdPrograma": ["0001", "0001"],
        "cdProduto": ["1300", "0100"],
        "codCadMu": ["11111", "11111"],
        "Atividade": ["2", "1"],
        "codIbge": ["1100023", "1100023"],
        "VlCusteio": ["1000.0", "500.0"],
        "AreaCusteio": ["10", "5"],
    })


@pytest.fixture
def df_invest_bruto() -> pd.DataFrame:
    """Formato da consulta InvestMunicipioProduto: sem codIbge, só o cadmu."""
    return pd.DataFrame({
        "Municipio": ["ARIQUEMES", "SEM CADMU"],
        "nomeProduto": ['"BOVINOS"', '"BOVINOS"'],
        "MesEmissao": ["01", "01"],
        "AnoEmissao": ["2021", "2021"],
        "cdPrograma": ["0001", "0001"],
        "cdProduto": ["1300", "1300"],
        "cdMunicipio": ["11111", "99999"],   # 99999 não existe no custeio -> descartado
        "Atividade": ["2", "2"],
        "VlInvest": ["2000.0", "300.0"],
        "AreaInvest": ["0", "0"],
    })


@pytest.fixture
def df_base() -> pd.DataFrame:
    """Formato de base_municipio_ano.csv (3 municípios × 2 anos)."""
    return pd.DataFrame({
        "cod_ibge": ["1100015", "1100023", "5100102"] * 2,
        "municipio": ["Alta Floresta D'Oeste", "Ariquemes", "Acorizal"] * 2,
        "uf": ["RO", "RO", "MT"] * 2,
        "ano_prodes": [2020] * 3 + [2021] * 3,
        "incremento_km2": [10.0, 50.0, 0.0, 20.0, 40.0, 0.0],
        "credito_total": [100.0, 900.0, 50.0, 200.0, 800.0, 0.0],
        "credito_custeio": [60.0, 500.0, 50.0, 100.0, 400.0, 0.0],
        "credito_investimento": [40.0, 400.0, 0.0, 100.0, 400.0, 0.0],
        "credito_bovinos": [80.0, 700.0, 0.0, 150.0, 600.0, 0.0],
        "registros": [3, 9, 1, 4, 8, 0],
    })


@pytest.fixture
def df_por_produto() -> pd.DataFrame:
    """Formato de credito_municipio_produto.csv."""
    return pd.DataFrame({
        "cod_ibge": ["1100023", "1100023", "5100102"],
        "uf": ["RO", "RO", "MT"],
        "ano_prodes": [2020, 2020, 2020],
        "finalidade": ["custeio", "investimento", "custeio"],
        "produto": ["BOVINOS", "BOVINOS", "SOJA"],
        "valor": [500.0, 400.0, 50.0],
        "area_ha": [0.0, 0.0, 10.0],
        "registros": [5, 4, 1],
    })
