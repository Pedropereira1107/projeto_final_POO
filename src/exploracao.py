"""Exploração dos dados brutos: um raio-x das tabelas antes do tratamento.

Executar na raiz do projeto:
    python src/exploracao.py
"""

import config
from fontes import FonteCSV


def explorar(fonte):
    """Mostra tamanho, primeiras linhas, valores ausentes e duplicados de uma fonte."""
    tabela = fonte.obter()                                       # polimorfismo: serve para qualquer fonte
    print("=" * 60)
    print(fonte.nome)
    print("=" * 60)
    print("Linhas e colunas:", tabela.shape)                     # (linhas, colunas)
    print(tabela.head())                                         # 5 primeiras linhas
    print("\nValores ausentes por coluna:")
    print(tabela.isna().sum())                                   # quantos vazios em cada coluna
    print("\nLinhas duplicadas:", tabela.duplicated().sum())     # quantas linhas repetidas
    print()


fontes = [
    FonteCSV("Crédito - custeio", config.PASTA_BRUTOS, config.ARQUIVOS_CUSTEIO),
    FonteCSV("Crédito - investimento", config.PASTA_BRUTOS, config.ARQUIVOS_INVESTIMENTO),
    FonteCSV("PRODES", config.PASTA_BRUTOS, config.ARQUIVO_PRODES),
]

for fonte in fontes:
    explorar(fonte)

# Duas particularidades das fontes que vale citar no relatório:
custeio = fontes[0].obter()
print("Registros de custeio por mês em 2016 (mar a jun têm bem menos, a fonte é assim):")
print(custeio[custeio["AnoEmissao"] == "2016"]["MesEmissao"].value_counts().sort_index())

prodes = fontes[2].obter()
print("\nNo PRODES, a linha do ano 2007 é o desmatamento ACUMULADO (1500-2007), não de um ano só:")
print(prodes[prodes["ano_prodes"] == "2007"][["municipio", "inicio_periodo", "incremento_km2"]].head(3))
