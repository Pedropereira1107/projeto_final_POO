"""Fluxo de preparação dos dados: Fontes -> Tratador -> Integrador -> cache em data/processed.

Substitui o antigo ``preparar_dados.py``. Pode ser executado sozinho:
    python src/pipeline.py            (gera/atualiza o cache)
ou é chamado automaticamente pelo dashboard quando o cache não existe.
"""

from __future__ import annotations

import pandas as pd

import config
from fontes import FonteAPI, FonteCSV
from tratamento import IntegradorMunicipal, TratadorCredito


def criar_fontes() -> dict[str, FonteCSV | FonteAPI]:
    """Instancia todas as fontes do projeto (o resto do código só chama ``obter()``)."""
    return {
        "custeio": FonteCSV("SICOR/BCB - custeio", config.DIR_DADOS_BRUTOS,
                            padrao=config.PADRAO_CUSTEIO, dtype=str),
        "investimento": FonteCSV("SICOR/BCB - investimento", config.DIR_DADOS_BRUTOS,
                                 padrao=config.PADRAO_INVESTIMENTO, dtype=str),
        "prodes": FonteCSV("PRODES/INPE", config.ARQUIVO_PRODES, dtype={"codibge": str}),
        "ipca": FonteAPI("IPCA/BCB (SGS 433)", config.IPCA_URL, config.IPCA_PARAMETROS,
                         timeout=config.TIMEOUT_SEGUNDOS, caminho_cache=config.ARQUIVO_IPCA),
    }


def gerar_bases() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Executa o fluxo completo e salva as duas bases leves em data/processed."""
    fontes = criar_fontes()

    tratador = TratadorCredito(fontes["custeio"].obter(), fontes["investimento"].obter())
    credito = tratador.processar()
    # TODO (etapa 3): credito = TratadorCredito.deflacionar(credito, fontes["ipca"].obter())
    #                 e passar a usar "valor_real" no lugar de "valor" no integrador

    integrador = IntegradorMunicipal(IntegradorMunicipal.ler_municipios_oficiais(),
                                     fontes["prodes"].obter())
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
