"""Limpeza e padronização do crédito rural (MDCR/SICOR).

Migrado do antigo ``preparar_dados.py`` (já testado com os dados reais).
A classe não lê arquivos: recebe os DataFrames prontos das fontes (inversão de dependência).
"""

from __future__ import annotations

import pandas as pd

import config


class TratadorCredito:
    """Junta custeio + investimento em uma tabela única e padronizada.

    Args:
        custeio: DataFrame bruto da consulta ``CusteioMunicipioProduto`` (lido com ``dtype=str``).
        investimento: DataFrame bruto da consulta ``InvestMunicipioProduto`` (lido com ``dtype=str``).
    """

    # nomes diferentes nas duas consultas da API -> nome único
    RENOMEAR = {
        "VlCusteio": "valor", "VlInvest": "valor",
        "AreaCusteio": "area_ha", "AreaInvest": "area_ha",
        "codCadMu": "cod_cadmu", "cdMunicipio": "cod_cadmu",
        "codIbge": "cod_ibge",
    }

    COLUNAS_FINAIS = {
        "finalidade": "finalidade", "ano": "ano", "mes": "mes", "ano_prodes": "ano_prodes",
        "uf": "uf", "cod_ibge": "cod_ibge", "cod_cadmu": "cod_cadmu", "Municipio": "municipio",
        "produto": "produto", "cdProduto": "cod_produto", "Atividade": "atividade",
        "cdPrograma": "cod_programa", "valor": "valor", "area_ha": "area_ha",
    }

    def __init__(self, custeio: pd.DataFrame, investimento: pd.DataFrame) -> None:
        self._custeio = custeio
        self._investimento = investimento
        self.linhas_descartadas = 0  # investimento sem correspondência cadmu -> IBGE

    def processar(self) -> pd.DataFrame:
        """Executa todo o tratamento e devolve uma linha por operação."""
        custeio = self._padronizar(self._custeio, "custeio")
        invest = self._preencher_ibge(self._padronizar(self._investimento, "investimento"), custeio)
        df = pd.concat([custeio, invest], ignore_index=True)
        df = self._converter_tipos(df)
        return df[list(self.COLUNAS_FINAIS)].rename(columns=self.COLUNAS_FINAIS)

    # ------------------------------------------------------------------ #
    # Etapas do tratamento
    # ------------------------------------------------------------------ #
    def _padronizar(self, df: pd.DataFrame, finalidade: str) -> pd.DataFrame:
        return df.rename(columns=self.RENOMEAR).assign(finalidade=finalidade)

    def _preencher_ibge(self, invest: pd.DataFrame, custeio: pd.DataFrame) -> pd.DataFrame:
        """A consulta de investimento não traz o código IBGE: usa o custeio como tabela cadmu -> IBGE."""
        mapa = custeio[["cod_cadmu", "cod_ibge"]].dropna().drop_duplicates("cod_cadmu")
        invest = invest.drop(columns="cod_ibge", errors="ignore").merge(mapa, on="cod_cadmu", how="left")
        sem_ibge = invest["cod_ibge"].isna()
        self.linhas_descartadas = int(sem_ibge.sum())
        return invest[~sem_ibge]

    @staticmethod
    def _converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["valor"] = df["valor"].astype(float)
        df["area_ha"] = df["area_ha"].astype(float)
        df["ano"] = df["AnoEmissao"].astype(int)
        df["mes"] = df["MesEmissao"].astype(int)
        df["produto"] = df["nomeProduto"].str.strip().str.strip('"').str.strip()
        df["uf"] = df["cod_ibge"].str[:2].map(config.UF_AMAZONIA_LEGAL)
        # ano PRODES vai de agosto a julho: ago/2020 a jul/2021 = PRODES 2021
        df["ano_prodes"] = df["ano"] + (df["mes"] >= 8).astype(int)
        return df

    # ------------------------------------------------------------------ #
    # Correção pela inflação (etapa 3 do plano)
    # ------------------------------------------------------------------ #
    @staticmethod
    def deflacionar(credito: pd.DataFrame, ipca: pd.DataFrame,
                    mes_referencia: str = config.IPCA_MES_REFERENCIA) -> pd.DataFrame:
        """Adiciona a coluna ``valor_real`` (R$ do mês de referência).

        Args:
            credito: Saída de ``processar()`` (precisa de ``ano``, ``mes`` e ``valor``).
            ipca: Saída da FonteAPI do IPCA (colunas ``data`` "dd/mm/aaaa" e ``valor`` em %).
            mes_referencia: Mês-base no formato "AAAA-MM".
        """
        # TODO: ipca["mes_ref"] = pd.to_datetime(ipca["data"], dayfirst=True).dt.strftime("%Y-%m")
        # TODO: ipca["indice"] = (1 + ipca["valor"].astype(float) / 100).cumprod()
        # TODO: fator = indice[mes_referencia] / indice[mês do contrato]
        # TODO: credito["mes_ref"] = credito["ano"].astype(str) + "-" + credito["mes"].astype(str).str.zfill(2)
        # TODO: merge pelo mes_ref e credito["valor_real"] = credito["valor"] * fator
        raise NotImplementedError
