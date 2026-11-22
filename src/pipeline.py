"""Fluxo de preparação dos dados: preparar_dados (Tratador + Integrador) -> cache em data/processed"""

from __future__ import annotations

import pandas as pd

import config
from fontes import FonteAPI, FonteCSV
from preparar_dados import IntegradorMunicipal, TratadorCredito


def criar_fontes() -> dict[str, FonteCSV | FonteAPI]:
    """Instancia as fontes do projeto (usadas na exploração e na correção pelo IPCA)."""
    return {
        "custeio": FonteCSV("SICOR/BCB - custeio", config.DIR_DADOS_BRUTOS,
                            padrao=config.PADRAO_CUSTEIO, dtype=str),
        "investimento": FonteCSV("SICOR/BCB - investimento", config.DIR_DADOS_BRUTOS,
                                 padrao=config.PADRAO_INVESTIMENTO, dtype=str),
        "prodes": FonteCSV("PRODES/INPE", config.ARQUIVO_PRODES, dtype={"codibge": str}),
        "ipca": FonteAPI("IPCA/BCB (SGS 433)", config.IPCA_URL, config.IPCA_PARAMETROS,
                         timeout=config.TIMEOUT_SEGUNDOS, caminho_cache=config.ARQUIVO_IPCA),
    }


def deflacionar(credito: pd.DataFrame, ipca: pd.DataFrame,
                mes_referencia: str = config.IPCA_MES_REFERENCIA) -> pd.DataFrame:
    """Adiciona a coluna ``valor_real`` (R$ do mês de referência).

    Args:
        credito: Saída de ``TratadorCredito.processar()`` (precisa de ``ano``, ``mes`` e ``valor``).
        ipca: Saída da FonteAPI do IPCA (colunas ``data`` "dd/mm/aaaa" e ``valor`` em %).
        mes_referencia: Mês-base no formato "AAAA-MM".
    """
    ipca = ipca.copy()
    ipca["mes_ref"] = pd.to_datetime(ipca["data"], dayfirst=True).dt.strftime("%Y-%m")
    
    ipca["indice"] = (1 + ipca["valor"].astype(float) / 100).cumprod()   
    
    indice_ref = ipca.loc[ipca["mes_ref"] == mes_referencia, "indice"].iloc[0]
    
    ipca["fator"] = indice_ref / ipca["indice"]

    credito = credito.copy()
    credito["mes_ref"] = credito["ano"].astype(str) + "-" + credito["mes"].astype(str).str.zfill(2)
    
    credito = credito.merge(ipca[["mes_ref", "fator"]], on="mes_ref", how="left")
    
    credito["valor_real"] = credito["valor"] * credito["fator"]
    
    return credito
    


def gerar_bases() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Executa o tratamento do preparar_dados e salva as duas bases leves em data/processed."""
    credito = TratadorCredito(config.DIR_DADOS_BRUTOS).processar()
    credito = deflacionar(credito, criar_fontes()["ipca"].obter())
    credito["valor"] = credito["valor_real"]

    integrador = IntegradorMunicipal(config.DIR_DADOS_BRUTOS)
    base = integrador.integrar(credito)
    por_produto = integrador.agregar_por_produto(credito)

    config.DIR_DADOS_PROCESSADOS.mkdir(parents=True, exist_ok=True)
    base.to_csv(config.ARQUIVO_BASE, index=False)
    por_produto.to_csv(config.ARQUIVO_POR_PRODUTO, index=False)
    return base, por_produto


def carregar_bases() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Lê o cache; se ele não existir, gera as bases primeiro."""
    if not (config.ARQUIVO_BASE.exists() and config.ARQUIVO_POR_PRODUTO.exists()):
        return gerar_bases()
    base = FonteCSV("Base município × ano", config.ARQUIVO_BASE, dtype={"cod_ibge": str}).obter()
    por_produto = FonteCSV("Crédito por produto", config.ARQUIVO_POR_PRODUTO,
                           dtype={"cod_ibge": str}).obter()
    return base, por_produto


if __name__ == "__main__":
    base, por_produto = gerar_bases()
    print(f"base_municipio_ano: {len(base):,} linhas | credito_municipio_produto: {len(por_produto):,} linhas")
