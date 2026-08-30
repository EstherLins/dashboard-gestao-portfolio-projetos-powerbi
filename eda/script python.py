# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 150)

# %%
caminho_arquivo = r"C:\Users\esthe\Downloads\dataset_gestao_projetos.xlsx"

tabelas = pd.read_excel(caminho_arquivo, sheet_name=None)

print("Abas encontradas:", list(tabelas.keys()))

# %%
dim_projeto = tabelas["dim_projeto"]
dim_colaborador = tabelas["dim_colaborador"]
dim_calendario = tabelas["dim_calendario"]
fato_tarefas = tabelas["fato_tarefas"]
fato_progresso_semanal = tabelas["fato_progresso_semanal"]
fato_marcos = tabelas["fato_marcos"]
fato_financeiro_mensal = tabelas["fato_financeiro_mensal"]

print("dim_projeto:", dim_projeto.shape)
print("dim_colaborador:", dim_colaborador.shape)
print("dim_calendario:", dim_calendario.shape)
print("fato_tarefas:", fato_tarefas.shape)
print("fato_progresso_semanal:", fato_progresso_semanal.shape)
print("fato_marcos:", fato_marcos.shape)
print("fato_financeiro_mensal:", fato_financeiro_mensal.shape)

# %%
print("fato_financeiro_mensal:")
print(fato_financeiro_mensal.dtypes)

# %%
fato_financeiro_mensal.info()

# %%
fato_financeiro_mensal.head()
fato_financeiro_mensal.sample(10)# %%

# %%
for nome, tabela in tabelas.items():
    if nome != "Leia-me":
        print(f"{nome}: {tabela.duplicated().sum()} linhas duplicadas")
        
# %%
print("projeto_id único?", dim_projeto["projeto_id"].is_unique)
print("colaborador_id único?", dim_colaborador["colaborador_id"].is_unique)
print("tarefa_id único?", fato_tarefas["tarefa_id"].is_unique)
print("progresso_id único?", fato_progresso_semanal["progresso_id"].is_unique)
print("marco_id único?", fato_marcos["marco_id"].is_unique)
print("financeiro_id único?", fato_financeiro_mensal["financeiro_id"].is_unique)

# %%
def checar_orfas(nome_fato, tabela_fato, coluna_fk, dim_projeto_ids):
    orfas = set(tabela_fato[coluna_fk]) - set(dim_projeto_ids)
    print(f"{nome_fato}.{coluna_fk} — chaves órfãs: {len(orfas)}")
    if orfas:
        print("   Valores órfãos encontrados:", orfas)

ids_projeto = dim_projeto["projeto_id"]

checar_orfas("fato_tarefas", fato_tarefas, "projeto_id", ids_projeto)
checar_orfas("fato_progresso_semanal", fato_progresso_semanal, "projeto_id", ids_projeto)
checar_orfas("fato_marcos", fato_marcos, "projeto_id", ids_projeto)
checar_orfas("fato_financeiro_mensal", fato_financeiro_mensal, "projeto_id", ids_projeto)

# %%
print("fato_tarefas (horas):")
print(fato_tarefas[["horas_planejadas", "horas_reais"]].describe())

print("\nfato_progresso_semanal:")
print(fato_progresso_semanal[["horas_trabalhadas_semana", "custo_realizado_semana_rs", "percentual_concluido_acumulado"]].describe())

print("\nfato_financeiro_mensal (custos):")
print(fato_financeiro_mensal[["custo_planejado_rs", "custo_realizado_rs"]].describe())

# %%

print("\nfato_financeiro_mensal (custos):")
print(fato_financeiro_mensal[["custo_planejado_rs", "custo_realizado_rs"]].describe())

# %%
print("Percentual concluído — mínimo:", fato_progresso_semanal["percentual_concluido_acumulado"].min())
print("Percentual concluído — máximo:", fato_progresso_semanal["percentual_concluido_acumulado"].max())

print("\nHoras reais — mínimo:", fato_tarefas["horas_reais"].min())
print("Horas reais — máximo:", fato_tarefas["horas_reais"].max())

print("\nCusto realizado — mínimo:", fato_financeiro_mensal["custo_realizado_rs"].min())
print("Custo realizado — máximo:", fato_financeiro_mensal["custo_realizado_rs"].max())

# %%
print("Status dos projetos:")
print(dim_projeto["status"].value_counts())

print("\nDepartamentos:")
print(dim_projeto["departamento"].value_counts())

print("\nMetodologias:")
print(dim_projeto["metodologia"].value_counts())

print("\nPrioridades:")
print(dim_projeto["prioridade"].value_counts())

# %%
sns.set_theme(style="whitegrid")

