"""Tabelas pequenas e inventadas, no mesmo formato dos dados reais, para usar nos testes.

Cada função com @pytest.fixture vira um "ingrediente": um teste que tem um parâmetro
com o mesmo nome recebe a tabela pronta.
"""

import pandas as pd
import pytest


@pytest.fixture
def custeio():
    """Igual ao arquivo de custeio do BCB (tudo texto)."""
    return pd.DataFrame({
        "Municipio": ["ARIQUEMES", "ARIQUEMES"],
        "nomeProduto": ['"BOVINOS"', '"CAFÉ"'],       # o BCB manda o nome com aspas
        "MesEmissao": ["07", "08"],                   # julho -> PRODES 2020; agosto -> PRODES 2021
        "AnoEmissao": ["2020", "2020"],
        "codCadMu": ["11111", "11111"],
        "codIbge": ["1100023", "1100023"],
        "VlCusteio": ["1000.0", "500.0"],
    })


@pytest.fixture
def investimento():
    """Igual ao arquivo de investimento do BCB: não tem codIbge, só o cadmu."""
    return pd.DataFrame({
        "Municipio": ["ARIQUEMES", "SEM CADMU"],
        "nomeProduto": ['"BOVINOS"', '"BOVINOS"'],
        "MesEmissao": ["01", "01"],
        "AnoEmissao": ["2021", "2021"],
        "cdMunicipio": ["11111", "99999"],            # 99999 não existe no custeio -> descartado
        "VlInvest": ["2000.0", "300.0"],
    })


@pytest.fixture
def ipca_zero():
    """IPCA com inflação zero: os valores não mudam (facilita conferir as somas)."""
    return pd.DataFrame({
        "data": ["01/07/2020", "01/08/2020", "01/01/2021"],
        "valor": ["0", "0", "0"],
    })


@pytest.fixture
def base():
    """Igual a base_municipio_ano.csv: 3 municípios x 2 anos."""
    return pd.DataFrame({
        "cod_ibge": ["1100015", "1100023", "5100102"] * 2,
        "municipio": ["Alta Floresta D'Oeste", "Ariquemes", "Acorizal"] * 2,
        "uf": ["RO", "RO", "MT"] * 2,
        "ano_prodes": [2020, 2020, 2020, 2021, 2021, 2021],
        "incremento_km2": [10.0, 50.0, 0.0, 20.0, 40.0, 0.0],
        "credito_total": [100.0, 900.0, 50.0, 200.0, 800.0, 0.0],
        "credito_custeio": [60.0, 500.0, 50.0, 100.0, 400.0, 0.0],
        "credito_investimento": [40.0, 400.0, 0.0, 100.0, 400.0, 0.0],
        "credito_bovinos": [80.0, 700.0, 0.0, 150.0, 600.0, 0.0],
        "registros": [3, 9, 1, 4, 8, 0],
    })


@pytest.fixture
def produtos():
    """Igual a credito_municipio_produto.csv."""
    return pd.DataFrame({
        "cod_ibge": ["1100023", "1100023", "5100102"],
        "uf": ["RO", "RO", "MT"],
        "ano_prodes": [2020, 2020, 2020],
        "finalidade": ["custeio", "investimento", "custeio"],
        "produto": ["BOVINOS", "BOVINOS", "SOJA"],
        "valor": [500.0, 400.0, 50.0],
    })
