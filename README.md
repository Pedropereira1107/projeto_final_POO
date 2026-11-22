# Crédito Rural e Desmatamento na Amazônia Legal

Projeto final de Programação Orientada a Objetos: um sistema de análise de dados e dashboard interativo
(Python, POO, Pandas, Plotly e Streamlit) para verificar se o crédito rural está associado ao desmatamento
nos estados da Amazônia Legal.

## Estrutura

```
├── data/
│   ├── raw/                 # dados originais (BCB e PRODES), nunca alterados
│   └── processed/           # tabelas geradas pelo programa (recriadas se apagadas)
├── src/
│   ├── config.py            # caminhos e valores fixos
│   ├── fontes.py            # FonteDados (abstrata), FonteCSV, FonteAPI
│   ├── preparar_dados.py    # TratadorCredito, IntegradorMunicipal
│   ├── analisador.py        # Analisador (as 4 perguntas)
│   ├── graficos.py          # Visualizador
│   ├── dashboard.py         # Dashboard (Streamlit)
│   ├── app.py               # ponto de entrada: liga as peças
│   └── exploracao.py        # raio-x dos dados brutos
├── tests/                   # testes automatizados (pytest)
└── requirements.txt
```

Caminho dos dados:
`Fontes -> TratadorCredito -> IntegradorMunicipal -> data/processed -> Analisador -> Dashboard`

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

python src/exploracao.py        # exploração inicial
python src/preparar_dados.py    # gera data/processed (opcional: o dashboard faz isso sozinho)
streamlit run src/app.py        # dashboard
pytest -v                       # testes
```

## Fontes de dados

- **PRODES/INPE**: incremento anual de desmatamento por município.
- **SICOR/BCB**: Matriz de Dados do Crédito Rural.