# 1. Histograma de orcamento_planejado_rs
plt.figure(figsize=(10, 6))
# bins=10 é um bom ponto de partida para 56 projetos
sns.histplot(data=dim_projeto, x='orcamento_planejado_rs', kde=True, bins=10, color='skyblue')
plt.title('Distribuição do Orçamento Planejado (56 Projetos)')
plt.xlabel('Orçamento (R$)')
plt.ylabel('Quantidade de Projetos')
plt.show()

# %%
# Calcula o método do Z-score ou IQR para detectar outliers matematicamente
Q1 = dim_projeto['orcamento_planejado_rs'].quantile(0.25)
Q3 = dim_projeto['orcamento_planejado_rs'].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = dim_projeto[(dim_projeto['orcamento_planejado_rs'] < limite_inferior) | 
                       (dim_projeto['orcamento_planejado_rs'] > limite_superior)]

print(f"Quantidade de outliers detectados: {len(outliers)}")

# %%
plt.figure(figsize=(12, 6))
sns.boxplot(data=fato_financeiro_mensal, x='categoria_custo', y='custo_realizado_rs', palette='viridis')
plt.title('Dispersão do Custo Realizado por Categoria')
plt.xticks(rotation=45)
plt.ylabel('Custo Realizado (R$)')
plt.show()

#%%
Q1 = fato_financeiro_mensal['custo_realizado_rs'].quantile(0.25)
Q3 = fato_financeiro_mensal['custo_realizado_rs'].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = fato_financeiro_mensal[(fato_financeiro_mensal['custo_realizado_rs'] < limite_inferior) | 
                       (fato_financeiro_mensal['custo_realizado_rs'] > limite_superior)]

print(f"Quantidade de outliers detectados: {len(outliers)}")

# %%
print(fato_financeiro_mensal.sort_values(by='custo_realizado_rs', ascending=False).head(10))

# %%
df_tarefas_com_senioridade = pd.merge(
    fato_tarefas, 
    dim_colaborador[['colaborador_id', 'senioridade']], 
    on='colaborador_id', 
    how='left'
)

# 2. Agora, plotar o boxplot usando este novo DataFrame combinado
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_tarefas_com_senioridade, 
    x='senioridade', 
    y='horas_reais'
)
plt.title('Distribuição de Horas Reais por Senioridade')
plt.xlabel('Senioridade')
plt.ylabel('Horas Reais')
plt.show()

# %%
# Ver os 10 maiores valores para entender se fazem sentido
print(df_tarefas_com_senioridade.sort_values(by='horas_reais', ascending=False).head(10))


