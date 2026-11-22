"""Configurações do projeto: caminhos dos arquivos e valores fixos.

Tudo o que é "fixo" fica aqui, num lugar só. Se algo mudar (ex.: o ano final),
muda-se só este arquivo.
"""

from pathlib import Path  # Path representa um caminho de pasta/arquivo no computador

# ---------------------------------------------------------------------------
# Pastas
# ---------------------------------------------------------------------------
RAIZ = Path(__file__).parent.parent             # pasta do projeto (a pasta acima de src/)
PASTA_BRUTOS = RAIZ / "data" / "raw"            # dados originais (nunca são alterados)
PASTA_PROCESSADOS = RAIZ / "data" / "processed"  # dados gerados pelo programa

# ---------------------------------------------------------------------------
# Nomes dos arquivos
# ---------------------------------------------------------------------------
# O * significa "qualquer coisa": pega os 13 arquivos, de 2013 a 2025
ARQUIVOS_CUSTEIO = "mdcr_custeio_*_amazonia_legal.csv"
ARQUIVOS_INVESTIMENTO = "mdcr_investimento_*_amazonia_legal.csv"
ARQUIVO_PRODES = "prodes_incremento_municipios_amazonia_legal.csv"
ARQUIVO_MUNICIPIOS = PASTA_BRUTOS / "prodes_legal_amazon_nomes_bruto.json"

# Arquivos gerados pelo programa (se forem apagados, ele cria de novo)
ARQUIVO_BASE = "base_municipio_ano.csv"           # perguntas 1, 3 e 4
ARQUIVO_PRODUTOS = "credito_municipio_produto.csv"  # pergunta 2
ARQUIVO_IPCA = PASTA_PROCESSADOS / "ipca_mensal.csv"

# ---------------------------------------------------------------------------
# Recorte da análise
# ---------------------------------------------------------------------------
# Os 2 primeiros dígitos do código IBGE dizem o estado (não usar o cdEstado do BCB)
UFS = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA",
    "16": "AP", "17": "TO", "21": "MA", "51": "MT",
}

# Anos PRODES usados: 2013 tem crédito incompleto e 2026 é preliminar
ANO_INICIAL = 2014
ANO_FINAL = 2025

# ---------------------------------------------------------------------------
# IPCA (inflação mensal em %, série 433 do Banco Central)
# ---------------------------------------------------------------------------
# Vai até dez/2025: todos os valores ficam em "reais de dezembro de 2025"
IPCA_URL = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
    "?formato=json&dataInicial=01/01/2013&dataFinal=31/12/2025"
)
