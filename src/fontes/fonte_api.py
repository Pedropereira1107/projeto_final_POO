"""Fonte de dados baseada em API pública (ex.: SICOR/BCB via OData)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from fontes.fonte_dados import FonteDados


class FonteAPI(FonteDados):
    """Consulta uma API HTTP que retorna JSON e converte o resultado em DataFrame.

    Args:
        nome: Nome da fonte.
        url: Endereço do recurso da API.
        parametros: Parâmetros da consulta (ex.: ``$format``, ``$filter``, ``$top``).
        descricao: Descrição curta da fonte.
        timeout: Tempo máximo de espera da requisição, em segundos.
        caminho_cache: Se informado, salva/lê uma cópia local em CSV para não
            consultar a API toda vez.
    """

    def __init__(
        self,
        nome: str,
        url: str,
        parametros: dict[str, Any] | None = None,
        descricao: str = "",
        timeout: int = 60,
        caminho_cache: str | Path | None = None,
    ) -> None:
        super().__init__(nome, descricao)
        self._url = url
        self._parametros = parametros or {}
        self._timeout = timeout
        self._caminho_cache = Path(caminho_cache) if caminho_cache else None

    def carregar(self) -> pd.DataFrame:
        """Usa o cache local se existir; caso contrário, consulta a API."""
        # TODO: se o cache existir, ler com pd.read_csv
        # TODO: senão, dados = self._requisitar(); df = pd.DataFrame(dados)
        # TODO: salvar o cache com self._salvar_cache(df)
        raise NotImplementedError

    # ------------------------------------------------------------------ #
    # Métodos privados (detalhes de implementação)
    # ------------------------------------------------------------------ #
    def _requisitar(self) -> list[dict[str, Any]]:
        """Faz a requisição HTTP e devolve a lista de registros (chave ``value`` no OData)."""
        # TODO: requests.get(self._url, params=self._parametros, timeout=self._timeout)
        # TODO: resp.raise_for_status(); return resp.json()["value"]
        # TODO (opcional): paginação com $skip, se houver mais registros que o $top
        raise NotImplementedError

    def _salvar_cache(self, df: pd.DataFrame) -> None:
        """Salva o DataFrame em CSV no caminho de cache."""
        # TODO: df.to_csv(self._caminho_cache, index=False)
        raise NotImplementedError
