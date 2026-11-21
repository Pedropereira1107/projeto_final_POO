# Contexto do projeto: Crédito Rural e Desmatamento na Amazônia Legal

> Documento de contexto para o Claude Code. Pode ser salvo na raiz do repositório como `CLAUDE.md`.
> Reúne as decisões e descobertas feitas até 21/11/2026, durante a definição do projeto e a coleta dos dados.

## 1. O trabalho

Trabalho final do semestre: **Sistema de Análise de Dados e Dashboard Interativo com Python, Programação Orientada a Objetos e Pandas.**

Requisitos do enunciado:
- Aplicação em Python que **obtém dados de uma fonte pública**, processa e analisa com **Pandas** e apresenta os resultados em um **dashboard dinâmico e interativo**.
- Uso de **POO**: classes, objetos, atributos e métodos.
- Aplicação dos **princípios SOLID**.
- Versionamento com **Git/GitHub**, além de documentação e organização do projeto.
- Simular uma solução de apoio à tomada de decisão.

A Etapa 1 (definição do problema e planejamento) já foi redigida. O ambiente do aluno é **Windows**, e a pasta do projeto é `Projeto_Final_POO`. Escreva o código, os comentários e a documentação em **português**.

## 2. Tema, problema e perguntas

**Tema:** crédito rural e desmatamento na Amazônia Legal, com uma análise integrada de dados do Banco Central (BCB) e do INPE.

**Problema:** não está claro se o crédito rural, a principal política de financiamento do agro, está indo para os municípios da Amazônia Legal que mais desmatam. As duas bases são públicas, mas separadas, e o projeto as integra por município e ano.

**Objetivo geral:** uma aplicação Python orientada a objetos que coleta, trata e integra crédito rural e desmatamento e apresenta os resultados em um dashboard interativo.

**Perguntas de análise (escopo final):**
1. Os municípios que mais recebem crédito rural, principalmente para a pecuária bovina, também estão entre os que mais desmatam?
2. Nos municípios com mais desmatamento, quais finalidades (custeio ou investimento) e quais produtos concentram o crédito?
3. Os municípios com pouco desmatamento recebem mais ou menos crédito do que os municípios críticos?
4. Como o crédito rural e o desmatamento evoluíram juntos, de 2013 a 2025, em cada estado da Amazônia Legal?

**Recorte:** os 772 municípios oficiais dos 9 estados da Amazônia Legal (AC, AM, AP, MA, MT, PA, RO, RR, TO). O Maranhão está só parcialmente incluído.

**Limitações a registrar no relatório:**
- **Correlação, não causalidade:** o projeto aponta sobreposições e padrões, mas não prova que o crédito causa desmatamento.
- **Localização:** o município do contrato de crédito pode não ser o local exato do desmatamento.
- **Valores nominais:** os valores de crédito ainda precisam ser corrigidos pelo IPCA.
- **Fonte instável:** a API do BCB falha com frequência, e a coleta foi feita com novas tentativas, download em partes e cópia local.

## 3. Fontes de dados

### 3.1 Matriz de Dados do Crédito Rural (MDCR / SICOR), Banco Central

- **Catálogo:** https://dadosabertos.bcb.gov.br/dataset/matrizdadoscreditorural
- **API OData:** `https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata/<Consulta>?$format=json&$filter=...`
- **Consultas usadas: só 2 das 17.** As outras 15 são recortes redundantes (UF, região, faixa, banco, gênero).
  - `CusteioMunicipioProduto`
  - `InvestMunicipioProduto`

**Campos e particularidades verificados na API:**

