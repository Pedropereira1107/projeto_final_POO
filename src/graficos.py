"""Gráficos: a classe que desenha. Ela não faz contas, só recebe tabelas prontas."""

import plotly.express as px     


class Visualizador:
    """Cria os gráficos do dashboard, todos com o mesmo estilo."""

    def __init__(self, altura=450):
        self.altura = altura        # altura dos gráficos, em pixels

    def estilo(self, figura):
        """Aplica o mesmo visual a todos os gráficos."""
        figura.update_layout(template="plotly_white", height=self.altura)
        return figura

    def dispersao(self, tabela, titulo):
        """Pergunta 1: cada ponto é um município (crédito no eixo x, desmatamento no eixo y)."""
        figura = px.scatter(
            tabela,
            x="credito_total",
            y="incremento_km2",
            color="uf",                 # uma cor por estado
            hover_name="municipio",     # nome que aparece ao passar o mouse
            log_x=True, log_y=True,     # escala log: os valores vão de milhares a bilhões
            labels={"credito_total": "Crédito (R$)", "incremento_km2": "Desmatamento (km²)"},
            title=titulo,
        )
        return self.estilo(figura)

    def barras(self, tabela, x, y, cor, titulo):
        """Pergunta 2: barras deitadas (fica mais fácil ler o nome dos produtos)."""
        figura = px.bar(tabela, x=x, y=y, color=cor, orientation="h", title=titulo)
        figura.update_yaxes(categoryorder="total ascending")    # maior barra em cima
        return self.estilo(figura)

    def caixa(self, tabela, x, y, titulo):
        """Pergunta 3: boxplot, que mostra a distribuição de valores em cada grupo."""
        figura = px.box(tabela, x=x, y=y, log_y=True, points="outliers", title=titulo)
        return self.estilo(figura)

    def linhas(self, tabela, y, titulo):
        """Pergunta 4: uma linha por estado ao longo dos anos."""
        figura = px.line(tabela, x="ano_prodes", y=y, color="uf", markers=True, title=titulo)
        return self.estilo(figura)
