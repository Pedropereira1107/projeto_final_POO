"""Tratamento e integração dos dados: transforma os dados brutos nas duas tabelas da análise.

Caminho dos dados:
    Fontes (CSV e API)  ->  TratadorCredito  ->  IntegradorMunicipal  ->  data/processed/

Pode ser executado sozinho (gera os arquivos de data/processed):
    python src/preparar_dados.py
O dashboard também chama este arquivo sozinho, se os arquivos ainda não existirem.
"""

import json             # para ler o arquivo .json com a lista de municípios

import pandas as pd

import config
from fontes import FonteAPI, FonteCSV


class TratadorCredito:
    """Limpa o crédito rural: junta custeio + investimento e corrige pela inflação."""

    # Os dois arquivos do BCB usam nomes diferentes para a mesma coisa.
    # Este dicionário diz: "nome antigo": "nome novo".
    NOVOS_NOMES = {
        "Municipio": "municipio",
        "nomeProduto": "produto",
        "AnoEmissao": "ano",
        "MesEmissao": "mes",
        "VlCusteio": "valor",          # valor no arquivo de custeio
        "VlInvest": "valor",           # valor no arquivo de investimento
        "codCadMu": "cod_cadmu",       # código interno do BCB no custeio
        "cdMunicipio": "cod_cadmu",    # o mesmo código, com outro nome, no investimento
        "codIbge": "cod_ibge",         # código IBGE (só existe no custeio)
    }

    def __init__(self, custeio, investimento, ipca):
        self.custeio = custeio              # tabela bruta de custeio
        self.investimento = investimento    # tabela bruta de investimento
        self.ipca = ipca                    # tabela do IPCA (inflação mensal)

    def processar(self):
        """Executa todas as etapas, na ordem, e devolve uma linha por operação de crédito."""
        custeio = self.padronizar(self.custeio, "custeio")                    # etapa 1: nomes iguais
        investimento = self.padronizar(self.investimento, "investimento")     # etapa 1: nomes iguais
        investimento = self.adicionar_codigo_ibge(investimento, custeio)      # etapa 2: código IBGE
        credito = pd.concat([custeio, investimento], ignore_index=True)       # etapa 3: junta as duas
        credito = self.limpar(credito)                                        # etapa 4: tipos e colunas novas
        credito = self.corrigir_inflacao(credito)                             # etapa 5: valores pelo IPCA
        return credito

    def padronizar(self, tabela, finalidade):
        """Etapa 1: renomeia as colunas e marca se é custeio ou investimento."""
        tabela = tabela.rename(columns=self.NOVOS_NOMES)   # troca os nomes das colunas
        tabela["finalidade"] = finalidade                  # nova coluna com "custeio" ou "investimento"
        return tabela

    def adicionar_codigo_ibge(self, investimento, custeio):
        """Etapa 2: o investimento não tem código IBGE; pegamos do custeio pelo código cadmu."""
        # tabela de "tradução": cada cod_cadmu com o seu cod_ibge (sem repetições)
        traducao = custeio[["cod_cadmu", "cod_ibge"]].dropna().drop_duplicates("cod_cadmu")
        # merge = PROCV do Excel: procura o cod_cadmu na tradução e traz o cod_ibge
        investimento = investimento.merge(traducao, on="cod_cadmu", how="left")
        # 210 linhas (R$ 6,4 mi) não têm tradução: são descartadas
        return investimento.dropna(subset=["cod_ibge"])

    def limpar(self, credito):
        """Etapa 4: fica só com as colunas úteis, acerta os tipos e cria uf e ano_prodes."""
        colunas = ["finalidade", "ano", "mes", "cod_ibge", "municipio", "produto", "valor"]
        credito = credito[colunas].copy()                          # só as colunas que vamos usar

        credito["ano"] = credito["ano"].astype(int)                # texto "2020" -> número 2020
        credito["mes"] = credito["mes"].astype(int)                # texto "01" -> número 1
        credito["valor"] = credito["valor"].astype(float)          # texto -> número com casas decimais
        credito["produto"] = credito["produto"].str.replace('"', "").str.strip()  # '"BOVINOS"' -> 'BOVINOS'
        credito["uf"] = credito["cod_ibge"].str[:2].map(config.UFS)  # 2 primeiros dígitos -> sigla ("11" -> "RO")

        # O ano PRODES vai de agosto a julho: ago/2020 a jul/2021 = PRODES 2021.
        credito["ano_prodes"] = credito["ano"]                           # começa igual ao ano...
        de_agosto_em_diante = credito["mes"] >= 8                        # ...marca os meses de agosto a dezembro...
        credito.loc[de_agosto_em_diante, "ano_prodes"] = credito["ano"] + 1  # ...e soma 1 nesses meses
        return credito

    def corrigir_inflacao(self, credito):
        """Etapa 5: converte todos os valores para reais de dezembro de 2025."""
        ipca = self.ipca.copy()
        ipca["ano"] = ipca["data"].str[6:10].astype(int)   # "01/03/2020" -> 2020
        ipca["mes"] = ipca["data"].str[3:5].astype(int)    # "01/03/2020" -> 3

        # Índice acumulado: começa em 1 e vai multiplicando (1 + inflação do mês).
        # Ex.: inflação de 1% e depois 2% -> 1,01 e depois 1,01 x 1,02 = 1,0302
        ipca["indice"] = (1 + ipca["valor"].astype(float) / 100).cumprod()

        indice_dez_2025 = ipca["indice"].iloc[-1]           # último mês da tabela = dez/2025
        ipca["fator"] = indice_dez_2025 / ipca["indice"]    # quanto cada mês precisa ser "atualizado"

        # traz o fator de cada mês para as operações de crédito daquele mês (como um PROCV)
        credito = credito.merge(ipca[["ano", "mes", "fator"]], on=["ano", "mes"], how="left")
        credito["valor"] = credito["valor"] * credito["fator"]   # valor corrigido pela inflação
        return credito.drop(columns="fator")                     # a coluna fator não é mais necessária


