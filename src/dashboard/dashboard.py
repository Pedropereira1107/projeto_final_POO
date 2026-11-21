"""Organização dos componentes do painel em Streamlit."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from analise.analisador import AnalisadorCreditoDesmatamento
from analise.indicadores import Indicador
from visualizacao.visualizador import Visualizador


class Dashboard:
    """Monta a página do dashboard.

    Recebe os objetos prontos pelo construtor (injeção de dependência):
    o Dashboard só organiza a tela; quem calcula é o Analisador/Indicadores
    e quem desenha é o Visualizador.

    Args:
        analisador: Analisador com as bases integradas.
        visualizador: Gerador de gráficos.
        indicadores: Lista de indicadores exibidos como KPIs.
        titulo: Título da página.
    """

    def __init__(
        self,
        analisador: AnalisadorCreditoDesmatamento,
        visualizador: Visualizador,
        indicadores: list[Indicador],
        titulo: str = "Crédito Rural e Desmatamento na Amazônia Legal",
    ) -> None:
        self._analisador = analisador
        self._visualizador = visualizador
        self._indicadores = indicadores
        self._titulo = titulo

    def renderizar(self) -> None:
        """Desenha a página completa."""
        self._cabecalho()
        filtros = self._filtros()
        df = self._analisador.filtrar(**filtros)
        self._kpis(df)
        aba1, aba2, aba3, aba4, aba5 = st.tabs(
            ["1. Crédito × desmatamento", "2. Finalidades e produtos",
             "3. Críticos × pouco desmatamento", "4. Evolução por estado", "Dados"]
        )
        with aba1:
            self._pergunta1(df)
        with aba2:
            self._pergunta2(df)
        with aba3:
            self._pergunta3(df)
        with aba4:
            self._pergunta4(df)
        with aba5:
            self._tabela(df)
        self._limitacoes()

    # ------------------------------------------------------------------ #
    # Seções da página
    # ------------------------------------------------------------------ #
    def _cabecalho(self) -> None:
        """Título, subtítulo e contexto do problema."""
        # TODO: st.set_page_config(page_title=self._titulo, layout="wide")  (1ª chamada Streamlit!)
        # TODO: st.title(self._titulo); st.caption("Fontes: SICOR/BCB e PRODES/INPE, 2014-2025")
        raise NotImplementedError

    def _filtros(self) -> dict:
        """Filtros na barra lateral. Retorna os argumentos para ``filtrar``."""
        # TODO: ufs = st.sidebar.multiselect("Estados", self._analisador.ufs, default=self._analisador.ufs)
        # TODO: ini, fim = st.sidebar.slider("Anos PRODES", *self._analisador.anos, value=self._analisador.anos)
        # TODO: return {"ufs": ufs, "ano_inicial": ini, "ano_final": fim}
        raise NotImplementedError

    def _kpis(self, df: pd.DataFrame) -> None:
        """Indicadores principais em colunas."""
        # TODO: cols = st.columns(len(self._indicadores))
        # TODO: for col, ind in zip(cols, self._indicadores):
        #           col.metric(ind.nome, ind.formatar(ind.calcular(df)), help=ind.descricao)
        raise NotImplementedError

    def _pergunta1(self, df: pd.DataFrame) -> None:
        """Dispersão crédito × desmatamento + tabela dos municípios nos dois rankings."""
        # TODO: m = self._analisador.acumular_por_municipio(df)
        # TODO: st.plotly_chart(self._visualizador.dispersao(m, "credito_total", "incremento_km2", "uf", "..."))
        # TODO: st.dataframe(self._analisador.p1_sobreposicao_rankings(df))
        raise NotImplementedError

    def _pergunta2(self, df: pd.DataFrame) -> None:
        """Barras: finalidades e produtos que concentram o crédito nos municípios críticos."""
        # TODO: grupo = st.radio("Grupo", ["Crítico", "Baixo"], horizontal=True)
        # TODO: p = self._analisador.p2_credito_por_produto(df, grupo)
        # TODO: st.plotly_chart(self._visualizador.grafico_barras(p, "produto", "valor", "..."))
        raise NotImplementedError

    def _pergunta3(self, df: pd.DataFrame) -> None:
        """Comparação entre grupos (tabela + boxplot)."""
        # TODO: st.dataframe(self._analisador.p3_comparar_grupos(df))
        # TODO: st.plotly_chart(self._visualizador.boxplot(classificados, "grupo", "credito_total", "..."))
        raise NotImplementedError

    def _pergunta4(self, df: pd.DataFrame) -> None:
        """Linhas: evolução de crédito e desmatamento por UF."""
        # TODO: s = self._analisador.p4_serie_por_uf(df)
        # TODO: dois gráficos lado a lado com st.columns(2): crédito e desmatamento, cor="uf"
        raise NotImplementedError

    def _tabela(self, df: pd.DataFrame) -> None:
        """Tabela de dados filtrados + botão de download."""
        # TODO: st.dataframe(df, use_container_width=True)
        # TODO: st.download_button("Baixar CSV", df.to_csv(index=False), "dados_filtrados.csv")
        raise NotImplementedError

    def _limitacoes(self) -> None:
        """Aviso fixo com as limitações do estudo."""
        # TODO: st.info("Correlação não é causalidade; o município do contrato pode não ser o local
        #               do desmatamento; valores nominais; queda de registros em mar-jun/2016.")
        raise NotImplementedError
