"""Geração das visualizações interativas com Plotly."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


class Visualizador:
    """Gera os gráficos do projeto. Apenas desenha: não calcula nada.

    Cada método recebe um DataFrame já preparado pelo ``AnalisadorDados``
    e devolve uma ``plotly.graph_objects.Figure``.

    Args:
        tema: Template do Plotly (ex.: "plotly_white").
        altura: Altura padrão dos gráficos, em pixels.
    """

    def __init__(self, tema: str = "plotly_white", altura: int = 450) -> None:
        self._tema = tema
        self._altura = altura

    def grafico_barras(self, df: pd.DataFrame, x: str, y: str, titulo: str) -> go.Figure:
        """Gráfico de barras (ex.: desmatamento por UF)."""
        # TODO: px.bar(...) e self._aplicar_estilo(fig)
        raise NotImplementedError

    def grafico_linhas(self, df: pd.DataFrame, x: str, y: str | list[str], titulo: str) -> go.Figure:
        """Gráfico de linhas (ex.: evolução anual de crédito e desmatamento)."""
        # TODO: px.line(..., markers=True)
        raise NotImplementedError

    def treemap(self, df: pd.DataFrame, caminho: list[str], valores: str, titulo: str) -> go.Figure:
        """Treemap hierárquico (ex.: UF -> município)."""
        # TODO: px.treemap(df, path=caminho, values=valores)
        raise NotImplementedError

    def dispersao(self, df: pd.DataFrame, x: str, y: str, cor: str | None, titulo: str) -> go.Figure:
        """Dispersão crédito × desmatamento (gráfico central da pergunta de pesquisa)."""
        # TODO: px.scatter(..., hover_name="municipio", log_x=True)
        raise NotImplementedError

    def boxplot(self, df: pd.DataFrame, x: str, y: str, titulo: str) -> go.Figure:
        """Boxplot (ex.: distribuição do desmatamento por UF)."""
        # TODO: px.box(...)
        raise NotImplementedError

    def _aplicar_estilo(self, fig: go.Figure) -> go.Figure:
        """Aplica tema e altura padronizados a qualquer figura."""
        # TODO: fig.update_layout(template=self._tema, height=self._altura)
        raise NotImplementedError
