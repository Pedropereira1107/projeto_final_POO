"""Dashboard: a classe que monta a página no Streamlit.

Ela recebe o Analisador (que faz as contas) e o Visualizador (que desenha) prontos.
O Dashboard só organiza a tela: filtros, números, abas, gráficos e tabelas.
"""

import streamlit as st      # Streamlit: transforma um script Python em página web


def reais(valor):
    """Formata dinheiro em bilhões: 1234567890 -> 'R$ 1,23 bi'."""
    return f"R$ {valor / 1e9:.2f} bi".replace(".", ",")


def numero(valor):
    """Formata número com ponto de milhar: 12406.3 -> '12.406'."""
    return f"{valor:,.0f}".replace(",", ".")


class Dashboard:
    """Monta a página completa do dashboard."""

    def __init__(self, analisador, visualizador):
        self.analisador = analisador        # objeto que faz os cálculos
        self.visualizador = visualizador    # objeto que desenha os gráficos

    def mostrar(self):
        """Desenha a página inteira, de cima para baixo."""
        st.title("Crédito Rural e Desmatamento na Amazônia Legal")
        st.caption("Fontes: SICOR/BCB (crédito) e PRODES/INPE (desmatamento). "
                   "Valores em reais de dez/2025, corrigidos pelo IPCA.")

        ufs, ano_inicial, ano_final = self.mostrar_filtros()                 # barra lateral
        tabela = self.analisador.filtrar(ufs, ano_inicial, ano_final)        # aplica os filtros

        if tabela.empty:                                                     # nenhum estado marcado
            st.warning("Escolha pelo menos um estado na barra lateral.")
            return                                                           # para de desenhar aqui

        self.mostrar_resumo(tabela)                                          # números do topo

        abas = st.tabs(["1. Crédito x desmatamento", "2. Produtos", "3. Grupos",
                        "4. Evolução", "Dados"])
        with abas[0]:                       # tudo dentro do "with" aparece nesta aba
            self.mostrar_pergunta1(tabela)
        with abas[1]:
            self.mostrar_pergunta2(tabela)
        with abas[2]:
            self.mostrar_pergunta3(tabela)
        with abas[3]:
            self.mostrar_pergunta4(tabela)
        with abas[4]:
            self.mostrar_dados(tabela)

        self.mostrar_limitacoes()

    def mostrar_filtros(self):
        """Barra lateral com os filtros. Devolve o que o usuário escolheu."""
        st.sidebar.header("Filtros")
        todas_ufs = sorted(self.analisador.base["uf"].unique())          # lista de estados, em ordem
        ufs = st.sidebar.multiselect("Estados", todas_ufs, default=todas_ufs)  # caixa de seleção múltipla

        menor_ano = int(self.analisador.base["ano_prodes"].min())
        maior_ano = int(self.analisador.base["ano_prodes"].max())
        ano_inicial, ano_final = st.sidebar.slider(                      # barra deslizante com 2 pontas
            "Anos PRODES (agosto a julho)", menor_ano, maior_ano, (menor_ano, maior_ano))
        return ufs, ano_inicial, ano_final

    def mostrar_resumo(self, tabela):
        """Quatro números grandes no topo da página."""
        resumo = self.analisador.resumo(tabela)
        coluna1, coluna2, coluna3, coluna4 = st.columns(4)               # divide a linha em 4 colunas
        coluna1.metric("Desmatamento", f"{numero(resumo['desmatamento_km2'])} km²")
        coluna2.metric("Crédito rural", reais(resumo["credito_total"]))
        coluna3.metric("Crédito por km² desmatado", f"R$ {numero(resumo['credito_por_km2'])}")
        coluna4.metric("Correlação (Spearman)", f"{resumo['correlacao']:.2f}".replace(".", ","))

    def mostrar_pergunta1(self, tabela):
        st.subheader("Quem recebe mais crédito também desmata mais?")
        municipios = self.analisador.somar_por_municipio(tabela)
        grafico = self.visualizador.dispersao(municipios, "Crédito x desmatamento por município (acumulado)")
        st.plotly_chart(grafico)

        n = st.slider("Tamanho do ranking (top N)", 10, 50, 20)
        st.write(f"Municípios que estão **ao mesmo tempo** no top {n} de crédito para bovinos "
                 f"e no top {n} de desmatamento:")
        st.dataframe(self.analisador.pergunta1(tabela, n), hide_index=True)

    def mostrar_pergunta2(self, tabela):
        st.subheader("Para onde vai o crédito nos municípios que mais desmatam?")
        grupo = st.radio("Grupo de municípios", ["Crítico", "Intermediário", "Baixo"], horizontal=True)
        produtos = self.analisador.pergunta2(tabela, grupo)
        grafico = self.visualizador.barras(produtos, "valor", "produto", "finalidade",
                                           f"10 maiores produtos - grupo {grupo}")
        st.plotly_chart(grafico)

    def mostrar_pergunta3(self, tabela):
        st.subheader("Municípios críticos x municípios com pouco desmatamento")
        st.caption("Crítico = 10% que mais desmatam. Baixo = metade que menos desmata.")
        st.dataframe(self.analisador.pergunta3(tabela), hide_index=True)
        municipios = self.analisador.classificar(tabela)
        grafico = self.visualizador.caixa(municipios, "grupo", "credito_total",
                                          "Distribuição do crédito por grupo")
        st.plotly_chart(grafico)

    def mostrar_pergunta4(self, tabela):
        st.subheader("Evolução por estado")
        serie = self.analisador.pergunta4(tabela)
        esquerda, direita = st.columns(2)                                # dois gráficos lado a lado
        esquerda.plotly_chart(self.visualizador.linhas(serie, "credito_total", "Crédito rural (R$)"))
        direita.plotly_chart(self.visualizador.linhas(serie, "incremento_km2", "Desmatamento (km²)"))

    def mostrar_dados(self, tabela):
        st.dataframe(tabela, hide_index=True)
        st.download_button("Baixar CSV", tabela.to_csv(index=False), "dados_filtrados.csv")

    def mostrar_limitacoes(self):
        st.info(
            "**Limitações:** correlação não é causalidade; o município do contrato pode não ser "
            "o local do desmatamento; só parte do Maranhão está na Amazônia Legal; "
            "mar-jun/2016 tem poucos registros de crédito na própria fonte do BCB."
        )
