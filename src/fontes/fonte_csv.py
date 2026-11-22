"""Fonte de dados baseada nos arquivos CSV do PRODES/INPE e do SICOR/BCB"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from fontes.fonte_dados import FonteDados


class FonteCSV(FonteDados):
    """Carrega dados de um CSV ou de vários CSVs com o mesmo formato."""

    def __init__(
        self,
        nome: str,
        caminho: str | Path,
        descricao: str = "",
        padrao: str | None = None,
        **opcoes_leitura: Any,
    ) -> None:
        super().__init__(nome, descricao)
        self._caminho = Path(caminho)
        self._padrao = padrao
        self._opcoes_leitura = opcoes_leitura

    @property
    def caminho(self) -> Path:
        return self._caminho

    def carregar(self) -> pd.DataFrame:
        """Lê os CSV's com pd.read_csv."""
        arquivos = self._listar_arquivos()
        if not arquivos:
            raise FileNotFoundError(f"{self.nome}: nenhum arquivo em {self._caminho}")
        

    def _listar_arquivos(self) -> list[Path]:
        """Um arquivo só, ou todos os que casam com o padrão, em ordem."""
        if self._padrao:
            return sorted(self._caminho.glob(self.padrao))
        raise NotImplementedError
