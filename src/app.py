"""Ponto de entrada: liga todas as peças e abre o dashboard.

Executar na raiz do projeto:
    streamlit run src/app.py
"""

import streamlit as st

from analisador import Analisador
from dashboard import Dashboard
from graficos import Visualizador
from preparar_dados import carregar_bases

st.set_page_config(page_title="Crédito Rural e Desmatamento", layout="wide")  # 1º comando do Streamlit


@st.cache_resource      # guarda o resultado: os dados são lidos 1 vez só, e não a cada clique
def criar_analisador():
    base, produtos = carregar_bases()       # lê (ou gera) as tabelas prontas
    return Analisador(base, produtos)       # cria o objeto que faz as contas


analisador = criar_analisador()                      # objeto que calcula
visualizador = Visualizador()                        # objeto que desenha
dashboard = Dashboard(analisador, visualizador)      # objeto que monta a página, usando os dois acima
dashboard.mostrar()                                  # desenha a página
