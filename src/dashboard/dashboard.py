"""Organização dos componentes do painel em Streamlit."""

from __future__ import annotations

import pandas as pd

from analise.analisador import AnalisadorDados
from analise.indicadores import Indicador
from visualizacao.visualizador import Visualizador


class Dashboard:
    """Monta a página do dashboard.

    Recebe os objetos prontos pelo construtor (injeção de dependência):
    o Dashboard só organiza a tela; quem calcula é o Analisador/Indicadores
    e quem desenha é o Visualizador.

    Args:
        analisador: Analisador com a base já integrada.
        visualizador: Gerador de gráficos.
        indicadores: Lista de indicadores exibidos como KPIs.
        titulo: Título da página.
    """

    def __init__(
        self,
        analisador: AnalisadorDados,
        visualizador: Visualizador,
        indicadores: list[Indicador],
        titulo: str = "Crédito Rural e Desmatamento na Amazônia Legal",
    ) -> None:
        self._analisador = analisador
        self._visualizador = visualizador
        self._indicadores = indicadores
        self._titulo = titulo

    def renderizar(self) -> None:
        """Desenha a página completa, na ordem exigida pelo enunciado."""
        self._cabecalho()
        filtros = self._filtros()
        df = self._analisador.filtrar(**filtros)
        self._kpis(df)
        self._graficos(df)
        self._tabela(df)
        self._analise_interpretativa(df)

    # ------------------------------------------------------------------ #
    # Seções da página
    # ------------------------------------------------------------------ #
    def _cabecalho(self) -> None:
        """Título, subtítulo e contexto do problema."""
        # TODO: st.set_page_config(...) (deve ser a 1ª chamada Streamlit), st.title, st.markdown
        raise NotImplementedError

    def _filtros(self) -> dict:
        """Filtros na barra lateral. Retorna os argumentos para ``AnalisadorDados.filtrar``."""
        # TODO: st.sidebar.multiselect (UFs) e st.sidebar.slider (intervalo de anos)
        # TODO: return {"ufs": ..., "ano_inicial": ..., "ano_final": ...}
        raise NotImplementedError

    def _kpis(self, df: pd.DataFrame) -> None:
        """Indicadores principais em colunas."""
        # TODO: cols = st.columns(len(self._indicadores))
        # TODO: para cada indicador: col.metric(ind.nome, ind.formatar(ind.calcular(df)))
        raise NotImplementedError

    def _graficos(self, df: pd.DataFrame) -> None:
        """Visualizações dinâmicas (barras, linhas, treemap, dispersão, boxplot)."""
        # TODO: st.tabs([...]) + st.plotly_chart(fig, use_container_width=True)
        raise NotImplementedError

    def _tabela(self, df: pd.DataFrame) -> None:
        """Tabela de dados filtrados + botão de download."""
        # TODO: st.dataframe(df); st.download_button(...)
        raise NotImplementedError

    def _analise_interpretativa(self, df: pd.DataFrame) -> None:
        """Texto interpretando os resultados do recorte atual."""
        # TODO: st.markdown / st.info com conclusões baseadas nos indicadores
        raise NotImplementedError
