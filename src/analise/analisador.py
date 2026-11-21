"""Processamento e análise dos dados com Pandas."""

from __future__ import annotations

from typing import Iterable

import pandas as pd


class AnalisadorDados:
    """Realiza a limpeza, integração e as análises das bases.

    Recebe os DataFrames já carregados (não sabe de onde vieram: inversão de
    dependência) e produz uma base integrada município × ano com desmatamento
    e crédito rural.

    Args:
        desmatamento: DataFrame do PRODES/INPE.
        credito: DataFrame do SICOR/BCB.
    """

    def __init__(self, desmatamento: pd.DataFrame, credito: pd.DataFrame) -> None:
        self._desmatamento = desmatamento.copy()
        self._credito = credito.copy()
        self.__dados: pd.DataFrame | None = None  # base integrada (privada)

    @property
    def dados(self) -> pd.DataFrame:
        """Base integrada. Só fica disponível depois de ``integrar()``."""
        if self.__dados is None:
            raise RuntimeError("Execute integrar() antes de acessar os dados.")
        return self.__dados

    # ------------------------------------------------------------------ #
    # Etapa 2 - Exploração
    # ------------------------------------------------------------------ #
    @staticmethod
    def relatorio_qualidade(df: pd.DataFrame) -> dict:
        """Resumo de qualidade: tipos, ausentes, duplicados e linhas/colunas."""
        # TODO: df.shape, df.dtypes, df.isna().sum(), df.duplicated().sum()
        raise NotImplementedError

    # ------------------------------------------------------------------ #
    # Etapa 4 - Tratamento
    # ------------------------------------------------------------------ #
    def limpar_desmatamento(self) -> pd.DataFrame:
        """Trata a base do PRODES."""
        # TODO: remover linhas do ano acumulado (config.ANO_PRODES_ACUMULADO)
        # TODO: drop_duplicates(subset=["codibge", "ano_prodes"])
        # TODO: converter tipos (codibge -> str, incremento_km2 -> float)
        # TODO: renomear ano_prodes -> ano
        raise NotImplementedError

    def limpar_credito(self) -> pd.DataFrame:
        """Trata a base do SICOR."""
        # TODO: selecionar colunas relevantes; padronizar nomes (codibge, ano, valor)
        # TODO: pd.to_numeric(..., errors="coerce"); tratar ausentes
        # TODO: filtrar apenas UFs da Amazônia Legal (config.UFS_AMAZONIA_LEGAL)
        # TODO: groupby(["codibge", "ano"]).agg(...) para somar contratos
        raise NotImplementedError

    def integrar(self) -> pd.DataFrame:
        """Limpa as duas bases e faz o merge por município e ano."""
        # TODO: pd.merge(desmat, credito, on=["codibge", "ano"], how="left")
        # TODO: preencher crédito ausente com 0 (município sem crédito no ano)
        # TODO: guardar em self.__dados e retornar
        raise NotImplementedError

    # ------------------------------------------------------------------ #
    # Etapa 4 - Análise
    # ------------------------------------------------------------------ #
    def filtrar(
        self,
        ufs: Iterable[str] | None = None,
        ano_inicial: int | None = None,
        ano_final: int | None = None,
    ) -> pd.DataFrame:
        """Seleciona registros por UF e intervalo de anos (usado pelos filtros do dashboard)."""
        # TODO: máscara booleana com .isin() e .between()
        raise NotImplementedError

    def agrupar(self, df: pd.DataFrame, por: str | list[str]) -> pd.DataFrame:
        """Agrupa somando desmatamento e crédito (ex.: por "uf" ou por "ano")."""
        # TODO: df.groupby(por, as_index=False).agg(...)
        raise NotImplementedError

    def ranking(self, df: pd.DataFrame, coluna: str, n: int = 10) -> pd.DataFrame:
        """Top-N municípios por uma coluna, em ordem decrescente."""
        # TODO: agrupar por município e usar sort_values / nlargest
        raise NotImplementedError

    def estatisticas_descritivas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Média, mediana, desvio-padrão, quartis etc. das colunas numéricas."""
        # TODO: df.describe() (+ median, se quiser)
        raise NotImplementedError

    def adicionar_defasagem_credito(self, df: pd.DataFrame, anos: int = 1) -> pd.DataFrame:
        """Cria coluna com o crédito do(s) ano(s) anterior(es) para cada município."""
        # TODO: ordenar por codibge/ano e usar groupby("codibge")["valor_credito"].shift(anos)
        raise NotImplementedError
