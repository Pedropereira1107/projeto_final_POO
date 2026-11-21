"""Configurações centrais do projeto: caminhos, constantes e parâmetros das fontes.

Centralizar as constantes aqui evita "números mágicos" espalhados pelo código
e facilita a manutenção (princípio da responsabilidade única).
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
DIR_DADOS_BRUTOS = RAIZ_PROJETO / "data" / "raw"
DIR_DADOS_PROCESSADOS = RAIZ_PROJETO / "data" / "processed"

# Brutos (nunca são alterados)
ARQUIVO_PRODES = DIR_DADOS_BRUTOS / "prodes_incremento_municipios_amazonia_legal.csv"
ARQUIVO_NOMES_PRODES = DIR_DADOS_BRUTOS / "prodes_legal_amazon_nomes_bruto.json"
PADRAO_CUSTEIO = "mdcr_custeio_*_amazonia_legal.csv"            # 13 arquivos (2013-2025)
PADRAO_INVESTIMENTO = "mdcr_investimento_*_amazonia_legal.csv"  # 13 arquivos (2013-2025)

# Processados (cache gerado pelo pipeline; podem ser apagados e recriados)
ARQUIVO_BASE = DIR_DADOS_PROCESSADOS / "base_municipio_ano.csv"
ARQUIVO_POR_PRODUTO = DIR_DADOS_PROCESSADOS / "credito_municipio_produto.csv"
ARQUIVO_IPCA = DIR_DADOS_PROCESSADOS / "ipca_mensal.csv"

# ---------------------------------------------------------------------------
# Domínio do problema
# ---------------------------------------------------------------------------
# 2 primeiros dígitos do código IBGE -> sigla da UF (NÃO usar o cdEstado do BCB)
UF_AMAZONIA_LEGAL = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA",
    "16": "AP", "17": "TO", "21": "MA", "51": "MT",
}

# Anos PRODES com crédito e desmatamento completos.
# 2013 só tem jan-jul de crédito; 2026 é preliminar no PRODES.
ANOS_ANALISE = range(2014, 2026)

# Município crítico = top 10% em desmatamento acumulado no período
PERCENTIL_CRITICO = 0.90

# ---------------------------------------------------------------------------
# IPCA (série SGS 433 do BCB, variação mensal em %)
# ---------------------------------------------------------------------------
IPCA_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
IPCA_PARAMETROS = {"formato": "json", "dataInicial": "01/01/2013", "dataFinal": "31/12/2025"}
IPCA_MES_REFERENCIA = "2025-12"  # valores em R$ de dez/2025
TIMEOUT_SEGUNDOS = 60
