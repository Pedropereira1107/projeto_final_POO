"""Pacote de tratamento, análise e indicadores (Etapa 4)."""

from analise.analisador import AnalisadorCreditoDesmatamento
from analise.indicadores import (
    CorrelacaoCreditoDesmatamento,
    CreditoPorKm2,
    Indicador,
    TotalCredito,
    TotalDesmatado,
    VariacaoAnualDesmatamento,
)

__all__ = [
    "AnalisadorCreditoDesmatamento",
    "Indicador",
    "TotalDesmatado",
    "TotalCredito",
    "CreditoPorKm2",
    "CorrelacaoCreditoDesmatamento",
    "VariacaoAnualDesmatamento",
]
