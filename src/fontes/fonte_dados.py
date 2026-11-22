"""Classe abstrata base para qualquer origem de dados."""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class FonteDados(ABC):
    """Gerencia a origem dos dados.

    Classe abstrata: define o contrato que toda fonte deve cumprir
    (o método ''carregar''). As subclasses ''FonteCSV`` e ''FonteAPI''
    implementam esse contrato de formas diferentes (herança + polimorfismo).

    Attributes:
        _nome: Nome da fonte .
        _descricao: Descrição curta da fonte.
        _dados: Cache do DataFrame carregado (encapsulado).
    """

    def __init__(self, nome: str, descricao: str = "") -> None:
        self._nome = nome
        self._descricao = descricao
        self._dados: pd.DataFrame | None = None

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def descricao(self) -> str:
        return self._descricao

    def obter(self) -> pd.DataFrame:
        """Retorna os dados, carregando-os apenas na primeira chamada (cache)."""
        if self._dados is None:
            self._dados = self.carregar()
        return self._dados

    @abstractmethod
    def carregar(self) -> pd.DataFrame:
        """Lê os dados da origem e devolve um DataFrame. Implementado pelas subclasses."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nome={self._nome})"
