"""Fixtures compartilhadas: pequenos DataFrames sintéticos para testar as classes."""

import pandas as pd
import pytest


@pytest.fixture
def df_desmatamento() -> pd.DataFrame:
    """Amostra no formato do PRODES (inclui uma linha acumulada de 2007 e um duplicado)."""
    return pd.DataFrame(
        {
            "codibge": ["1100015", "1100015", "1100015", "1100023"],
            "municipio": ["Alta Floresta D'Oeste"] * 3 + ["Ariquemes"],
            "uf": ["RO", "RO", "RO", "RO"],
            "ano_prodes": [2007, 2008, 2008, 2008],
            "inicio_periodo": ["1500-08-10", "2007-08-01", "2007-08-01", "2007-08-01"],
            "fim_periodo": ["2007-07-31", "2008-07-31", "2008-07-31", "2008-07-31"],
            "incremento_km2": [2213.6, 10.5, 10.5, 20.0],
        }
    )


@pytest.fixture
def df_credito() -> pd.DataFrame:
    """Amostra no formato do SICOR. TODO: ajustar colunas ao recurso escolhido da API."""
    return pd.DataFrame(
        {
            "codibge": ["1100015", "1100015"],
            "ano": [2008, 2008],
            "valor": [100_000.0, None],
        }
    )
