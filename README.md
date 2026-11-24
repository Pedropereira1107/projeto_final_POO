# Crédito Rural e Desmatamento na Amazônia Legal

Projeto final de Programação Orientada a Objetos: um sistema de análise de dados e dashboard interativo
(Python, POO, Pandas, Plotly e Streamlit) para verificar se o crédito rural está associado ao desmatamento
nos estados da Amazônia Legal.
## Justificativa
O crédito rural é a principal politica publica de financiamento do agro, e sabemos que o agro é, se não a principal, uma das atividades que mais causam desmatamento na floresta amazônica. A partir disso, escolhemos este tema pois vimos que essa área sobre financiamento de crédito ao agro era pouco comentada e que poderia ser trabalhada a fim de obter insights importantes sobre um possível fornecimento de crédito aos munícipios que mais desmatam. 

## Fontes de dados
Foram utilizados três fontes de dados: Matriz de Dados de Crédito Rural (MDCR), PRODES e IPCA série SGS 433.
- **Matriz de Dados do Crédito Rural**: Dados mensais do Banco Central datados desde 2013 por município, produto e finalidade (custeio ou investimento), foram usados 2 das 17 consultas (CusteioMunicipioProduto e InvestMunicipioProduto). 
- **PRODES**: Todo o conjunto é baseado em monitoramento por satélite do desmatamento na Amazônia Legal. Os dados coletados para a análise vieram do painel TerraBrasilis, sendo convertidos em arquivos csv.
- **IPCA**: Dados do conjunto série SGS 433 do Banco Central usados para corrigir os valores pela inflação ao longo dos anos.

## Variáveis
- **Crédito**: `cod_ibge`, `municipio`, `uf`, `ano`, `mes`, `ano_prodes`, `finalidade` (custeio ou investimento), `produto`, `valor`, `area_ha`, `atividade`, códigos de programa, fonte e modalidade.
- **PRODES**: `cod_ibge`, `municipio`, `uf`, `ano_prodes`, `incremento_km2` . 
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