# %%
# Calcula o IQR e os limites apenas para a coluna desejada
Q1 = df_tarefas_com_senioridade['horas_reais'].quantile(0.25)
Q3 = df_tarefas_com_senioridade['horas_reais'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

print(f"Limite Inferior: {limite_inferior}")
print(f"Limite Superior: {limite_superior}")

# %%
# 1. Agrupar o custo realizado por projeto na tabela de fatos
# Isso soma todos os gastos mensais de cada 'projeto_id'
custo_por_projeto = fato_financeiro_mensal.groupby('projeto_id')['custo_realizado_rs'].sum().reset_index()

# 2. Fazer o merge com a tabela dim_projeto
# Unimos o custo total calculado com o orçamento planejado que está na dim_projeto
df_comparativo = pd.merge(
    custo_por_projeto, 
    dim_projeto[['projeto_id', 'orcamento_planejado_rs']], 
    on='projeto_id', 
    how='inner'
)

# 3. Calcular o desvio
# Realizado - Planejado: Valor positivo indica estouro, negativo indica economi
df_comparativo['desvio'] = df_comparativo['custo_realizado_rs'] - df_comparativo['orcamento_planejado_rs']

# 4. Plotar o histograma do desvio
plt.figure(figsize=(10, 6))
sns.histplot(df_comparativo['desvio'], kde=True, color='red')

# Adiciona linha vertical no zero para destacar projetos "no alvo"
plt.axvline(0, color='black', linestyle='--', label='Ponto de Equilíbrio')

plt.title('Distribuição do Desvio Orçamentário por Projeto (Realizado - Planejado)')
plt.xlabel('Desvio (R$)')
plt.ylabel('Quantidade de Projetos')
plt.legend()
plt.show()


# %%
# %%
from datetime import datetime

hoje = pd.Timestamp("2025-06-30")  # mesma data de corte usada na geração do dataset

# só avalia projetos cujo prazo planejado já passou (senão não é justo julgar "atraso" ainda)
projetos_avaliaveis = dim_projeto[dim_projeto["data_fim_planejada"] <= hoje].copy()

projetos_avaliaveis["teve_atraso"] = (
    (projetos_avaliaveis["data_fim_real"].isna()) |
    (projetos_avaliaveis["data_fim_real"] > projetos_avaliaveis["data_fim_planejada"])
)

print(f"Total de projetos avaliáveis (prazo já vencido): {len(projetos_avaliaveis)} de {len(dim_projeto)}")
print("\n% de projetos com atraso por metodologia (considerando só quem já venceu o prazo):")
print((projetos_avaliaveis.groupby("metodologia")["teve_atraso"].mean() * 100).round(1).sort_values(ascending=False))


# %%
custo_por_projeto = fato_financeiro_mensal.groupby("projeto_id")["custo_realizado_rs"].sum().reset_index()
custo_por_projeto = custo_por_projeto.merge(
    dim_projeto[["projeto_id", "departamento", "orcamento_planejado_rs"]], on="projeto_id"
)
custo_por_projeto["desvio_pct"] = (
    (custo_por_projeto["custo_realizado_rs"] / custo_por_projeto["orcamento_planejado_rs"]) - 1
) * 100

print(custo_por_projeto.groupby("departamento")["desvio_pct"].mean().sort_values(ascending=False).round(1))

# %%
fato_tarefas_com_colab = fato_tarefas.merge(dim_colaborador[["colaborador_id", "senioridade", "custo_hora_rs"]], on="colaborador_id")
fato_tarefas_com_colab["custo_tarefa"] = fato_tarefas_com_colab["horas_reais"] * fato_tarefas_com_colab["custo_hora_rs"]

print(fato_tarefas_com_colab.groupby("senioridade")["custo_tarefa"].mean().round(2))

# %%
plt.figure(figsize=(8, 6))
sns.scatterplot(data=fato_tarefas, x="horas_planejadas", y="horas_reais", hue="status_tarefa", alpha=0.6)
plt.plot([0, 80], [0, 80], color="gray", linestyle="--", label="Linha ideal (planejado = real)")
plt.xlabel("Horas Planejadas")
plt.ylabel("Horas Reais")
plt.title("Horas Planejadas vs Reais por Tarefa")
plt.legend()
plt.show()

# %%
horas_por_semana = fato_progresso_semanal.groupby("data_semana")["horas_trabalhadas_semana"].sum().reset_index()

plt.figure(figsize=(14, 5))
plt.plot(horas_por_semana["data_semana"], horas_por_semana["horas_trabalhadas_semana"])
plt.xlabel("Semana")
plt.ylabel("Horas trabalhadas (soma de todos os projetos)")
plt.title("Horas Trabalhadas por Semana — Todos os Projetos")
plt.grid(alpha=0.3)
plt.show()


# %%
custo_por_mes = fato_financeiro_mensal.groupby("ano_mes")["custo_realizado_rs"].sum().reset_index()
custo_por_mes = custo_por_mes.sort_values("ano_mes")

plt.figure(figsize=(14, 5))
plt.plot(custo_por_mes["ano_mes"], custo_por_mes["custo_realizado_rs"])
plt.xticks(rotation=45)
plt.xlabel("Mês")
plt.ylabel("Custo Realizado Total (R$)")
plt.title("Custo Realizado Mensal — Todos os Projetos")
plt.grid(alpha=0.3)
plt.show()

# %%
def contar_projetos_ativos(mes_str):
    mes_ts = pd.Timestamp(mes_str + "-01")
    ativos = dim_projeto[
        (dim_projeto["data_inicio_planejada"] <= mes_ts) &
        (
            (dim_projeto["data_fim_real"].isna()) |
            (dim_projeto["data_fim_real"] >= mes_ts)
        ) &
        (dim_projeto["data_fim_planejada"] >= mes_ts - pd.DateOffset(months=1))
    ]
    return len(ativos)

meses_unicos = sorted(fato_financeiro_mensal["ano_mes"].unique())
projetos_ativos_por_mes = pd.DataFrame({
    "ano_mes": meses_unicos,
    "projetos_ativos": [contar_projetos_ativos(m) for m in meses_unicos]
})

plt.figure(figsize=(14, 5))
plt.bar(projetos_ativos_por_mes["ano_mes"], projetos_ativos_por_mes["projetos_ativos"])
plt.xticks(rotation=45)
plt.xlabel("Mês")
plt.ylabel("Projetos Ativos")
plt.title("Quantidade de Projetos Ativos por Mês")
plt.show()

# %%
from statsmodels.tsa.seasonal import seasonal_decompose

serie = horas_por_semana.set_index("data_semana")["horas_trabalhadas_semana"]
serie.index = pd.DatetimeIndex(serie.index)

decomposicao = seasonal_decompose(serie, model="additive", period=52)

fig = decomposicao.plot()
fig.set_size_inches(12, 8)
plt.show()


# %%
