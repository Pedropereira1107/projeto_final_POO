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

ARQUIVO_PRODES = DIR_DADOS_BRUTOS / "prodes_incremento_municipios_amazonia_legal.csv"
ARQUIVO_SICOR = DIR_DADOS_BRUTOS / "sicor_credito_rural.csv"  # cópia local da API do BCB

# ---------------------------------------------------------------------------
# Domínio do problema
# ---------------------------------------------------------------------------
UFS_AMAZONIA_LEGAL = ("AC", "AM", "AP", "MA", "MT", "PA", "RO", "RR", "TO")

# No PRODES, as linhas de 2007 trazem o desmatamento ACUMULADO histórico
# (inicio_periodo = 1500-08-10), e não o incremento anual.
ANO_PRODES_ACUMULADO = 2007

# ---------------------------------------------------------------------------
# API do Banco Central (SICOR - Matriz de Dados do Crédito Rural)
# ---------------------------------------------------------------------------
SICOR_URL_BASE = "https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata"
SICOR_RECURSO = ""  # TODO: definir o recurso (ex.: crédito por município) no portal do BCB
SICOR_TIMEOUT_SEGUNDOS = 60
