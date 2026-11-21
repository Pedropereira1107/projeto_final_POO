"""Fonte de dados baseada em arquivo(s) CSV local(is) (PRODES/INPE e cópia local do SICOR/BCB)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from fontes.fonte_dados import FonteDados


class FonteCSV(FonteDados):
    """Carrega dados de um CSV ou de vários CSVs com o mesmo formato.

    Exemplos:
        FonteCSV("PRODES", caminho=config.ARQUIVO_PRODES)               # um arquivo
        FonteCSV("SICOR custeio", caminho=config.DIR_DADOS_BRUTOS,
                 padrao="mdcr_custeio_*_amazonia_legal.csv")             # 13 arquivos juntos

    Args:
        nome: Nome da fonte.
        caminho: Caminho do arquivo CSV, ou da pasta (quando ``padrao`` é usado).
        descricao: Descrição curta da fonte.
        padrao: Padrão glob dos arquivos dentro da pasta (ex.: ``"mdcr_custeio_*.csv"``).
        **opcoes_leitura: Parâmetros repassados ao ``pd.read_csv``
            (ex.: ``sep``, ``encoding``, ``dtype``).
    """

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
        """Lê o(s) CSV(s) com ``pd.read_csv``."""
        # TODO: arquivos = self._listar_arquivos()
        # TODO: se a lista estiver vazia -> raise FileNotFoundError(...)
        # TODO: return pd.concat((pd.read_csv(a, **self._opcoes_leitura) for a in arquivos),
        #                        ignore_index=True)
        raise NotImplementedError

    def _listar_arquivos(self) -> list[Path]:
        """Um arquivo só, ou todos os que casam com o padrão, em ordem."""
        # TODO: se self._padrao: return sorted(self._caminho.glob(self._padrao))
        # TODO: senão: return [self._caminho] se ele existir, ou [] se não existir
        raise NotImplementedError