| Campo | Custeio | Investimento | Observação |
|---|---|---|---|
| Código IBGE (7 dígitos) | `codIbge` | **não existe** | Liga com o PRODES |
| Código cadmu (5 dígitos, interno do BCB) | `codCadMu` | `cdMunicipio` | **Não é o código IBGE** |
| Valor (R$) | `VlCusteio` | `VlInvest` | |
| Área (ha) | `AreaCusteio` | `AreaInvest` | |
| Produto | `nomeProduto`, `cdProduto` | idem | `nomeProduto` vem com aspas extras: `"\"BOVINOS\""` |
| Data | `AnoEmissao`, `MesEmissao` | idem | Texto, com zero à esquerda (`'01'`) |
| Outros | `cdPrograma`, `cdSubPrograma`, `cdFonteRecurso`, `cdModalidade`, `cdTipoSeguro`, `Atividade`, `cdEstado`, `Municipio` | idem | |

- **Código IBGE do investimento:** como a consulta de investimento não traz esse código, use a de custeio como tabela de correspondência cadmu → IBGE. Sobram 210 linhas sem correspondência (R$ 6,4 mi), que são descartadas.
- **`cdEstado`:** é um código próprio do BCB, não o código de UF do IBGE. Para obter a UF, use os 2 primeiros dígitos de `codIbge`.
  - Códigos `cdEstado` dos 9 estados: RO=22, AC=1, AM=3, RR=23, PA=15, AP=4, TO=28, MA=11, MT=14.
- **`Atividade`:** aparentemente 1 = agrícola e 2 = pecuária. Ainda não confirmado na documentação.
- **O que funciona na API:** `$filter` com `eq`, `and` e `or`, e `$top`.
- **O que não funcionou:** `$select`, `$count` e `startswith`, que retornaram erro 500.
- **Instabilidade:** a API responde com frequência "Erro desconhecido" (500) e rejeita pedidos simultâneos. A coleta que funcionou foi **sequencial**, um mês por pedido, com 3 s de pausa e novas tentativas com espera crescente.
- **Volume:** cerca de 24 mil linhas por mês no Brasil inteiro. Os links "JSON" da página do catálogo pedem a base inteira e estouram o tempo limite, então não devem ser usados.
- **Anomalia real da fonte:** de março a junho de 2016 há muito menos registros nas duas consultas. Isso foi conferido com uma nova consulta e não é erro de download. Vale citar no relatório.

### 3.2 PRODES, INPE (desmatamento)

- **Página no dados.gov.br:** https://dados.gov.br/dados/conjuntos-dados/prodes. Os 46 recursos são todos mapas (SHP, GPKG, TIFF), e **nenhum** é usado. O shapefile de incremento da Amazônia Legal vai só até 2020.
- **Fonte usada:** o painel do TerraBrasilis em https://terrabrasilis.dpi.inpe.br/app/dashboard/deforestation/biomes/legal_amazon/increments
  - O painel carrega estes JSONs, dos quais o CSV foi montado:
    - `https://terrabrasilis.dpi.inpe.br/app/prodes/dashboard/deforestation/files/data/prodes_legal_amazon.json`: períodos → features (`loi`, `loiname` = gid, `areas[].area` em km²). Para municípios, `loi = 2`.
    - `https://terrabrasilis.dpi.inpe.br/app/prodes/dashboard/deforestation/files/config/loinames/prodes_legal_amazon.json`: nomes. A camada `mun` tem 805 municípios com `codibge`, dos quais 772 estão nos 9 estados.
  - O botão "Download CSV" do painel não funcionou no navegador usado, e não existe API oficial para essa tabela. Por isso a `FontePRODES` deve **ler o arquivo local**, o que deve ser documentado.
- **Ano PRODES:** vai de **agosto a julho** e é rotulado pelo ano final. Exemplo: ago/2020 a jul/2021 = PRODES 2021.
- **Período 2026:** os dados de 2025/2026 são **preliminares** e foram excluídos.
- **Linha "2007":** é o acumulado de 1500 a 2007, não um incremento anual.
- **Validação:** os totais anuais batem com o painel (2013: 5.393 km²; 2021: 12.406 km²; 2025: 5.257 km²).

### 3.3 IPCA (correção pela inflação, ainda não implementada)

