# Crédito Rural e Desmatamento na Amazônia Legal

Projeto final de Programação Orientada a Objetos: um sistema de análise de dados e dashboard interativo
(Python, POO, Pandas, Plotly e Streamlit) para verificar se o crédito rural está associado ao desmatamento
nos estados da Amazônia Legal.

## Estrutura

```
├── data/
│   ├── raw/                 # dados originais (PRODES, cache do SICOR)
│   └── processed/           # dados tratados gerados pelo código
├── docs/                    # documentação publicada no GitHub Pages (MkDocs)
├── src/
│   ├── app.py               # ponto de entrada do dashboard (Streamlit)
│   ├── exploracao.py        # exploração inicial dos dados (Etapa 2)
│   ├── config.py            # caminhos e constantes
│   ├── fontes/              # FonteDados, FonteCSV, FonteAPI
│   ├── analise/             # AnalisadorDados, Indicador e subclasses
│   ├── visualizacao/        # Visualizador
│   └── dashboard/           # Dashboard
├── tests/                   # testes automatizados (pytest)
├── mkdocs.yml
├── pyproject.toml
└── requirements.txt
```

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

python src/exploracao.py        # exploração inicial
streamlit run src/app.py        # dashboard
pytest -v                       # testes
mkdocs serve                    # documentação local
mkdocs gh-deploy                # publica no gh-pages
```

## Fontes de dados

- **PRODES/INPE**: incremento anual de desmatamento por município.
- **SICOR/BCB**: Matriz de Dados do Crédito Rural.
