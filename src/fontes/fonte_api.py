"""Fonte de dados baseada em API pública que devolve JSON (usada para o IPCA, série SGS 433 do BCB)."""

from __future__ import annotations

from pathlib import Path
from time import time
from typing import Any

import pandas as pd
import requests

from fontes.fonte_dados import FonteDados


class FonteAPI(FonteDados):
    """Consulta uma API HTTP que retorna JSON e converte o resultado em DataFrame.

    Args:
        nome: Nome da fonte.
        url: Endereço do recurso da API..
        descricao: Descrição curta da fonte.
        timeout: Tempo máximo de espera da requisição, em segundos.
        caminho_cache: Se informado, salva/lê uma cópia local em CSV para não
            consultar a API toda vez.
        tentativas: Quantas vezes tentar de novo se a API falhar.
    """

    def __init__(
        self,
        nome: str,
        url: str,
        parametros: dict[str, Any] | None = None,
        descricao: str = "",
        timeout: int = 60,
        caminho_cache: str | Path | None = None,
        tentativas: int = 3,
    ) -> None:
        super().__init__(nome, descricao)
        self._url = url
        self._parametros = parametros or {}
        self._timeout = timeout
        self._caminho_cache = Path(caminho_cache) if caminho_cache else None
        self._tentativas = tentativas

    def carregar(self) -> pd.DataFrame:
        """Usa o cache local se existir; caso contrário, consulta a API."""
        if self._caminho_cache and self._caminho_cache.exists(): return pd.read_csv(self._caminho_cache)
        
        df = pd.DataFrame(self._requisitar())
        if self._caminho_cache: self._salvar_cache(df) 
        return df
        

    def _requisitar(self) -> list[dict[str, Any]]:
        """Faz a requisição HTTP, com novas tentativas e espera crescente."""
        for tentativa in range(1, self._tentativas + 1):
            try:
                resp = requests.get(self._url, params=self._parametros, timeout=self._timeout)
                resp.raise_for_status()
                return resp.json()  
            except requests.RequestException:
                time.sleep(3 * tentativa)
        raise RuntimeError(f"{self.nome}: API indisponível")
       

    def _salvar_cache(self, df: pd.DataFrame) -> None:
        """Salva o DataFrame em CSV no caminho de cache."""
        self._caminho_cache.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(self._caminho_cache, index=False)
        
