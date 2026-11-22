"""Análise: os cálculos que respondem às 4 perguntas do projeto.

A classe só faz contas sobre tabelas prontas. Ela não lê arquivos e não desenha gráficos.
"""

import pandas as pd


class Analisador:
    """Responde às perguntas sobre crédito rural e desmatamento."""

    def __init__(self, base, produtos):
        self.base = base            # tabela município x ano (perguntas 1, 3 e 4)
        self.produtos = produtos    # tabela de crédito por produto (pergunta 2)

    # ------------------------------------------------------------------ #
    # Ferramentas usadas pelas perguntas
    # ------------------------------------------------------------------ #
    def filtrar(self, ufs, ano_inicial, ano_final):
        """Devolve só as linhas dos estados e anos escolhidos no dashboard."""
        tabela = self.base
        tabela = tabela[tabela["uf"].isin(ufs)]                                  # isin = "está na lista?"
        tabela = tabela[tabela["ano_prodes"].between(ano_inicial, ano_final)]    # between = "entre"
        return tabela

    def somar_por_municipio(self, tabela):
        """Soma todos os anos: fica 1 linha por município."""
        colunas = ["incremento_km2", "credito_total", "credito_custeio",
                   "credito_investimento", "credito_bovinos"]
        return tabela.groupby(["cod_ibge", "municipio", "uf"])[colunas].sum().reset_index()

    def classificar(self, tabela):
        """Separa os municípios em 3 grupos pelo desmatamento acumulado.

        - Crítico: os 10% que mais desmatam (acima do percentil 90)
        - Baixo: a metade que menos desmata (até a mediana)
        - Intermediário: o resto
        """
        municipios = self.somar_por_municipio(tabela)
        limite_baixo = municipios["incremento_km2"].quantile(0.5)     # mediana
        limite_critico = municipios["incremento_km2"].quantile(0.9)   # percentil 90

        municipios["grupo"] = "Intermediário"                                            # todos começam aqui
        municipios.loc[municipios["incremento_km2"] <= limite_baixo, "grupo"] = "Baixo"   # os de baixo
        municipios.loc[municipios["incremento_km2"] >= limite_critico, "grupo"] = "Crítico"  # os do topo
        return municipios

    def resumo(self, tabela):
        """Números do topo do dashboard (os KPIs)."""
        desmatamento = tabela["incremento_km2"].sum()
        credito = tabela["credito_total"].sum()

        if desmatamento > 0:                    # evita dividir por zero
            credito_por_km2 = credito / desmatamento
        else:
            credito_por_km2 = 0

        municipios = self.somar_por_municipio(tabela)
        # Correlação de Spearman: vai de -1 a 1. Perto de 1 = quem tem mais crédito também desmata mais.
        # rank() troca cada valor pela sua posição no ranking (1º, 2º, 3º...). Correlacionar as
        # posições (e não os valores) evita que poucos municípios gigantes distorçam o resultado.
        posicao_credito = municipios["credito_total"].rank()
        posicao_desmatamento = municipios["incremento_km2"].rank()
        correlacao = posicao_credito.corr(posicao_desmatamento)

        return {
            "desmatamento_km2": desmatamento,
            "credito_total": credito,
            "credito_por_km2": credito_por_km2,
            "correlacao": correlacao,
        }

    # ------------------------------------------------------------------ #
    # As 4 perguntas
    # ------------------------------------------------------------------ #
    def pergunta1(self, tabela, n=20):
        """P1: quais municípios estão ao mesmo tempo no top N de crédito para bovinos e no top N de desmatamento?"""
        municipios = self.somar_por_municipio(tabela)
        top_credito = municipios.nlargest(n, "credito_bovinos")["cod_ibge"]        # nlargest = os N maiores
        top_desmatamento = municipios.nlargest(n, "incremento_km2")["cod_ibge"]
        nos_dois = municipios["cod_ibge"].isin(top_credito) & municipios["cod_ibge"].isin(top_desmatamento)
        return municipios[nos_dois].sort_values("incremento_km2", ascending=False)

    def pergunta2(self, tabela, grupo, n=10):
        """P2: nos municípios de um grupo (ex.: "Crítico"), quais finalidades e produtos recebem mais crédito?"""
        municipios = self.classificar(tabela)
        codigos = municipios.loc[municipios["grupo"] == grupo, "cod_ibge"]   # códigos dos municípios do grupo

        produtos = self.produtos
        produtos = produtos[produtos["cod_ibge"].isin(codigos)]                    # só esses municípios
        produtos = produtos[produtos["ano_prodes"].isin(tabela["ano_prodes"])]     # só os anos do filtro

        soma = produtos.groupby(["finalidade", "produto"])["valor"].sum().reset_index()
        return soma.nlargest(n, "valor")

    def pergunta3(self, tabela):
        """P3: os municípios que desmatam pouco recebem mais ou menos crédito que os críticos?"""
        municipios = self.classificar(tabela)
        grupos = municipios.groupby("grupo")
        resultado = pd.DataFrame({
            "municipios": grupos["cod_ibge"].count(),              # quantos municípios em cada grupo
            "credito_medio": grupos["credito_total"].mean(),       # média
            "credito_mediano": grupos["credito_total"].median(),   # mediana (menos afetada por extremos)
            "desmatamento_total_km2": grupos["incremento_km2"].sum(),
        })
        return resultado.reset_index()

    def pergunta4(self, tabela):
        """P4: como crédito e desmatamento evoluíram juntos em cada estado, ano a ano?"""
        colunas = ["credito_total", "incremento_km2"]
        return tabela.groupby(["uf", "ano_prodes"])[colunas].sum().reset_index()
