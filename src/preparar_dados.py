"""
Junta e padroniza os dados brutos do projeto.

Entrada (em data/, em qualquer subpasta):
  - mdcr_custeio_AAAA_amazonia_legal.csv        (13 arquivos)
  - mdcr_investimento_AAAA_amazonia_legal.csv   (13 arquivos)
  - prodes_incremento_municipios_amazonia_legal.csv

Saída (em data/processed/):
  - credito_rural_amazonia_legal.csv   -> todas as operações, custeio + investimento (etapa intermediária)
  - base_municipio_ano.csv             -> crédito por município e ano PRODES + desmatamento (perguntas 1, 3, 4)
  - credito_municipio_produto.csv      -> crédito por município, ano PRODES, finalidade e produto (pergunta 2)

Uso:  python preparar_dados.py            (procura os arquivos em ./data)
      python preparar_dados.py caminho/para/data
"""
import sys
from pathlib import Path

import pandas as pd

# Códigos IBGE (2 primeiros dígitos) dos 9 estados da Amazônia Legal
UF_AMAZONIA_LEGAL = {"11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA",
                     "16": "AP", "17": "TO", "21": "MA", "51": "MT"}


class TratadorCredito:
    """Lê os 26 CSVs da MDCR, padroniza as colunas e junta tudo em uma tabela só."""

    # nomes diferentes nas duas consultas da API -> nome único
    RENOMEAR = {
        "VlCusteio": "valor", "VlInvest": "valor",
        "AreaCusteio": "area_ha", "AreaInvest": "area_ha",
        "codCadMu": "cod_cadmu", "cdMunicipio": "cod_cadmu",
        "codIbge": "cod_ibge",
    }

    def __init__(self, pasta_dados: Path):
        self.pasta = pasta_dados

    def _ler(self, finalidade: str) -> pd.DataFrame:
        arquivos = sorted(self.pasta.rglob(f"mdcr_{finalidade}_*_amazonia_legal.csv"))
        if not arquivos:
            raise FileNotFoundError(f"Nenhum arquivo mdcr_{finalidade}_*.csv em {self.pasta}")
        # dtype=str preserva zeros à esquerda dos códigos (ex.: MesEmissao '01')
        df = pd.concat((pd.read_csv(a, dtype=str) for a in arquivos), ignore_index=True)
        df = df.rename(columns=self.RENOMEAR)
        df["finalidade"] = finalidade
        print(f"  {finalidade}: {len(arquivos)} arquivos, {len(df):,} linhas")
        return df

    def processar(self) -> pd.DataFrame:
        custeio = self._ler("custeio")
        invest = self._ler("investimento")

        # A consulta de investimento não traz o código IBGE, só o cadmu.
        # A de custeio traz os dois: usamos ela como tabela de correspondência.
        mapa = custeio[["cod_cadmu", "cod_ibge"]].dropna().drop_duplicates("cod_cadmu")
        invest = invest.drop(columns="cod_ibge", errors="ignore").merge(mapa, on="cod_cadmu", how="left")
        sem_ibge = invest["cod_ibge"].isna()
        if sem_ibge.any():
            print(f"  aviso: {sem_ibge.sum():,} linhas de investimento sem código IBGE "
                  f"({invest.loc[sem_ibge, 'valor'].astype(float).sum() / 1e6:,.1f} mi R$) foram descartadas")
            invest = invest[~sem_ibge]

        df = pd.concat([custeio, invest], ignore_index=True)

        # tipos e limpeza
        df["valor"] = df["valor"].astype(float)
        df["area_ha"] = df["area_ha"].astype(float)
        df["ano"] = df["AnoEmissao"].astype(int)
        df["mes"] = df["MesEmissao"].astype(int)
        df["produto"] = df["nomeProduto"].str.strip().str.strip('"').str.strip()
        df["uf"] = df["cod_ibge"].str[:2].map(UF_AMAZONIA_LEGAL)
        # ano PRODES vai de agosto a julho: ago/2020 a jul/2021 = PRODES 2021
        df["ano_prodes"] = df["ano"] + (df["mes"] >= 8).astype(int)

        colunas = ["finalidade", "ano", "mes", "ano_prodes", "uf", "cod_ibge", "cod_cadmu",
                   "Municipio", "produto", "cdProduto", "Atividade", "cdPrograma",
                   "cdSubPrograma", "cdFonteRecurso", "cdModalidade", "valor", "area_ha"]
        return df[colunas].rename(columns={"Municipio": "municipio", "cdProduto": "cod_produto",
                                           "Atividade": "atividade", "cdPrograma": "cod_programa",
                                           "cdSubPrograma": "cod_subprograma",
                                           "cdFonteRecurso": "cod_fonte_recurso",
                                           "cdModalidade": "cod_modalidade"})


