"""Ponto de entrada do dashboard.

Executar a partir da raiz do projeto:
    streamlit run src/app.py

Este arquivo apenas cria e conecta os objetos (composição); toda a lógica
fica nas classes dos pacotes ``fontes``, ``tratamento``, ``analise``,
``visualizacao`` e ``dashboard``.
"""

from __future__ import annotations

import streamlit as st

from analise import (
    AnalisadorCreditoDesmatamento,
    CorrelacaoCreditoDesmatamento,
    CreditoPorKm2,
    TotalCredito,
    TotalDesmatado,
    VariacaoAnualDesmatamento,
)
from dashboard import Dashboard
from pipeline import carregar_bases
from visualizacao import Visualizador


@st.cache_resource  # carrega os CSVs uma vez só, e não a cada clique no dashboard
def criar_analisador() -> AnalisadorCreditoDesmatamento:
    base, por_produto = carregar_bases()
    return AnalisadorCreditoDesmatamento(base, por_produto)


def main() -> None:
    dashboard = Dashboard(
        analisador=criar_analisador(),
        visualizador=Visualizador(),
        indicadores=[
            TotalDesmatado(),
            TotalCredito(),
            CreditoPorKm2(),
            CorrelacaoCreditoDesmatamento(),
            VariacaoAnualDesmatamento(),
        ],
    )
    dashboard.renderizar()


if __name__ == "__main__":
    main()
