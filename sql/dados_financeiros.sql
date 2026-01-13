/*
Projeto: Controle Financeiro Corporativo
Arquivo: dados_financeiros.sql
Descrição: Criação do modelo relacional, staging e carga de dados
Autor: Anderson
Banco: SQLite
*/

-- ===============================
-- TABELA: account_type
-- Representa a classificação financeira das transações
-- ===============================
CREATE TABLE account_type (
    account_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_type_name TEXT NOT NULL UNIQUE
);

-- ===============================
-- TABELA: transactions
-- Representa o evento financeiro individual
-- ===============================
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    transaction_date TEXT NOT NULL, -- armazenado como TEXT no SQLite
    transaction_amount REAL NOT NULL,
    transaction_outcome TEXT NOT NULL,
    processing_time_seconds REAL,
    accuracy_score REAL,
    missing_data_indicator INTEGER,
    normalized_transaction_amount REAL,
    account_type_id INTEGER NOT NULL,
    FOREIGN KEY (account_type_id) REFERENCES account_type(account_type_id)
);

-- ===============================
-- TABELA: financial_metrics
-- Armazena métricas financeiras e operacionais
-- Relacionamento 1:1 com transactions
-- ===============================
CREATE TABLE financial_metrics (
    metrics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    revenue REAL,
    expenditure REAL,
    net_income REAL,
    gross_profit REAL,
    profit_margin REAL,
    cash_flow REAL,
    operating_expenses REAL,
    debt_to_equity_ratio REAL,
    transaction_volume INTEGER,
    transaction_id INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

-- ===============================
-- TABELA: staging_transactions
-- Camada de staging (dados brutos já padronizados via Python)
-- ===============================
CREATE TABLE staging_transactions (
    transaction_id INTEGER,
    transaction_date TEXT,
    account_type TEXT,
    transaction_amount REAL,
    cash_flow REAL,
    net_income REAL,
    revenue REAL,
    expenditure REAL,
    profit_margin REAL,
    debt_to_equity_ratio REAL,
    operating_expenses REAL,
    gross_profit REAL,
    transaction_volume INTEGER,
    processing_time_seconds REAL,
    accuracy_score REAL,
    missing_data_indicator INTEGER,
    normalized_transaction_amount REAL,
    transaction_outcome TEXT
);

-- ===============================
-- CARGA DA DIMENSÃO account_type
-- ===============================
INSERT INTO account_type (account_type_name)
SELECT DISTINCT account_type
FROM staging_transactions;

-- Validação
SELECT * FROM account_type;

-- ===============================
-- CARGA DA TABELA transactions
-- Relacionando transações ao tipo de conta
-- ===============================
INSERT INTO transactions (
    transaction_id,
    transaction_date,
    account_type_id,
    transaction_amount,
    transaction_outcome,
    processing_time_seconds,
    accuracy_score,
    missing_data_indicator,
    normalized_transaction_amount
)
SELECT
    s.transaction_id,
    s.transaction_date,
    a.account_type_id,
    s.transaction_amount,
    s.transaction_outcome,
    s.processing_time_seconds,
    s.accuracy_score,
    s.missing_data_indicator,
    s.normalized_transaction_amount
FROM staging_transactions s
JOIN account_type a
    ON s.account_type = a.account_type_name;

-- Validação
SELECT COUNT(*) FROM transactions;

-- ===============================
-- CARGA DA TABELA financial_metrics
-- ===============================
INSERT INTO financial_metrics (
    transaction_id,
    cash_flow,
    net_income,
    revenue,
    expenditure,
    gross_profit,
    profit_margin,
    operating_expenses,
    debt_to_equity_ratio,
    transaction_volume
)
SELECT
    transaction_id,
    cash_flow,
    net_income,
    revenue,
    expenditure,
    gross_profit,
    profit_margin,
    operating_expenses,
    debt_to_equity_ratio,
    transaction_volume
FROM staging_transactions;

-- Validação
SELECT COUNT(*) FROM financial_metrics;

-- ===============================
-- CONSULTA DE VALIDAÇÃO FINAL
-- ===============================
SELECT
    t.transaction_id,
    a.account_type_name,
    f.revenue,
    f.net_income
FROM transactions t
JOIN account_type a
    ON t.account_type_id = a.account_type_id
JOIN financial_metrics f
    ON t.transaction_id = f.transaction_id
LIMIT 10;
/*
Projeto: Controle Financeiro Corporativo
Arquivo: dados_financeiros.sql
Descrição: Criação do modelo relacional, staging e carga de dados
Autor: Anderson
Banco: SQLite
*/

-- ===============================
-- TABELA: account_type
-- Representa a classificação financeira das transações
-- ===============================
CREATE TABLE account_type (
    account_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_type_name TEXT NOT NULL UNIQUE
);

-- ===============================
-- TABELA: transactions
-- Representa o evento financeiro individual
-- ===============================
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    transaction_date TEXT NOT NULL, -- armazenado como TEXT no SQLite
    transaction_amount REAL NOT NULL,
    transaction_outcome TEXT NOT NULL,
    processing_time_seconds REAL,
    accuracy_score REAL,
    missing_data_indicator INTEGER,
    normalized_transaction_amount REAL,
    account_type_id INTEGER NOT NULL,
    FOREIGN KEY (account_type_id) REFERENCES account_type(account_type_id)
);

