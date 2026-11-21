"""Ponto de entrada do dashboard.

Executar a partir da raiz do projeto:
    streamlit run src/app.py

Este arquivo apenas cria e conecta os objetos (composição); toda a lógica
fica nas classes dos pacotes ``fontes``, ``analise``, ``visualizacao`` e ``dashboard``.
"""

from __future__ import annotations

import config
from analise import (
    AnalisadorDados,
    CorrelacaoCreditoDesmatamento,
    CreditoPorKm2,
    TotalCredito,
    TotalDesmatado,
    VariacaoAnualDesmatamento,
)
from dashboard import Dashboard
from fontes import FonteAPI, FonteCSV
from visualizacao import Visualizador


def criar_fontes() -> tuple[FonteCSV, FonteAPI]:
    """Instancia as fontes de dados do projeto."""
    prodes = FonteCSV(
        nome="PRODES/INPE",
        caminho=config.ARQUIVO_PRODES,
        descricao="Incremento anual de desmatamento por município da Amazônia Legal.",
        dtype={"codibge": str},
    )
    sicor = FonteAPI(
        nome="SICOR/BCB",
        url=f"{config.SICOR_URL_BASE}/{config.SICOR_RECURSO}",
        parametros={"$format": "json"},  # TODO: completar filtros ($filter, $top, ...)
        descricao="Matriz de Dados do Crédito Rural.",
        timeout=config.SICOR_TIMEOUT_SEGUNDOS,
        caminho_cache=config.ARQUIVO_SICOR,
    )
    return prodes, sicor


def criar_analisador() -> AnalisadorDados:
    """Carrega as fontes e devolve o analisador com a base integrada."""
    # TODO: decorar com @st.cache_resource para não recarregar a cada interação
    prodes, sicor = criar_fontes()
    analisador = AnalisadorDados(prodes.obter(), sicor.obter())
    analisador.integrar()
    return analisador


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