class IntegradorMunicipal:
    """Junta o crédito com o desmatamento, por município e por ano PRODES."""

    def __init__(self, credito, prodes, municipios):
        self.credito = credito          # saída do TratadorCredito
        self.prodes = prodes            # tabela bruta do PRODES
        self.municipios = municipios    # lista oficial dos 772 municípios

    def montar_base(self):
        """Tabela com 1 linha por município e ano (772 x 12 = 9.264 linhas). Perguntas 1, 3 e 4."""
        # --- 1. Somar o crédito de cada município em cada ano ---
        credito = self.credito.copy()
        credito["credito_custeio"] = 0.0                                    # coluna começa com zero...
        e_custeio = credito["finalidade"] == "custeio"
        credito.loc[e_custeio, "credito_custeio"] = credito["valor"]        # ...e recebe o valor se for custeio

        credito["credito_investimento"] = 0.0                               # mesma ideia para investimento
        e_investimento = credito["finalidade"] == "investimento"
        credito.loc[e_investimento, "credito_investimento"] = credito["valor"]

        credito["credito_bovinos"] = 0.0                                    # e para o produto BOVINOS
        e_bovinos = credito["produto"] == "BOVINOS"
        credito.loc[e_bovinos, "credito_bovinos"] = credito["valor"]

        credito["registros"] = 1                                 # cada linha é 1 operação; somando, temos a contagem
        credito = credito.rename(columns={"valor": "credito_total"})

        colunas_somadas = ["credito_total", "credito_custeio", "credito_investimento",
                           "credito_bovinos", "registros"]
        # groupby = "tabela dinâmica": agrupa por município e ano, e soma as colunas
        credito_por_ano = credito.groupby(["cod_ibge", "ano_prodes"])[colunas_somadas].sum().reset_index()

        # --- 2. Preparar o desmatamento ---
        prodes = self.prodes.rename(columns={"codibge": "cod_ibge"})
        prodes["ano_prodes"] = prodes["ano_prodes"].astype(int)
        prodes["incremento_km2"] = prodes["incremento_km2"].astype(float)
        prodes = prodes[["cod_ibge", "ano_prodes", "incremento_km2"]]

        # --- 3. Grade completa: todo município em todo ano (mesmo sem crédito ou sem desmatamento) ---
        anos = pd.DataFrame({"ano_prodes": range(config.ANO_INICIAL, config.ANO_FINAL + 1)})
        grade = self.municipios.merge(anos, how="cross")    # "cross" = combina cada município com cada ano

        # --- 4. Juntar tudo na grade ---
        base = grade.merge(prodes, on=["cod_ibge", "ano_prodes"], how="left")          # traz o desmatamento
        base = base.merge(credito_por_ano, on=["cod_ibge", "ano_prodes"], how="left")  # traz o crédito
        base = base.fillna(0)                          # vazio = não teve desmatamento ou não teve crédito
        base["registros"] = base["registros"].astype(int)
        return base

    def agregar_por_produto(self):
        """Crédito somado por município, ano, finalidade e produto. Pergunta 2."""
        credito = self.credito
        oficiais = credito["cod_ibge"].isin(self.municipios["cod_ibge"])   # só os 772 municípios oficiais
        no_periodo = credito["ano_prodes"].between(config.ANO_INICIAL, config.ANO_FINAL)  # só 2014 a 2025
        credito = credito[oficiais & no_periodo]
        colunas = ["cod_ibge", "uf", "ano_prodes", "finalidade", "produto"]
        return credito.groupby(colunas)["valor"].sum().reset_index()