-- ===============================
-- TABELA: financial_metrics
-- Armazena métricas financeiras e operacionais
-- Relacionamento 1:1 com transactions
-- ===============================
CREATE TABLE financial_metrics (
    metrics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    revenue REAL,
    expenditure REAL,
    net_income REAL,
    gross_profit REAL,
    profit_margin REAL,
    cash_flow REAL,
    operating_expenses REAL,
    debt_to_equity_ratio REAL,
    transaction_volume INTEGER,
    transaction_id INTEGER UNIQUE NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

-- ===============================
-- TABELA: staging_transactions
-- Camada de staging (dados brutos já padronizados via Python)
-- ===============================
CREATE TABLE staging_transactions (
    transaction_id INTEGER,
    transaction_date TEXT,
    account_type TEXT,
    transaction_amount REAL,
    cash_flow REAL,
    net_income REAL,
    revenue REAL,
    expenditure REAL,
    profit_margin REAL,
    debt_to_equity_ratio REAL,
    operating_expenses REAL,
    gross_profit REAL,
    transaction_volume INTEGER,
    processing_time_seconds REAL,
    accuracy_score REAL,
    missing_data_indicator INTEGER,
    normalized_transaction_amount REAL,
    transaction_outcome TEXT
);

-- ===============================
-- CARGA DA DIMENSÃO account_type
-- ===============================
INSERT INTO account_type (account_type_name)
SELECT DISTINCT account_type
FROM staging_transactions;

-- Validação
SELECT * FROM account_type;

-- ===============================
-- CARGA DA TABELA transactions
-- Relacionando transações ao tipo de conta
-- ===============================
INSERT INTO transactions (
    transaction_id,
    transaction_date,
    account_type_id,
    transaction_amount,
    transaction_outcome,
    processing_time_seconds,
    accuracy_score,
    missing_data_indicator,
    normalized_transaction_amount
)
SELECT
    s.transaction_id,
    s.transaction_date,
    a.account_type_id,
    s.transaction_amount,
    s.transaction_outcome,
    s.processing_time_seconds,
    s.accuracy_score,
    s.missing_data_indicator,
    s.normalized_transaction_amount
FROM staging_transactions s
JOIN account_type a
    ON s.account_type = a.account_type_name;

-- Validação
SELECT COUNT(*) FROM transactions;

-- ===============================
-- CARGA DA TABELA financial_metrics
-- ===============================
INSERT INTO financial_metrics (
    transaction_id,
    cash_flow,
    net_income,
    revenue,
    expenditure,
    gross_profit,
    profit_margin,
    operating_expenses,
    debt_to_equity_ratio,
    transaction_volume
)
SELECT
    transaction_id,
    cash_flow,
    net_income,
    revenue,
    expenditure,
    gross_profit,
    profit_margin,
    operating_expenses,
    debt_to_equity_ratio,
    transaction_volume
FROM staging_transactions;

-- Validação
SELECT COUNT(*) FROM financial_metrics;

-- ===============================
-- CONSULTA DE VALIDAÇÃO FINAL
-- ===============================
SELECT
    t.transaction_id,
    a.account_type_name,
    f.revenue,
    f.net_income
FROM transactions t
JOIN account_type a
    ON t.account_type_id = a.account_type_id
JOIN financial_metrics f
    ON t.transaction_id = f.transaction_id
LIMIT 10;
