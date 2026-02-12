# =========================
#Imports e configuração
# =========================
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

# ==============================
# Dicionário de labels
# ==============================
labels = {
    "revenue": "Receita",
    "expenditure": "Despesas",
    "net_income": "Lucro Líquido",
    "cash_flow": "Fluxo de Caixa",
    "transaction_volume": "Volume de Transações",
    "processing_time_seconds": "Tempo de Processamento (s)",
    "accuracy_score": "Score de Acurácia"
}
labels_calc = {
    "revenue_calc": "Receita (Recalculada)",
    "expenditure_calc": "Despesas (Recalculadas)",
    "net_income_calc": "Lucro Líquido (Recalculado)"
}
outcome_labels = {
    0: "Falha", 1: "Sucesso", "0": "Falha", "1": "Sucesso"
    }

# =========================
#Conexão com banco
# =========================
@st.cache_resource
def get_connection():
    return sqlite3.connect(
        "data/dados_financeiros.db",
        check_same_thread=False
    )

@st.cache_data
def load_data():
    conn = get_connection()
    query = """
    SELECT
        t.transaction_id,
        t.transaction_date,
        t.transaction_amount,
        t.transaction_outcome,
        t.processing_time_seconds,
        t.accuracy_score,
        t.missing_data_indicator,
        t.normalized_transaction_amount,
        f.revenue,
        f.expenditure,
        f.net_income,
        f.gross_profit,
        f.profit_margin,
        f.cash_flow,
        f.operating_expenses,
        f.debt_to_equity_ratio,
        f.transaction_volume,
        a.account_type_name
    FROM transactions t
    JOIN financial_metrics f
        ON t.transaction_id = f.transaction_id
    JOIN account_type a
        ON t.account_type_id = a.account_type_id
    """
    df = pd.read_sql(query, conn)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df

df = load_data()

# =========================
#Sidebar – filtro de datas
# =========================
st.sidebar.header("Filtros")

modo_dados = st.sidebar.radio(
    "Modo de Análise",
    ["Dados Originais(Banco)", "Dados Recalculados(Análise)"]
)

min_date = df["transaction_date"].min()
max_date = df["transaction_date"].max()

date_range = st.sidebar.date_input(
    "Período",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

start_date = min_date
end_date = max_date


# =========================
#Aplicar filtro
# =========================
df_filtered = df[
    (df["transaction_date"] >= start_date) &
    (df["transaction_date"] <= end_date)
]
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range)

    df_filtered = df[
        (df["transaction_date"] >= start_date) &
        (df["transaction_date"] <= end_date)
    ]
else:
    st.warning("Selecione um intervalo completo de datas")
    df_filtered = df.copy()

# Criar colunas auxiliares para análises temporais
df_filtered = df_filtered.copy()

