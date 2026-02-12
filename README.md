# 📊 Projeto de Análise de Dados — Controle Financeiro Corporativo
Este projeto foi desenvolvido como parte da minha jornada de aprendizado em Análise de Dados, aplicando conceitos de modelagem relacional, SQL e visualização de dados em um cenário simulado de negócio.

A iniciativa simula um cenário corporativo de **análise financeira e operacional** em uma empresa fictícia do setor FinTech, com o objetivo de demonstrar habilidades práticas em **SQL, modelagem de dados, análise exploratória, KPIs e visualização de dados**.

A solução foi construída seguindo um fluxo profissional de **Data Analytics**, desde o entendimento do negócio até a entrega de insights acionáveis para tomada de decisão.

---

## 🧠 Contexto de Negócio

A **TechFinance XPTO Solutions S.A.** é uma empresa fictícia de médio porte do setor de tecnologia financeira que passou por crescimento acelerado nos últimos anos.

Apesar da expansão, a liderança enfrentou dificuldades para avaliar:
- A real saúde financeira da empresa
- A sustentabilidade do fluxo de caixa
- A eficiência operacional das transações
- A qualidade e confiabilidade dos dados

Diante disso, foi iniciado este projeto de Análise de Dados para transformar dados financeiros e operacionais em **informações claras, confiáveis e estratégicas**.

📄 Contexto completo:  
👉 [Documentação de Contexto](docs/context.md)

---

## 🎯 Objetivos do Projeto

- Avaliar a performance financeira da empresa
- Analisar o fluxo de caixa e identificar períodos críticos
- Identificar tendências ao longo do tempo
- Medir eficiência operacional das transações
- Avaliar qualidade e confiabilidade dos dados
- Apoiar a tomada de decisão estratégica baseada em dados

---

## 🛠️ Tecnologias Utilizadas

- **Python** (pandas, sqlite3)
- **SQLite**
- **SQL**
- **Streamlit** (Dashboard interativo)
- **Modelagem de Dados** (MER e Modelo Lógico)
- **Git & GitHub**

---

## 🗂️ Estrutura do Projeto

```text
financial-data-analysis/
│
├── app.py                 # Aplicação Streamlit
├── README.md
├── requirements.txt
│
├── data/
│   ├── accounting_data.csv
│   └── dados_financeiros.db
│
├── docs/
│   ├── context.md
│   └── data_dictionary.md
│
├── scripts/
│   └── load_data.py
│
├── sql/
│   ├── dados_financeiros.sql
│   ├── Modelo Entidade Relacionamento.png
│   └── Modelo Logico_DBML.png
```
## 🧪 Pipeline de Análise

1. Entendimento do negócio e definição das perguntas
2. Modelagem conceitual e lógica dos dados
3. Criação do banco de dados relacional (SQLite)
4. Carga e tratamento dos dados via Python
5. Construção de consultas e KPIs com SQL
6. Visualizações e insights com Streamlit
7. Storytelling e entrega executiva


## 📘 Nota Metodológica

Durante o desenvolvimento, foi identificado que algumas métricas financeiras apresentavam divergências conceituais quando comparadas às regras contábeis tradicionais.

Para garantir maior transparência analítica, o dashboard permite dois modos de visualização:

Dados Originais (Banco): utiliza os valores conforme armazenados no dataset.

Dados Recalculados (Análise): recalcula métricas financeiras com base em receita, despesa e tipo de conta (account_type), assegurando consistência lógica entre os indicadores.

A comparação entre os dois modos permite identificar possíveis inconsistências estruturais e reforça a importância da governança e validação de dados em ambientes corporativos.


## 📊 KPIs e Métricas Implementadas

O dashboard contempla os seguintes indicadores:

### 📈 Financeiro
- Receita Total
- Despesa Total
- Lucro Líquido
- Variação Percentual do Lucro
- Debt-to-Equity Ratio Médio

### 💸 Liquidez
- Fluxo de Caixa por período
- Correlação entre Cash Flow e Net Income

### ⏱️ Operacional
- Tempo Médio de Processamento
- Correlação entre Volume e Tempo
- Tempo Médio por Resultado (Sucesso vs Falha)

### ✅ Qualidade
- Taxa de Sucesso vs Falha
- Impacto de Dados Ausentes
- Correlação Volume x Lucro


## ⭐ Diferenciais do Projeto

Implementação de dois modos analíticos (Dados Originais vs Dados Recalculados)

Reprocessamento de métricas financeiras com base em regras contábeis

Análise de correlação entre indicadores financeiros e operacionais

Estrutura modular de dashboard em Streamlit

Storytelling orientado a perguntas de negócio

Documentação técnica e dicionário de dados

## 📌 Principais Insights Gerados

A análise permitiu identificar que:

- O lucro líquido apresentava divergências quando comparado às regras contábeis tradicionais.
- O fluxo de caixa, apesar de positivo em média, apresentou períodos críticos.
- Houve correlação moderada entre volume de transações e tempo de processamento, indicando impacto operacional da demanda.
- Transações com falha apresentaram maior tempo médio de processamento, sugerindo gargalos no fluxo de validação.

Esses achados demonstram a importância da governança de dados e da análise integrada entre indicadores financeiros e operacionais.

## 🚀 Impacto Estratégico

Este projeto demonstra a capacidade de:

- Traduzir problemas de negócio em perguntas analíticas
- Modelar dados relacionais para suportar análise financeira
- Validar métricas e identificar inconsistências estruturais
- Construir dashboards executivos com foco em decisão
- Integrar análise financeira e operacional em uma visão única

O resultado é uma solução analítica completa, com foco em confiabilidade, governança e geração de valor.

## 🧠 Principais Aprendizados

- Importância da validação de métricas antes da análise
- Impacto da granularidade temporal na interpretação de tendências
- Diferença entre resultado contábil e geração real de caixa
- Correlação não implica causalidade
- Importância do storytelling em dashboards executivos

## ▶️ Como Executar o Projeto

1. Clone o repositório
2. Instale as dependências:
   pip install -r requirements.txt
3. Execute a aplicação:
   streamlit run app.py


## 👤 Autor
Anderson
Projeto desenvolvido para fins de portfólio profissional em Análise de Dados.