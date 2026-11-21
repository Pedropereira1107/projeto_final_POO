"""Testes dos indicadores."""

import pytest

from analise import (
    CorrelacaoCreditoDesmatamento,
    CreditoPorKm2,
    Indicador,
    TotalCredito,
    TotalDesmatado,
    VariacaoAnualDesmatamento,
)

TODOS = [
    TotalDesmatado,
    TotalCredito,
    CreditoPorKm2,
    CorrelacaoCreditoDesmatamento,
    VariacaoAnualDesmatamento,
]


@pytest.mark.parametrize("classe", TODOS)
def test_indicadores_sao_subclasses_de_indicador(classe):
    assert isinstance(classe(), Indicador)


@pytest.mark.skip(reason="TODO: implementar calcular")
def test_total_desmatado():
    ...


@pytest.mark.skip(reason="TODO: implementar calcular")
def test_credito_por_km2_sem_desmatamento_nao_divide_por_zero():
    ...
