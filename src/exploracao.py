"""Etapa 2 - Exploração inicial dos dados (executado no terminal, fora do dashboard).

Executar a partir da raiz do projeto:
    python src/exploracao.py

Objetivo: identificar variáveis e tipos, valores ausentes, duplicidades e
inconsistências antes de definir o tratamento da Etapa 4. Os achados devem
ser registrados em docs/dados.md.
"""

from __future__ import annotations

import pandas as pd

from analise import AnalisadorDados
from app import criar_fontes


def explorar(nome: str, df: pd.DataFrame) -> None:
    """Imprime um panorama da base."""
    print(f"\n{'=' * 60}\n{nome}\n{'=' * 60}")
    # TODO: df.shape, df.head(), df.info(), df.dtypes
    # TODO: AnalisadorDados.relatorio_qualidade(df)
    # TODO: df.describe(); value_counts() de colunas categóricas (ex.: "uf")
    # TODO: inconsistências específicas (ex.: linhas acumuladas de 2007 no PRODES,
    #       valores negativos, UFs fora da Amazônia Legal)
    raise NotImplementedError


def main() -> None:
    for fonte in criar_fontes():  # polimorfismo: CSV e API respondem a obter()
        explorar(fonte.nome, fonte.obter())


if __name__ == "__main__":
    main()