- **Série SGS 433** (IPCA, variação mensal em %), da API do BCB: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json`. Ela não aparece como conjunto próprio no portal de dados abertos, e o endereço ainda não foi testado.
- **Uso:** montar o índice acumulado com `(1 + valor/100).cumprod()` e deflacionar: `valor_real = valor_nominal * indice[mês_ref] / indice[mês_contrato]`.
- **Alternativa:** a tabela 1737 do IBGE/SIDRA, que já traz o número-índice.

## 4. Arquivos de dados (já baixados, em `data/`)

Nenhum arquivo bruto deve ser alterado: todo tratamento gera arquivos novos em `data/processed/`.

| Arquivo | Conteúdo |
|---|---|
| `mdcr_custeio_AAAA_amazonia_legal.csv` (2013 a 2025, 13 arquivos) | Saída bruta da API, só os 9 estados, todas as colunas. 393.528 linhas no total. |
| `mdcr_investimento_AAAA_amazonia_legal.csv` (2013 a 2025, 13 arquivos) | Idem. 661.363 linhas no total. |
| `prodes_incremento_municipios_amazonia_legal.csv` | Colunas `codibge, municipio, uf, ano_prodes, inicio_periodo, fim_periodo, incremento_km2`. Uma linha por município com desmatamento em cada ano (677 municípios). |
| `prodes_legal_amazon_bruto.json` | JSON original de dados do painel. |
| `prodes_legal_amazon_nomes_bruto.json` | JSON original de nomes do painel. Tem a **lista oficial de municípios**, necessária para o recorte. |

Todos os 26 CSVs de crédito foram conferidos: 12 meses por arquivo, sem duplicatas.

**Custeio nominal na Amazônia Legal, como referência:** R$ 9,0 bi (2013), 22,4 bi (2020), 48,1 bi (2023), 40,6 bi (2025). O MT concentra a maior parte, e BOVINOS é o produto mais frequente.

## 5. Script já pronto: `preparar_dados.py`

Foi testado com os dados reais e roda em cerca de 6 s. Contém duas classes, que devem depois migrar para `src/tratamento/`.

**`TratadorCredito`** lê os 26 CSVs e:
- padroniza os nomes das colunas (`valor`, `area_ha`, `cod_ibge`, `cod_cadmu`, `produto` etc.);
- cria a coluna `finalidade`;
- preenche o código IBGE do investimento pela correspondência com o cadmu;
- limpa as aspas de `produto`;
- cria `uf` e `ano_prodes` (`ano + 1` quando o mês é 8 ou maior).

**`IntegradorMunicipal`**:
- monta uma grade completa com os 772 municípios × anos PRODES 2014–2025, usando a lista oficial do JSON de nomes;
- agrega o crédito (total, custeio, investimento, bovinos, registros) e junta com `incremento_km2`;
- preenche ausências com 0;
- exclui 2013 (crédito incompleto para o ano PRODES) e 2026 (preliminar);
- no método `agregar_por_produto()`, gera a tabela leve da pergunta 2.

**Saídas em `data/processed/`:**

| Arquivo | Tamanho | Conteúdo |
|---|---|---|
| `credito_rural_amazonia_legal.csv` | 1.054.681 linhas, ~119 MB | Inclui a coluna `amazonia_legal`: 56.489 operações são de municípios do leste do MA, fora da Amazônia Legal. |
| `base_municipio_ano.csv` | 9.264 linhas (772 × 12) | Colunas `cod_ibge, municipio, uf, ano_prodes, incremento_km2, credito_total, credito_custeio, credito_investimento, credito_bovinos, registros`. |
| `credito_municipio_produto.csv` | 144.757 linhas, ~10 MB | Colunas `cod_ibge, uf, ano_prodes, finalidade, produto, valor, area_ha, registros`. Só municípios oficiais, anos 2014–2025. |

**Conferências feitas:**
- O desmatamento total da base integrada (98.615 km²) bate com o PRODES original.
- A soma de `credito_municipio_produto.csv` bate centavo a centavo com `base_municipio_ano.csv`: R$ 498,45 bi no total e R$ 177,62 bi em bovinos, valores nominais.

**Uso das saídas por pergunta:**
- **`base_municipio_ano.csv`:** perguntas 1, 3 e 4.
- **`credito_municipio_produto.csv`:** pergunta 2. Cruze pelo `cod_ibge` com a lista de municípios críticos tirada da base.
- **`credito_rural_amazonia_legal.csv`:** só etapa intermediária. **O dashboard não deve ler esse arquivo** (1 milhão de linhas, lento no Streamlit).
- **Os arquivos em `data/processed/` são um cache gerado pela aplicação.** A geração deve fazer parte do fluxo POO (Fonte → Tratador → Integrador → Analisador → Dashboard), e não ser um passo manual.
- **Nomes de produto a padronizar:** alguns nomes aparecem em variantes (ex.: `PISCICULTURA` e `PISCICULTURA (CULTIVO DE PEIXE)`). Antes dos rankings por produto, vale agrupar pelo `cod_produto` ou uniformizar esses nomes.

## 6. Arquitetura planejada (POO + SOLID)

| Classe | Responsabilidade | SOLID |
|---|---|---|
| `FonteDados` (abstrata, método `coletar()`) | Contrato comum das fontes | D, L |
| `FonteSICOR`, `FontePRODES`, `FonteIPCA` | Uma fonte cada. A `FontePRODES` lê o arquivo local. | O: nova fonte = nova classe |
| `TratadorDados` (hoje `TratadorCredito`) | Limpeza, tipos, códigos IBGE, IPCA | S |
| `IntegradorMunicipal` | Junção por município e ano PRODES | S |
| `AnalisadorCreditoDesmatamento` | Indicadores, rankings e séries que respondem às perguntas | S |
| `Dashboard` (Streamlit) | Filtros por estado, ano, finalidade e produto; mapa, rankings, séries | I: depende só do analisador |

**Ferramentas:** Python 3, pandas, requests, plotly, streamlit, pytest, Git e GitHub.

**Estrutura sugerida:**
```
Projeto_Final_POO/
├── src/
│   ├── fontes/        # FonteDados, FonteSICOR, FontePRODES, FonteIPCA
│   ├── tratamento/    # TratadorDados, IntegradorMunicipal
│   ├── analise/       # AnalisadorCreditoDesmatamento
│   └── dashboard/     # app Streamlit
├── data/              # brutos (não versionar) + data/processed/
├── tests/
├── requirements.txt
└── README.md
```

## 7. Próximos passos

1. Rodar `preparar_dados.py` e conferir as saídas.
2. **Antes do primeiro commit**, colocar `data/` no `.gitignore`: o arquivo de crédito tem 119 MB e o GitHub recusa arquivos acima de 100 MB. Explicar no README como obter os dados.
3. Implementar a `FonteIPCA` e deflacionar os valores de crédito, escolhendo um mês de referência (por exemplo, dez/2025).
4. Migrar o script para a arquitetura em `src/`, com a classe abstrata `FonteDados` e as implementações concretas.
5. Implementar o `AnalisadorCreditoDesmatamento`. Definir o critério de "município crítico" (por exemplo, o top 10% em desmatamento acumulado 2014–2025) e responder às 4 perguntas.
6. Montar o dashboard em Streamlit.
7. Escrever testes com pytest para o tratamento e a integração, e documentar no README.

## 8. Cuidados para o Claude Code

- Use **sempre o código IBGE como chave**, nunca o nome do município.
- Leia os códigos com `dtype=str`, para preservar os zeros à esquerda.
- Não use o `cdEstado` do BCB como código de UF.
- Respeite o ano PRODES de agosto a julho ao comparar crédito com desmatamento.
- Se for coletar de novo da API do BCB, faça pedidos sequenciais com pausa e novas tentativas. Pedidos simultâneos provocam erro 500.