df_filtered["year_month"] = (
    df_filtered["transaction_date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

df_filtered["year_day"] = df_filtered["transaction_date"]

# =========================
#KPIs FIXAS
# =========================
volume_transacionado = df_filtered["transaction_amount"].sum()

df_cash = df_filtered.copy()

df_cash["cashflow_calc"] = df_cash.apply(
    lambda row: row["transaction_amount"]
    if row["account_type_name"] in ["Revenue", "Asset"]
    else -row["transaction_amount"],
    axis=1
)
cashflow_total = df_cash["cashflow_calc"].sum()

# =========================
# KPIs RECALCULADAS
# =========================


if modo_dados == "Dados Originais(Banco)":
    receita_total = df_filtered["revenue"].sum()
    despesa_total = df_filtered["expenditure"].sum()
    lucro_liquido = df_filtered["net_income"].sum()
    margem_media = df_filtered["profit_margin"].mean()
else:
    receita_total = df_filtered[
     df_filtered["account_type_name"].isin(["Revenue", "Asset"])]["transaction_amount"].sum()
    
    despesa_total = df_filtered[
    df_filtered["account_type_name"].isin(["Expense", "Liability"])]["transaction_amount"].sum()
    lucro_liquido = receita_total - despesa_total
    margem_media = (
        lucro_liquido / receita_total if receita_total > 0 else 0
    )
    


#Exibição das KPIs Fixas 
st.subheader("KPIs Fixas")
col1, col2 = st.columns(2)

col1.metric(
    "Volume Total Transacionado",
    f"R$ {volume_transacionado:,.2f}"
)

col2.metric(
    "Fluxo de Caixa Líquido do Período",
    f"R$ {cashflow_total:,.2f}"
)


#Botões de KPI
st.divider()
st.subheader("KPIs Dinâmicas")
st.caption(f"Modo ativo: {modo_dados}")

kpis = {
    "Receita Total": "show_revenue",
    "Despesa Total": "show_expense",
    "Lucro Líquido": "show_profit",
    "Margem Média": "show_margin",
}

for key in kpis.values():
    if key not in st.session_state:
        st.session_state[key] = False

cols = st.columns(len(kpis))

for col, (label, state_key) in zip(cols, kpis.items()):
    if col.button(label):
        st.session_state[state_key] = not st.session_state[state_key]


#Exibição dinâmica dos KPIs
st.divider()

metric_cols = st.columns(5)
idx = 0

if st.session_state.show_revenue:
    metric_cols[idx].metric("Receita Total", f"R$ {receita_total:,.2f}")
    idx += 1

if st.session_state.show_expense:
    metric_cols[idx].metric("Despesa Total", f"R$ {despesa_total:,.2f}")
    idx += 1

if st.session_state.show_profit:
    metric_cols[idx].metric("Lucro Líquido", f"R$ {lucro_liquido:,.2f}")
    idx += 1

if st.session_state.show_margin:
    metric_cols[idx].metric("Margem Média", f"{margem_media:.2%}")
    idx += 1

# =========================
# SEÇÃO: ANÁLISE FINANCEIRA
# =========================
st.divider()
st.header("📊 Desempenho Financeiro e Sustentabilidade")

st.subheader("📈 Evolução Mensal de Receita, Despesas e Lucro Líquido")
st.caption("Apresenta a evolução temporal dos principais indicadores financeiros, permitindo identificar tendências de crescimento, retração ou estabilidade.")

df_time = df_filtered.groupby(
    pd.Grouper(key="transaction_date", freq="ME")
)[["revenue", "expenditure", "net_income"]].sum().reset_index()

df_time = df_time.rename(columns={
    "revenue": "Receita",
    "expenditure": "Despesas",
    "net_income": "Lucro Líquido"
})

st.line_chart(df_time.set_index("transaction_date"))


# ==============================
# 📈 Variação Percentual do Lucro
# ==============================
st.subheader("📊 Variação Percentual do Lucro Líquido")
st.caption("Evidencia a aceleração ou desaceleração do lucro ao longo do tempo, destacando períodos de expansão ou contração financeira.")

df_time["Lucro Var %"] = df_time["Lucro Líquido"].pct_change() * 100

st.line_chart(df_time["Lucro Var %"])


# ==============================
# 💳 Análise Debt-to-Equity Ratio
# ==============================

st.subheader("💳 Evolução do Debt-to-Equity Ratio")
st.caption("Mostra o nível médio de alavancagem financeira, indicando o grau de dependência de capital de terceiros ao longo do período.")


de_ratio_mean = df_filtered["debt_to_equity_ratio"].mean()

st.metric("Debt-to-Equity Médio", f"{de_ratio_mean:.2f}")

st.line_chart(
    df_filtered.groupby(
        pd.Grouper(key="transaction_date", freq="ME")
    )["debt_to_equity_ratio"].mean()
)

# =========================
# Insight
# =========================

st.subheader("Insight Financeiro")
st.write("""
A análise temporal demonstra que o desempenho financeiro apresenta variações relevantes conforme o período analisado. 
Momentos de crescimento do lucro alternam com períodos de retração, indicando ciclos financeiros que exigem monitoramento contínuo.

A estrutura de capital, medida pelo Debt-to-Equity Ratio, reforça a importância do equilíbrio entre financiamento próprio e de terceiros para manter sustentabilidade no longo prazo.

Esses indicadores, analisados em conjunto, permitem avaliar não apenas o resultado momentâneo, mas a consistência e estabilidade financeira da empresa.
""")


# =========================
# SEÇÃO: FLUXO DE CAIXA
# =========================
st.divider()
st.header("💸 Liquidez e Geração de Caixa")

st.subheader("📊 Fluxo de Caixa ao Longo do Tempo")
st.caption("Apresenta a geração líquida de caixa por período, evidenciando a capacidade operacional de conversão de receitas em recursos disponíveis.")

df_cash_time = df_cash.groupby(
    pd.Grouper(key="transaction_date", freq="ME")
)["cashflow_calc"].sum().reset_index()

df_cash_time = df_cash_time.rename(
    columns={"cashflow_calc": "Fluxo de Caixa"}
)
st.bar_chart(
    df_cash_time.set_index("transaction_date")
)


# ==============================
# 🔎 Correlação Cash Flow x Net Income
# ==============================

st.subheader("📈 Relação entre Fluxo de Caixa e Lucro Líquido")
st.caption("Avalia se o resultado contábil está sendo efetivamente convertido em geração real de caixa.")
st.caption("Correlação próxima de 1 indica forte relação positiva; valores próximos de 0 indicam baixa relação linear.")


correlation_cf = df_filtered["cash_flow"].corr(df_filtered["net_income"])

st.metric("Correlação", f"{correlation_cf:.2f}")

st.scatter_chart(
    df_filtered,
    x="cash_flow",
    y="net_income"
)

# =========================
# Insight
# =========================

st.subheader("Insight de Liquidez")
st.write("""
O fluxo de caixa revela a capacidade da empresa de sustentar suas operações e investimentos com recursos próprios.

A correlação entre lucro e geração de caixa indica o nível de eficiência financeira na conversão de resultado contábil em liquidez. 
Divergências relevantes podem sinalizar riscos relacionados a capital de giro ou gestão financeira.
""")


# =========================
# SEÇÃO: EFICIÊNCIA OPERACIONAL
# =========================
st.divider()
st.header("⏱️ Eficiência e Desempenho Operacional")

# ==============================
# 🔄 Relação entre Volume e Tempo
# ==============================

st.subheader("🔄 Relação entre Volume de Transações e Tempo de Processamento")
st.caption("Analisa se o aumento do volume operacional impacta diretamente o tempo médio de processamento das transações.")

df_oper = df_filtered[[
    "transaction_volume",
    "processing_time_seconds"
]].rename(columns={
    "transaction_volume": "Volume de Transações",
    "processing_time_seconds": "Tempo de Processamento (s)"
})

st.scatter_chart(df_oper)


# ==============================
# 📊 Indicadores Estatísticos de Processamento
# ==============================

st.subheader("📊 Indicadores de Desempenho Operacional")
st.caption("Resumo estatístico da eficiência do processamento e da relação entre demanda e tempo de execução.")

avg_processing_time = df_filtered["processing_time_seconds"].mean()

correlation_vol_time = df_filtered["transaction_volume"].corr(
    df_filtered["processing_time_seconds"]
)

col1, col2 = st.columns(2)

with col1:
    st.metric("Tempo Médio (segundos)", f"{avg_processing_time:.2f}")

with col2:
    st.metric("Correlação Volume x Tempo", f"{correlation_vol_time:.2f}")


st.caption("Correlação positiva indica que maior volume tende a aumentar o tempo de processamento; valores próximos de 0 indicam baixa relação linear.")


# ==============================
# 🚨 Tempo de Processamento por Resultado
# ==============================

st.subheader("🚨 Tempo Médio por Resultado da Transação")
st.caption("Compara o tempo médio entre transações bem-sucedidas e falhas, permitindo identificar possíveis gargalos operacionais.")

processing_by_outcome = df_filtered.groupby("transaction_outcome")[
    "processing_time_seconds"
].mean()

st.bar_chart(processing_by_outcome)


# =========================
# Insight
# =========================

st.subheader("Insight Operacional")
st.write("""
A análise indica como o sistema reage ao aumento da demanda operacional.

O tempo médio de processamento fornece uma visão geral da eficiência do sistema,
enquanto a correlação entre volume e tempo revela o grau de escalabilidade da operação.

Diferenças significativas no tempo médio entre transações bem-sucedidas e falhas
podem indicar gargalos específicos no fluxo de validação ou execução,
sinalizando oportunidades de otimização operacional.
""")


# =========================
# SEÇÃO: QUALIDADE DAS TRANSAÇÕES
# =========================
st.divider()
st.header("✅ Qualidade e Confiabilidade das Transações")

# =========================
# Pie: Taxa de Sucesso vs Falha
# =========================
st.subheader("📊 Distribuição de Sucesso e Falha")
st.caption("Apresenta a proporção entre transações concluídas com sucesso e aquelas que resultaram em falha.")

outcome_counts = (
    df_filtered["transaction_outcome"]
    .value_counts()
    .reset_index()
)

outcome_counts.columns = ["Resultado", "Quantidade"]
outcome_counts["Resultado"] = outcome_counts["Resultado"].map(outcome_labels)

fig_pie = px.pie(
    outcome_counts,
    values="Quantidade",
    names="Resultado",
    title="Distribuição dos Resultados das Transações",
    hole=0.4, # Adicionei um pouco de hole para um visual "Donut" moderno
    color="Resultado",
    color_discrete_map={"Falha": "#FF0000", "Sucesso": "#2BB837"}
)
st.plotly_chart(fig_pie, use_container_width=True)

# ==============================
# 📂 Impacto de Dados Ausentes nas Falhas
# ==============================

st.subheader("📂 Impacto de Dados Ausentes nas Transações")
st.caption("Avalia se a presença de dados incompletos está associada a maior taxa de falhas.")


missing_vs_outcome = pd.crosstab(
    df_filtered["missing_data_indicator"],
    df_filtered["transaction_outcome"],
    normalize="index"
)

st.bar_chart(missing_vs_outcome)

# ==============================
# 📦 Evolução do Volume de Transações
# ==============================

st.subheader("📦 Evolução do Volume de Transações")
st.caption("Mostra a variação do volume operacional ao longo do tempo, permitindo identificar picos de atividade.")


volume_time = df_filtered.groupby(
    pd.Grouper(key="transaction_date", freq="ME")
)["transaction_volume"].sum()


st.line_chart(volume_time)


# ==============================
# 💰 Relação Volume x Lucro
# ==============================

st.subheader("💰 Relação entre Volume de Transações e Lucro")
st.caption("Analisa se o aumento no volume operacional está efetivamente associado ao crescimento da lucratividade.")


correlation_vol_profit = df_filtered["transaction_volume"].corr(
    df_filtered["net_income"]
)

st.metric("Correlação Volume x Lucro", f"{correlation_vol_profit:.2f}")

st.scatter_chart(
    df_filtered,
    x="transaction_volume",
    y="net_income"
)


# =========================
# Insight
# =========================
st.subheader("Insight de Qualidade")
st.write("""
A proporção entre transações bem-sucedidas e falhas fornece um indicador direto
de estabilidade operacional.

A análise do impacto de dados ausentes sugere que a qualidade da informação pode
influenciar diretamente o sucesso das transações, reforçando a importância de
processos robustos de validação e governança de dados.

Além disso, a relação entre volume e lucro permite avaliar se o crescimento operacional
está sendo convertido em desempenho financeiro sustentável.
""")


# =========================
# SEÇÃO: CONCLUSÃO EXECUTIVA
# =========================
st.divider()
st.header("📌 Conclusão Executiva")

st.write("""
A análise integrada dos indicadores financeiros, operacionais e de qualidade
demonstra que o desempenho da empresa apresenta ciclos de expansão e retração
ao longo do período analisado.

Observa-se que variações no volume operacional impactam diretamente a eficiência
e a geração de resultados, reforçando a necessidade de monitoramento contínuo
e planejamento estratégico baseado em dados.

A consistência entre lucro e geração de caixa, bem como a estabilidade na taxa
de sucesso das transações, são fatores críticos para a sustentabilidade
financeira e operacional no longo prazo.

Essas evidências demonstram o valor da análise de dados estruturados como
suporte à tomada de decisão orientada por indicadores objetivos.
""")

