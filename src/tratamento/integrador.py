"""Junção do crédito rural com o desmatamento por município e ano PRODES.

Migrado do antigo ``preparar_dados.py`` (já testado com os dados reais:
98.615 km² de desmatamento e R$ 498,45 bi de crédito nominal, 2014-2025).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

import config


class IntegradorMunicipal:
    """Monta as bases que o analisador usa.

    Args:
        municipios: Lista oficial dos 772 municípios (coluna ``cod_ibge``).
        prodes: DataFrame bruto do PRODES (colunas ``codibge``, ``municipio``, ``ano_prodes``,
            ``incremento_km2``).
        anos: Anos PRODES mantidos na análise.
    """

    def __init__(self, municipios: pd.DataFrame, prodes: pd.DataFrame,
                 anos: range = config.ANOS_ANALISE) -> None:
        self._municipios = municipios
        self._prodes = prodes.rename(columns={"codibge": "cod_ibge"})
        self._anos = anos

    @staticmethod
    def ler_municipios_oficiais(arquivo: Path = config.ARQUIVO_NOMES_PRODES) -> pd.DataFrame:
        """Lista oficial de municípios do PRODES, só dos 9 estados (772 municípios).

        Necessária porque o Maranhão só tem parte do território na Amazônia Legal:
        sem ela, municípios do leste do MA entrariam com desmatamento zero.
        """
        with open(arquivo, encoding="utf-8") as f:
            lois = json.load(f)["lois"]
        mun = next(l for l in lois if l["name"] == "mun")["loinames"]
        df = pd.DataFrame(mun)[["codibge"]].rename(columns={"codibge": "cod_ibge"})
        df["cod_ibge"] = df["cod_ibge"].astype(str)
        return df[df["cod_ibge"].str[:2].isin(config.UF_AMAZONIA_LEGAL)].drop_duplicates()

    def integrar(self, credito: pd.DataFrame) -> pd.DataFrame:
        """Base município × ano PRODES (perguntas 1, 3 e 4). 772 × 12 = 9.264 linhas."""
        c = credito.assign(
            valor_custeio=credito["valor"].where(credito["finalidade"] == "custeio", 0.0),
            valor_investimento=credito["valor"].where(credito["finalidade"] == "investimento", 0.0),
            valor_bovinos=credito["valor"].where(credito["produto"] == "BOVINOS", 0.0),
        )
        agregado = (c.groupby(["cod_ibge", "ano_prodes"], as_index=False)
                     .agg(credito_total=("valor", "sum"),
                          credito_custeio=("valor_custeio", "sum"),
                          credito_investimento=("valor_investimento", "sum"),
                          credito_bovinos=("valor_bovinos", "sum"),
                          registros=("valor", "size")))

        prodes = self._prodes[["cod_ibge", "ano_prodes", "incremento_km2"]]

        # grade completa: todo município em todo ano, mesmo sem crédito ou sem desmatamento
        grade = self._municipios.merge(pd.DataFrame({"ano_prodes": list(self._anos)}), how="cross")
        base = (grade.merge(agregado, on=["cod_ibge", "ano_prodes"], how="left")
                     .merge(prodes, on=["cod_ibge", "ano_prodes"], how="left"))

        nomes = (pd.concat([self._prodes[["cod_ibge", "municipio"]], credito[["cod_ibge", "municipio"]]])
                 .drop_duplicates("cod_ibge"))
        base = base.merge(nomes, on="cod_ibge", how="left")
        base["uf"] = base["cod_ibge"].str[:2].map(config.UF_AMAZONIA_LEGAL)

        # ausência no PRODES = nenhum desmatamento; ausência no crédito = nenhum crédito
        numericas = ["credito_total", "credito_custeio", "credito_investimento",
                     "credito_bovinos", "registros", "incremento_km2"]
        base[numericas] = base[numericas].fillna(0)
        base["registros"] = base["registros"].astype(int)

        ordem = ["cod_ibge", "municipio", "uf", "ano_prodes", "incremento_km2"] + numericas[:-1]
        return base[ordem].sort_values(["ano_prodes", "cod_ibge"]).reset_index(drop=True)

    def agregar_por_produto(self, credito: pd.DataFrame) -> pd.DataFrame:
        """Crédito por município, ano, finalidade e produto (pergunta 2). ~145 mil linhas."""
        oficiais = set(self._municipios["cod_ibge"])
        c = credito[credito["cod_ibge"].isin(oficiais) & credito["ano_prodes"].isin(self._anos)]
        agregado = (c.groupby(["cod_ibge", "uf", "ano_prodes", "finalidade", "produto"], as_index=False)
                     .agg(valor=("valor", "sum"), area_ha=("area_ha", "sum"),
                          registros=("valor", "size")))
        return agregado.sort_values(["ano_prodes", "cod_ibge", "finalidade", "valor"],
                                    ascending=[True, True, True, False]).reset_index(drop=True)
