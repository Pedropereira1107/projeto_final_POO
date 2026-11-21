"""Indicadores calculados a partir da base integrada.

Cada indicador é uma subclasse de ``Indicador`` e implementa ``calcular``
(polimorfismo). Para criar um indicador novo, basta criar outra subclasse,
sem alterar as existentes (princípio aberto/fechado).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class Indicador(ABC):
    """Representa um indicador calculado.

    Args:
        nome: Nome exibido no dashboard.
        unidade: Unidade de medida (ex.: "km²", "R$", "%").
        descricao: Explicação curta do que o indicador mede.
    """

    def __init__(self, nome: str, unidade: str, descricao: str = "") -> None:
        self._nome = nome
        self._unidade = unidade
        self._descricao = descricao

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def unidade(self) -> str:
        return self._unidade

    @property
    def descricao(self) -> str:
        return self._descricao

    @abstractmethod
    def calcular(self, df: pd.DataFrame) -> float:
        """Calcula o valor do indicador sobre o DataFrame (já filtrado)."""

    def formatar(self, valor: float) -> str:
        """Formata o valor para exibição (pode ser sobrescrito pelas subclasses)."""
        # TODO: formatar com separador de milhar e a unidade
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self._nome} ({self._unidade})"


class TotalDesmatado(Indicador):
    """Soma da área desmatada no recorte."""

    def __init__(self) -> None:
        super().__init__("Área desmatada", "km²", "Soma do incremento de desmatamento.")

    def calcular(self, df: pd.DataFrame) -> float:
        # TODO: df["incremento_km2"].sum()
        raise NotImplementedError


class TotalCredito(Indicador):
    """Soma do crédito rural concedido no recorte."""

    def __init__(self) -> None:
        super().__init__("Crédito rural", "R$", "Valor total de crédito rural contratado.")

    def calcular(self, df: pd.DataFrame) -> float:
        # TODO: df["valor_credito"].sum()
        raise NotImplementedError


class CreditoPorKm2(Indicador):
    """Crédito rural por km² desmatado."""

    def __init__(self) -> None:
        super().__init__("Crédito por km² desmatado", "R$/km²")

    def calcular(self, df: pd.DataFrame) -> float:
        # TODO: total de crédito / total desmatado (cuidado com divisão por zero)
        raise NotImplementedError


class CorrelacaoCreditoDesmatamento(Indicador):
    """Correlação de Pearson entre crédito e desmatamento por município."""

    def __init__(self) -> None:
        super().__init__("Correlação crédito × desmatamento", "r")

    def calcular(self, df: pd.DataFrame) -> float:
        # TODO: df["valor_credito"].corr(df["incremento_km2"])
        raise NotImplementedError


class VariacaoAnualDesmatamento(Indicador):
    """Variação percentual do desmatamento entre o último e o penúltimo ano do recorte."""

    def __init__(self) -> None:
        super().__init__("Variação anual do desmatamento", "%")

    def calcular(self, df: pd.DataFrame) -> float:
        # TODO: groupby("ano")["incremento_km2"].sum().pct_change().iloc[-1] * 100
        raise NotImplementedError
