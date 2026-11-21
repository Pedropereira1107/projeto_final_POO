"""Fonte de dados baseada em arquivo CSV local (ex.: PRODES/INPE)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from fontes.fonte_dados import FonteDados


class FonteCSV(FonteDados):
    """Carrega dados de um arquivo CSV.

    Args:
        nome: Nome da fonte.
        caminho: Caminho do arquivo CSV.
        descricao: Descrição curta da fonte.
        **opcoes_leitura: Parâmetros repassados ao ``pd.read_csv``
            (ex.: ``sep``, ``encoding``, ``dtype``, ``parse_dates``).
    """

    def __init__(
        self,
        nome: str,
        caminho: str | Path,
        descricao: str = "",
        **opcoes_leitura: Any,
    ) -> None:
        super().__init__(nome, descricao)
        self._caminho = Path(caminho)
        self._opcoes_leitura = opcoes_leitura

    @property
    def caminho(self) -> Path:
        return self._caminho

    def carregar(self) -> pd.DataFrame:
        """Lê o CSV com ``pd.read_csv``."""
        # TODO: verificar se o arquivo existe (self._caminho.exists())
        # TODO: return pd.read_csv(self._caminho, **self._opcoes_leitura)
        raise NotImplementedError