class IntegradorMunicipal:
    """Agrega o crédito por município e ano PRODES e junta com o desmatamento."""

    ANOS = range(2014, 2026)  # anos PRODES com crédito e desmatamento completos

    def __init__(self, pasta_dados: Path):
        self.pasta = pasta_dados

    def municipios_amazonia_legal(self) -> pd.DataFrame:
        """Lista oficial de municípios usada pelo PRODES, só dos 9 estados (772 municípios).

        Vem do arquivo prodes_legal_amazon_nomes_bruto.json. Ela é necessária porque o
        Maranhão só tem parte do território na Amazônia Legal: sem a lista, municípios do
        leste do MA entrariam na análise com desmatamento zero."""
        arquivo = next(self.pasta.rglob("prodes_legal_amazon_nomes_bruto.json"))
        lois = pd.read_json(arquivo, typ="series")["lois"]
        mun = next(l for l in lois if l["name"] == "mun")["loinames"]
        df = pd.DataFrame(mun)[["codibge"]].rename(columns={"codibge": "cod_ibge"})
        df["cod_ibge"] = df["cod_ibge"].astype(str)
        return df[df["cod_ibge"].str[:2].isin(UF_AMAZONIA_LEGAL)].drop_duplicates()

    def _ler_prodes(self) -> pd.DataFrame:
        arquivo = next(self.pasta.rglob("prodes_incremento_municipios_amazonia_legal.csv"))
        prodes = pd.read_csv(arquivo, dtype={"codibge": str})
        return prodes.rename(columns={"codibge": "cod_ibge"})

    def integrar(self, credito: pd.DataFrame) -> pd.DataFrame:
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

        prodes = self._ler_prodes()[["cod_ibge", "ano_prodes", "incremento_km2"]]

        # grade completa: todo município da Amazônia Legal em todo ano, mesmo sem crédito
        # ou sem desmatamento (anos PRODES 2014-2025; 2013 só tem jan-jul de crédito e
        # 2026 só tem ago-dez de 2025, com PRODES preliminar)
        municipios = self.municipios_amazonia_legal()
        grade = municipios.merge(pd.DataFrame({"ano_prodes": list(self.ANOS)}), how="cross")
        base = (grade.merge(agregado, on=["cod_ibge", "ano_prodes"], how="left")
                     .merge(prodes, on=["cod_ibge", "ano_prodes"], how="left"))

        nomes = (pd.concat([self._ler_prodes()[["cod_ibge", "municipio"]],
                            credito[["cod_ibge", "municipio"]]])
                 .drop_duplicates("cod_ibge"))
        base = base.merge(nomes, on="cod_ibge", how="left")
        base["uf"] = base["cod_ibge"].str[:2].map(UF_AMAZONIA_LEGAL)

        # ausência no PRODES = nenhum desmatamento detectado; ausência no crédito = nenhum crédito
        numericas = ["credito_total", "credito_custeio", "credito_investimento",
                     "credito_bovinos", "registros", "incremento_km2"]
        base[numericas] = base[numericas].fillna(0)
        base["registros"] = base["registros"].astype(int)

        ordem = ["cod_ibge", "municipio", "uf", "ano_prodes", "incremento_km2"] + numericas[:-1]
        return base[ordem].sort_values(["ano_prodes", "cod_ibge"]).reset_index(drop=True)

    def agregar_por_produto(self, credito: pd.DataFrame) -> pd.DataFrame:
        """Crédito por município, ano PRODES, finalidade e produto (pergunta 2).

        Versão leve do arquivo de crédito (~145 mil linhas) para o analisador e o
        dashboard, que não precisam ler o milhão de operações a cada interação."""
        oficiais = set(self.municipios_amazonia_legal()["cod_ibge"])
        c = credito[credito["cod_ibge"].isin(oficiais) & credito["ano_prodes"].isin(self.ANOS)]
        agregado = (c.groupby(["cod_ibge", "uf", "ano_prodes", "finalidade", "produto"], as_index=False)
                     .agg(valor=("valor", "sum"), area_ha=("area_ha", "sum"),
                          registros=("valor", "size")))
        return agregado.sort_values(["ano_prodes", "cod_ibge", "finalidade", "valor"],
                                    ascending=[True, True, True, False]).reset_index(drop=True)


def main():
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data")
    saida = pasta / "processed"
    saida.mkdir(parents=True, exist_ok=True)

    print("Lendo crédito rural...")
    credito = TratadorCredito(pasta).processar()
    integrador = IntegradorMunicipal(pasta)

    # marca as operações de municípios fora da Amazônia Legal (leste do Maranhão)
    oficiais = set(integrador.municipios_amazonia_legal()["cod_ibge"])
    credito["amazonia_legal"] = credito["cod_ibge"].isin(oficiais)
    credito.to_csv(saida / "credito_rural_amazonia_legal.csv", index=False)
    print(f"  -> {saida / 'credito_rural_amazonia_legal.csv'} ({len(credito):,} linhas, "
          f"{(~credito['amazonia_legal']).sum():,} fora da Amazônia Legal)")

    print("Integrando com o PRODES...")
    base = integrador.integrar(credito)
    base.to_csv(saida / "base_municipio_ano.csv", index=False)
    print(f"  -> {saida / 'base_municipio_ano.csv'} ({len(base):,} linhas, "
          f"{base['cod_ibge'].nunique()} municípios)")

    print("Agregando crédito por produto...")
    por_produto = integrador.agregar_por_produto(credito)
    por_produto.to_csv(saida / "credito_municipio_produto.csv", index=False)
    print(f"  -> {saida / 'credito_municipio_produto.csv'} ({len(por_produto):,} linhas)")


if __name__ == "__main__":
    main()
