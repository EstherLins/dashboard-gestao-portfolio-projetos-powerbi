# Dashboard de Gestão de Portfólio de Projetos — Power BI

> Painel de PMO construído do zero: dataset sintético, ETL, modelagem dimensional, DAX e storytelling de dados, simulando a rotina de decisão de um portfólio real de projetos.

## Sobre o projeto

Este projeto simula o cenário de um PMO (Project Management Office) sem visão consolidada de orçamento, prazo e execução. Em vez de usar um dataset pronto, construí a base de dados sintética, tratei e modelei os dados, e desenvolvi um relatório de 6 páginas no Power BI capaz de responder:

- Os projetos estão dentro do orçamento?
- Os prazos e marcos estão sendo cumpridos?
- O ritmo de execução está saudável?
- Onde está o risco agora, e em qual projeto especificamente?

## Ordem do processo

O relatório não nasceu do canvas do Power BI. Foi construído nessa ordem:

1. **ETL (Power Query)** — tratamento de tipos, nulos, chaves órfãs e padronização de colunas antes de qualquer relacionamento entrar no modelo.
2. **EDA (Python)** — análise exploratória no VS Code com extensão Jupyter, usando pandas, matplotlib, seaborn e statsmodels. Histogramas com KDE, boxplots com detecção de outliers por IQR, scatter plots e decomposição de série temporal (tendência, sazonalidade, resíduo).
3. **Modelagem dimensional** — esquema estrela com múltiplas tabelas fato (constelação de fatos), cardinalidade e direção de filtro testadas relacionamento a relacionamento.
4. **Definição de objetivo e perguntas** — com o dado já entendido, defini o que cada página do relatório precisava responder antes de escrever qualquer medida.
5. **DAX** — SPI, CPI, taxa de acerto orçamentário, burndown por projeto, entre outras medidas.
6. **Visualizações** — 6 páginas organizadas por nível de decisão: visão executiva → financeiro / marcos / execução → drill-through por projeto individual.
7. **Validação** — revisão de relacionamentos, medidas e filtros de cada página até garantir que os números batiam entre si.

## Modelo de dados

Esquema estrela com 3 dimensões e 4 tabelas fato:

| Tabela | Tipo | Granularidade |
|---|---|---|
| `dim_projeto` | Dimensão | 1 linha por projeto |
| `dim_colaborador` | Dimensão | 1 linha por colaborador |
| `dim_calendario` | Dimensão | 1 linha por dia |
| `fato_tarefas` | Fato | 1 linha por tarefa |
| `fato_progresso_semanal` | Fato | 1 linha por projeto/semana |
| `fato_marcos` | Fato | 1 linha por marco |
| `fato_financeiro_mensal` | Fato | 1 linha por projeto/mês/categoria de custo |

O modelo inclui uma relação de floco de neve (`dim_projeto` → `dim_colaborador`, via gerente), mantida inativa e ativada pontualmente via `USERELATIONSHIP` em medidas específicas.

## Um bug, uma lição

Durante a construção das medidas de burndown, uma função `ALL()` mal posicionada dentro de um `FILTER()` fazia o "Escopo Acumulado" somar tarefas do portfólio inteiro (~1.700) mesmo com o relatório filtrado para um único projeto (~25 tarefas). A causa: `ALL()` remove todos os filtros da tabela em que é aplicado — inclusive o de projeto, que chegava até ali via relacionamento. A correção envolveu reestruturar o filtro para atuar apenas sobre a tabela de calendário, deixando o filtro de projeto propagar normalmente. Esse é o tipo de erro que não gera mensagem de erro nenhuma — o DAX sempre devolve um número, e cabe à análise garantir que é o número certo.

## Métricas principais (DAX)

- **SPI** (Schedule Performance Index) — ritmo de entrega de tarefas frente ao planejado
- **CPI** (Cost Performance Index) — valor agregado por real gasto
- **Taxa de acerto orçamentário** — aderência entre custo planejado e realizado
- **Burndown** — escopo acumulado, tarefas restantes reais e ideais, por projeto
- Indicadores de status textual (avisos) para cada métrica, com tratamento de projetos concluídos/cancelados

## Estrutura do relatório

1. **Visão Executiva** — panorama geral, sem filtro de projeto
2. **Financeiro** — custo real x planejado, desvio orçamentário, Pareto de causas de estouro
3. **Marcos** — cumprimento de prazos por criticidade
4. **Execução** — progresso semanal, tarefas por fase/status, burndown
5. **Projeto Individual** — drill-through com detalhamento completo de um projeto
6. **Pessoas** — carga e custo por colaborador e senioridade

## Stack técnica

`Power Query` · `Python (pandas, seaborn, matplotlib, statsmodels)` · `DAX` · `Power BI` · `Modelagem dimensional`

## Estrutura do repositório

```
├── dataset/                  # Dataset sintético (Excel) com as 7 tabelas
├── eda/                      # Notebook/script Python da análise exploratória
├── powerbi/                  # Arquivo .pbix do relatório
├── docs/                     # Prints do modelo de dados, medidas DAX e páginas do relatório
└── README.md
```

## Como reproduzir

1. Clone o repositório
2. Abra `dataset/dataset_gestao_projetos.xlsx` — todas as 7 tabelas já vêm documentadas em uma aba "Leia-me"
3. Abra `powerbi/relatorio.pbix` no Power BI Desktop
4. Para reproduzir a EDA, abra `eda/` no VS Code (extensão Jupyter) com um ambiente Python que tenha pandas, matplotlib, seaborn e statsmodels instalados

## Portfólio

Projeto documentado com mais detalhes, vídeo do relatório e prints do processo em: [esther-lins.vercel.app](https://esther-lins.vercel.app/)

---

Projeto pessoal desenvolvido por Esther Lins como prática de análise de dados aplicada à gestão de projetos.