def ler_municipios_oficiais():
    """Lista oficial dos 772 municípios da Amazônia Legal (vem do painel do PRODES).

    Ela é necessária porque só parte do Maranhão está na Amazônia Legal.
    """
    with open(config.ARQUIVO_MUNICIPIOS, encoding="utf-8") as arquivo:   # abre o arquivo .json
        conteudo = json.load(arquivo)                                    # transforma em dicionário do Python

    for camada in conteudo["lois"]:            # o arquivo tem várias camadas (estados, municípios...)
        if camada["name"] == "mun":            # queremos a camada de municípios
            lista = camada["loinames"]

    municipios = pd.DataFrame(lista)                                     # vira tabela
    municipios = municipios.rename(columns={"codibge": "cod_ibge", "loiname": "municipio"})
    municipios["cod_ibge"] = municipios["cod_ibge"].astype(str)          # código como texto
    municipios["uf"] = municipios["cod_ibge"].str[:2].map(config.UFS)    # sigla do estado
    municipios = municipios.dropna(subset=["uf"])                        # tira quem não é dos 9 estados
    return municipios[["cod_ibge", "municipio", "uf"]].drop_duplicates("cod_ibge")


def preparar_bases():
    """Executa o caminho completo: Fontes -> Tratador -> Integrador -> salva os arquivos."""
    # 1. Fontes: cada uma sabe buscar os seus dados
    custeio = FonteCSV("Crédito - custeio", config.PASTA_BRUTOS, config.ARQUIVOS_CUSTEIO).obter()
    investimento = FonteCSV("Crédito - investimento", config.PASTA_BRUTOS, config.ARQUIVOS_INVESTIMENTO).obter()
    prodes = FonteCSV("PRODES", config.PASTA_BRUTOS, config.ARQUIVO_PRODES).obter()
    ipca = FonteAPI("IPCA", config.IPCA_URL, config.ARQUIVO_IPCA).obter()
    municipios = ler_municipios_oficiais()

    # 2. Tratamento do crédito
    credito = TratadorCredito(custeio, investimento, ipca).processar()

    # 3. Integração com o desmatamento
    integrador = IntegradorMunicipal(credito, prodes, municipios)
    base = integrador.montar_base()
    produtos = integrador.agregar_por_produto()

    # 4. Salva os resultados (da próxima vez, o dashboard só lê esses arquivos)
    config.PASTA_PROCESSADOS.mkdir(parents=True, exist_ok=True)
    base.to_csv(config.PASTA_PROCESSADOS / config.ARQUIVO_BASE, index=False)
    produtos.to_csv(config.PASTA_PROCESSADOS / config.ARQUIVO_PRODUTOS, index=False)
    return base, produtos


def carregar_bases():
    """Lê as duas tabelas prontas. Se ainda não existirem, gera primeiro."""
    base_existe = (config.PASTA_PROCESSADOS / config.ARQUIVO_BASE).exists()
    produtos_existe = (config.PASTA_PROCESSADOS / config.ARQUIVO_PRODUTOS).exists()
    if not base_existe or not produtos_existe:
        return preparar_bases()

    texto = {"cod_ibge": str}   # só o código fica como texto; o resto é lido como número
    base = FonteCSV("Base município x ano", config.PASTA_PROCESSADOS, config.ARQUIVO_BASE, texto).obter()
    produtos = FonteCSV("Crédito por produto", config.PASTA_PROCESSADOS, config.ARQUIVO_PRODUTOS, texto).obter()
    return base, produtos


# Este bloco só roda quando o arquivo é executado direto: python src/preparar_dados.py
if __name__ == "__main__":
    base, produtos = preparar_bases()
    print(f"base_municipio_ano.csv: {len(base)} linhas")
    print(f"credito_municipio_produto.csv: {len(produtos)} linhas")
