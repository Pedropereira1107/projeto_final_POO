"""Testes das fontes de dados."""

import pandas as pd
import pytest

from fontes import FonteCSV, FonteDados


def test_fonte_dados_e_abstrata():
    # Classe abstrata é só um molde: tentar criar um objeto dela dá erro
    with pytest.raises(TypeError):
        FonteDados("qualquer")


def test_fonte_csv_junta_varios_arquivos(tmp_path):
    # tmp_path = uma pasta temporária que o pytest cria e apaga sozinho
    pd.DataFrame({"codigo": ["01"]}).to_csv(tmp_path / "dados_2020.csv", index=False)
    pd.DataFrame({"codigo": ["02"]}).to_csv(tmp_path / "dados_2021.csv", index=False)

    tabela = FonteCSV("teste", tmp_path, "dados_*.csv").obter()

    assert len(tabela) == 2                             # juntou os 2 arquivos
    assert tabela["codigo"].tolist() == ["01", "02"]    # manteve o zero à esquerda


def test_obter_le_so_uma_vez(tmp_path):
    pd.DataFrame({"a": [1]}).to_csv(tmp_path / "x.csv", index=False)
    fonte = FonteCSV("teste", tmp_path, "x.csv")
    # "is" confere se é exatamente o mesmo objeto (não leu o arquivo de novo)
    assert fonte.obter() is fonte.obter()


def test_fonte_csv_sem_arquivo_da_erro(tmp_path):
    with pytest.raises(FileNotFoundError):
        FonteCSV("teste", tmp_path, "nao_existe.csv").obter()
