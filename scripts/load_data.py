import pandas as pd
import sqlite3
from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dados_financeiros.db"
CSV_PATH = BASE_DIR / "data" / "accounting_data.csv"

# Conexão com o banco
conn = sqlite3.connect(DB_PATH)

# Mapeando colunas
COLUMN_MAPPING = {
    "Transaction ID": "transaction_id",
    "Date": "transaction_date",
    "Account Type": "account_type",
    "Transaction Amount": "transaction_amount",
    "Cash Flow": "cash_flow",
    "Net Income": "net_income",
    "Revenue": "revenue",
    "Expenditure": "expenditure",
    "Profit Margin": "profit_margin",
    "Debt-to-Equity Ratio": "debt_to_equity_ratio",
    "Operating Expenses": "operating_expenses",
    "Gross Profit": "gross_profit",
    "Transaction Volume": "transaction_volume",
    "Processing Time (seconds)": "processing_time_seconds",
    "Accuracy Score": "accuracy_score",
    "Missing Data Indicator": "missing_data_indicator",
    "Normalized Transaction Amount": "normalized_transaction_amount",
    "Transaction Outcome": "transaction_outcome"
}

# Leitura do CSV aplicando o mapping
df = pd.read_csv(CSV_PATH)

df = df.rename(columns=COLUMN_MAPPING)

#Garantindo ordem correta
df = df[list(COLUMN_MAPPING.values())]

print(df.columns.tolist())

# Carga para tabela staging
df.to_sql(
    "staging_transactions",
    conn,
    if_exists="append",
    index=False
)

conn.close()

print("✅ Dados importados com sucesso para staging_transactions.")
