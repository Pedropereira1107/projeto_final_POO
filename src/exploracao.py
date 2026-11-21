"""Exploração inicial dos dados brutos (executado no terminal, fora do dashboard).

Executar a partir da raiz do projeto:
    python src/exploracao.py

Objetivo: identificar variáveis e tipos, valores ausentes, duplicidades e
inconsistências. Os achados vão para o README/relatório.
"""

from __future__ import annotations

import pandas as pd

from analise import AnalisadorCreditoDesmatamento
from pipeline import criar_fontes


def explorar(nome: str, df: pd.DataFrame) -> None:
    """Imprime um panorama da base."""
    print(f"\n{'=' * 60}\n{nome}\n{'=' * 60}")
    # TODO: print(df.shape); print(df.head())
    # TODO: print(AnalisadorCreditoDesmatamento.relatorio_qualidade(df))
    # TODO: print(df.describe())
    # TODO: inconsistências: linhas de 2007 no PRODES (acumulado), queda de registros em mar-jun/2016
    raise NotImplementedError


def main() -> None:
    fontes = criar_fontes()
    for chave in ("custeio", "investimento", "prodes"):  # polimorfismo: todas respondem a obter()
        explorar(fontes[chave].nome, fontes[chave].obter())


if __name__ == "__main__":
    main()
